"""
-*- coding: utf-8 -*-
----------------------------------------------------------------------------
Created By: Franco Barrionuevo
Created Date: September 2026
----------------------------------------------------------------------------

radiometric_uncertainty.py

Utilities for computing radiometric uncertainty (based on Equivalent
Number of Looks, ENL) from a raster and a set of vector sample polygons.

Pipeline overview
------------------
1. `read_check_vector`   -> read samples, align CRS with raster
2. `clip_tif`             -> clip raster by each polygon, extract valid values
3. `get_dict_stats`       -> per-sample Mean / Std / ENL
4. `error_vs_probability` -> error in dB and probability for a given ENL
5. `plot_error_prob` -> probability plot (error_dB vs probability) for a given ENL
6. `get_unct`             -> nearest error_dB bound for a target probability
7. `get_dict_ru`          -> add uncertainty columns to the stats table
7. `radunc`               -> end-to-end pipeline, exports results to Excel
"""

import warnings

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio as rio
from rasterio.mask import mask
from scipy.stats import gamma


def read_check_vector(tif_path, samples_path):
    """
    Read a vector samples file and check whether its CRS matches the
    raster's CRS. If they don't match, reproject the samples to the
    raster's CRS and emit a warning.

    Parameters
    ----------
    tif_path : str or Path
        Path to the raster (.tif) file.
    samples_path : str or Path
        Path to the vector samples file (e.g., shapefile, geojson).

    Returns
    -------
    geopandas.GeoDataFrame
        The samples GeoDataFrame, reprojected to match the raster's CRS
        if needed.

    Raises
    ------
    ValueError
        If either the raster or the samples file has no CRS defined.
    """
    gdf_samples = gpd.read_file(samples_path)

    with rio.open(tif_path) as src:
        raster_crs = src.crs

    # Guard against missing CRS on either side
    if raster_crs is None:
        raise ValueError(f"Raster '{tif_path}' has no CRS defined.")
    if gdf_samples.crs is None:
        raise ValueError(f"Samples file '{samples_path}' has no CRS defined.")

    if gdf_samples.crs != raster_crs:
        warnings.warn(
            f"CRS mismatch: samples CRS ({gdf_samples.crs}) does not match "
            f"raster CRS ({raster_crs}). Reprojecting samples to match raster.",
            UserWarning,
            stacklevel=2,
        )
        gdf_samples = gdf_samples.to_crs(raster_crs)

    return gdf_samples


def clip_tif(tif_path, samples_path, samples_col, back_val=0):
    """
    Clip a raster with each polygon in a vector samples file and extract
    the pixel values within each polygon, excluding background values.

    For each polygon in the samples file, the raster is clipped to that
    polygon's extent, the specified background value is masked out (set
    to NaN and removed), and the remaining valid pixel values are stored
    in a dictionary keyed by the polygon's identifier.

    Parameters
    ----------
    tif_path : str or Path
        Path to the raster (.tif) file to clip.
    samples_path : str or Path
        Path to the vector samples file (e.g., shapefile, geojson)
        containing the polygons to clip with.
    samples_col : str
        Name of the column in the samples file to use as the identifier
        (dictionary key) for each polygon's extracted values.
    back_val : int or float, optional
        Background/nodata value to exclude from the extracted pixel
        values (default is 0).

    Returns
    -------
    dict
        Dictionary mapping each polygon's identifier (from `samples_col`)
        to a 1D numpy array of valid (non-background, non-NaN) pixel
        values extracted from that polygon.
    """
    with rio.open(tif_path) as src:
        gdf_samples = read_check_vector(tif_path, samples_path)

        dict_samp_val = {}
        for idx, row in gdf_samples.iterrows():
            geom = [row.geometry]  # mask() expects a list of geometries
            #geom = row.geometry  # mask() expects a list of geometries
            out_image, out_transform = mask(src, geom, all_touched=True, crop=True)

            x = out_image
            x[0][x[0] == back_val] = np.nan
            x = x[~np.isnan(x)]

            dict_samp_val[row[samples_col]] = x

    return dict_samp_val


def error_vs_probability(enl, minError_dB=0.1, maxError_dB=4, stepError_dB=0.01):
    """
    For a given ENL, compute probability for a range of error_dB values.

    Parameters
    ----------
    enl : float
        Equivalent Number of Looks (ENL), shape parameter of the Gamma pdf.
    minError_dB, maxError_dB, stepError_dB : float
        Range of error_dB values to evaluate.

    Returns
    -------
    error_dBs : ndarray
        The error_dB values evaluated.
    probabilities : ndarray
        The corresponding probability for each error_dB.
    """
    error_dBs = np.arange(minError_dB, maxError_dB + 1e-9, stepError_dB)

    lower = 10 ** (-error_dBs / 10)
    upper = 10 ** (error_dBs / 10)

    probabilities = gamma.cdf(upper, a=enl, scale=1.0 / enl) - gamma.cdf(lower, a=enl, scale=1.0 / enl)

    return error_dBs, probabilities

def plot_error_prob(enl, figsize=(10, 4)):
    """
    Plot the probability vs. radiometric uncertainty (error_dB) curve
    for a given ENL.

    Computes the probability curve (via `error_vs_probability`) and
    plots the portion where probability exceeds 45%, showing how
    probability increases with radiometric uncertainty bound.

    Parameters
    ----------
    enl : float
        Equivalent Number of Looks (ENL) to compute and plot the curve for.
    figsize : tuple of float, optional
        Figure size in inches, as (width, height) (default is (10, 4)).

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure.
    ax : matplotlib.axes.Axes
        The axes containing the plot.
    """
    error_dBs, probabilities = error_vs_probability(
        enl, minError_dB=0.1, maxError_dB=4, stepError_dB=0.01
    )

    fig, ax = plt.subplots(figsize=figsize)

    mask = probabilities > 0.45
    ax.plot(error_dBs[mask], probabilities[mask] * 100, color='red')
    ax.set_title(f'Probability vs Radiometric Uncertainty - ENL:{enl}', fontsize=14)
    ax.set_xlabel('Radiometric Uncertainty (dB)', fontsize=12)
    ax.set_ylabel('Probability (%)', fontsize=12)

    return fig, ax


def get_unct(enl, p):
    """
    Get the error bound (in dB) corresponding to a target probability,
    for a given ENL, by nearest-neighbor lookup.

    Computes the probability curve for the given ENL over a range of
    error_dB values (via `error_vs_probability`), then finds the
    error_dB value whose associated probability is closest to the
    target probability `p`.

    Parameters
    ----------
    enl : float
        Equivalent Number of Looks (ENL), shape parameter of the
        underlying Gamma distribution.
    p : float
        Target probability (between 0 and 1) for which to find the
        closest matching error_dB.

    Returns
    -------
    error_dB : float
        The error_dB value whose corresponding probability is nearest
        to `p`.
    prob_near : float
        The actual (nearest) probability achieved at `error_dB`, which
        may differ slightly from `p` due to the discrete grid used by
        `error_vs_probability`.
    """
    error_dBs, probabilities = error_vs_probability(enl)

    idx = np.abs(probabilities - p/100).argmin()  # index of nearest probability value (shortest absolute distance)
    error_dB = error_dBs[idx]
    prob_near = probabilities[idx]

    return error_dB, prob_near


def get_df_stats(tif_path, samples_path, samples_col, back_val):
    """
    Compute per-sample statistics (mean, standard deviation, and ENL)
    from raster values clipped by each polygon in a samples file.

    For each sample polygon, extracts the corresponding raster pixel
    values (via `clip_tif`), then computes the mean, standard
    deviation, and Equivalent Number of Looks (ENL = (mean/std)^2)
    for that sample.

    Parameters
    ----------
    tif_path : str or Path
        Path to the raster (.tif) file.
    samples_path : str or Path
        Path to the vector samples file (e.g., shapefile, geojson).
    samples_col : str
        Name of the column in the samples file used to identify each
        polygon/sample.
    back_val : int or float, optional
        Background/nodata value to exclude from the extracted pixel
        values (default is 0).

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per sample, containing columns:
        'Sample', 'Mean', 'Std', and 'ENL'.

    Notes
    -----
    Samples with zero standard deviation will produce an infinite ENL
    (division by zero); this is not currently handled and will
    propagate into `get_unct` / `error_vs_probability` downstream.
    """
    dict_samp_val = clip_tif(tif_path, samples_path, samples_col, back_val=back_val)

    list_samp = []
    list_mean = []
    list_std = []
    list_enl = []

    for samp in dict_samp_val.keys():
        vals = dict_samp_val[samp]
        mean = np.nanmean(vals)
        std = np.nanstd(vals)
        enl = round((mean / std) ** 2, 1)

        list_samp.append(samp)
        list_mean.append(mean)
        list_std.append(std)
        list_enl.append(enl)

    df_samp_stats = pd.DataFrame({
        'Sample': list_samp,
        'Mean': list_mean,
        'Std': list_std,
        'ENL': list_enl,
    })

    return df_samp_stats


def get_df_ru(df_samp_stats, p):
    """
    Add radiometric uncertainty and matched-probability columns to a
    per-sample statistics DataFrame, for a given target probability.

    For each sample (row), looks up the error_dB bound whose probability
    is nearest to `p` (via `get_unct`), using that sample's own ENL
    value, and appends the result as two new columns.

    Parameters
    ----------
    dict_samp_stats : pandas.DataFrame
        Per-sample statistics, as returned by `get_dict_stats`. Must
        contain an 'ENL' column.
    p : float
        Target probability, expressed as a percentage (0-100), e.g.
        `p=95` for a 95% probability bound.

    Returns
    -------
    pandas.DataFrame
        The input DataFrame with two new columns added:
        - f'Rad. Unc. {p} [dB]': the matched error_dB bound per sample.
        - f'Real. Prob. {p} [%]': the actual probability achieved at
          that error_dB (may differ slightly from `p` due to the
          discrete grid used by `get_unct`).

    Notes
    -----
    The DataFrame is modified in place (columns are added directly to
    `dict_samp_stats`), and the same object is also returned.
    """
    list_incrad = []
    list_realprob = []

    for idx, row in df_samp_stats.iterrows():
        error_dB, prob_near = get_unct(row['ENL'], p)

        list_incrad.append(round(error_dB, 2))
        list_realprob.append(round(prob_near*100, 2))

    df_samp_stats[f'Rad. Unc. {p} [dB]'] = list_incrad
    df_samp_stats[f'Real. Prob. {p} [%]'] = list_realprob

    return df_samp_stats


def radunc(tif_path, samples_path, samples_col, list_ci, back_val=0, output='output'):
    """
    Compute per-sample radiometric uncertainty statistics and export
    the results to an Excel file.

    For each sample polygon in the samples file, computes basic
    statistics (mean, std, ENL) from the clipped raster values, then
    for each target probability in `list_probs`, appends the matched
    error_dB bound and the actual achieved probability.

    Parameters
    ----------
    tif_path : str or Path
        Path to the raster (.tif) file.
    samples_path : str or Path
        Path to the vector samples file (e.g., shapefile, geojson).
    samples_col : str
        Name of the column in the samples file used to identify each
        polygon/sample.
    list_probs : list of float
        Target probabilities, expressed as percentages (0-100), e.g.
        `[90, 95, 99]`.
    back_val : int or float, optional
        Background/nodata value to exclude when extracting raster
        values per sample (default is 0).
    output : str, optional
        Output file name (without extension) for the exported Excel
        file (default is 'output').

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per sample, containing 'Sample', 'Mean',
        'Std', 'ENL', and — for each probability in `list_probs` — a
        'Rad. Unc. {p} [dB]' and 'Real. Prob. {p} [%]' column pair.
    """
    df_samp_ru = get_df_stats(tif_path, samples_path, samples_col, back_val=back_val)

    for p in list_ci:
        df_samp_ru = get_df_ru(df_samp_ru, p)
        
        
    df_samp_ru.to_excel(f'../../{output}.xlsx', index=False)
    
    print(f'\nSummary table was correctly exported as: {output}.xlsx ✅')

    return df_samp_ru
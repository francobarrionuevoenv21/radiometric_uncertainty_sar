# Radiometric Uncertainty SAR

---

### Description

`radiometric_uncertainty_sar` is a small Python package for estimating **radiometric
uncertainty** from SAR imagery based on the **Equivalent Number of Looks (ENL)**.
Given a raster (`.tif`) and a set of vector sample polygons, it clips the raster
by each polygon, computes per-sample statistics (mean, standard deviation, ENL),
and estimates the radiometric uncertainty bound (in dB) associated with a target
confidence probability.

### Installation and Use

1. **Clone the repository**

   ```bash
   git clone https://github.com/francobarrionuevoenv21/radiometric_uncertainty_sar.git
   ```

2. **Move into the folder containing the `.py` file**

   ```bash
   cd radiometric_uncertainty_sar/radunc
   ```

3. **Install the requirements**

   ```bash
   pip install -r requirements.txt
   ```

4. **Import and use it in your script or notebook**

   ```python
   from radunc import radunc as rdc

   df = rdc(
       tif_path="raster.tif", # (1, n, m) raster, it means one band or polarization
       samples_path="samples.shp", # Vector with homogeneus samples (every vector format readable by geopandas allowed)
       samples_col="col_samples_name", # Column with samples labels in the vector file
       list_ic=[90, 95, 99], # List with the confidence intervals to compute for each ENL
   )
   ```

### Output

A Pandas dataframe summarizing the backscatering coefficient ($\sigma^{0}$) mean value, standard deviation value, ENL, radiometric uncertainty and the true confidence interval associated to the uncertainty computed for each sample contained in the vector file. It is also generated .xlsx file exported as defaul as *output.xlsx*.

> 💡 NOTE: Since the method provides the nearest neighbour confidence interval to the target, the output also provides the true value for verification. 


### Acknowledgements

The package was developed during the course Applications of Synthetic Aperture Radar Images dictated by Dra. Mercedes Salvia as part of the Master in Spatial Information Applications curricula at the Gulich Institute during August-September 2026. The images and samples vector used for testing were provided by Prof. Salvia. 
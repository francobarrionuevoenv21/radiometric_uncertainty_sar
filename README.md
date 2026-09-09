# Radiometric Uncertainty / Incertidumbre Radiométrica

---

### Description

`radiometric_uncertainty_sar` is a small Python package for estimating **radiometric
uncertainty** from SAR imagery based on the **Equivalent Number of Looks (ENL)**.
Given a raster (`.tif`) and a set of vector sample polygons, it clips the raster
by each polygon, computes per-sample statistics (mean, standard deviation, ENL),
and estimates the radiometric uncertainty bound (in dB) associated with a target
confidence probability.

### Installation — Local

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   ```

2. **Move into the folder containing the `.py` file**

   ```bash
   cd <your-repo>/radiometric_uncertainty
   ```

3. **Install the requirements**

   ```bash
   pip install -r requirements.txt
   ```

4. **Import and use it in your script or notebook**

   ```python
   from radunc import radunc as rdc

   df = rdc(
       tif_path="raster.tif",
       samples_path="samples.shp",
       samples_col="col_samples_name",
       list_probs=[90, 95, 99],
   )
   ```

### Installation — Google Colab

1. **Clone the repository** (run this in a Colab cell)

   ```python
   !git clone https://github.com/<your-username>/<your-repo>.git
   ```

2. **Move into the folder containing the `.py` file**

   ```python
   %cd <your-repo>/radiometric_uncertainty
   ```

3. **Install the requirements**

   ```python
   !pip install -r requirements.txt
   ```

4. **Import and use it**


> 💡 Tip: some geospatial dependencies (`rasterio`, `geopandas`) may take a
> minute to install in Colab due to their compiled dependencies (GDAL). This
> is expected — just wait for the install cell to finish before importing.

---

### Descripción

`radiometric_uncertainty_sar` es un pequeño paquete de Python para estimar la
**incertidumbre radiométrica** en imágenes SAR a partir del **Número Equivalente
de Looks (ENL)**. Dado un raster (`.tif`) y un conjunto de polígonos de muestra
vectoriales, recorta el raster según cada polígono, calcula estadísticas por
muestra (media, desvío estándar, ENL), y estima el límite de incertidumbre
radiométrica (en dB) asociado a una probabilidad de confianza objetivo.

### Instalación — Local

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/<tu-usuario>/<tu-repo>.git
   ```

2. **Ingresar a la carpeta donde está el archivo `.py`**

   ```bash
   cd <tu-repo>/radiometric_uncertainty
   ```

3. **Instalar los requerimientos**

   ```bash
   pip install -r requirements.txt
   ```

4. **Importar y usar el paquete en tu script o notebook**

   ```python
   from radunc import radunc as rdc

   df = rdc(
       tif_path="raster.tif",
       samples_path="samples.shp",
       samples_col="col_samples_name",
       list_probs=[90, 95, 99],
   )
   ```

### Instalación — Google Colab

1. **Clonar el repositorio** (ejecutar en una celda de Colab)

   ```python
   !git clone https://github.com/<tu-usuario>/<tu-repo>.git
   ```

2. **Ingresar a la carpeta donde está el archivo `.py`**

   ```python
   %cd <tu-repo>/radiometric_uncertainty
   ```

3. **Instalar los requerimientos**

   ```python
   !pip install -r requirements.txt
   ```

4. **Importar y usar el paquete**


> 💡 Sugerencia: algunas dependencias geoespaciales (`rasterio`, `geopandas`)
> pueden tardar un minuto en instalarse en Colab debido a sus dependencias
> compiladas (GDAL). Esto es esperable — solo hay que esperar a que termine
> la celda de instalación antes de importar el paquete.

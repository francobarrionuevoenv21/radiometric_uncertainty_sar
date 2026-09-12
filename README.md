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


### Acknowledgements

The package was developed during the course Applications of Synthetic Aperture Radar Images dictated by Dra. Mercedes Salvia as part of the Master in Spatial Information Applications curricula at the Gulich Institute during August-September 2026. The images and samples vector used for testing were provided by Prof. Salvia. 

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


### Agradecimientos

El paquete fue desarrollado durante el cursado de la materia Aplicaciones de las imágenes de radar de apertura sintética dictado por la Dra. Mercedes Salvia, materia que forma parte de la currícula de la Maestría en aplicaciones de información espacial del Instituto Gulich durante agosto-septiembre del 2026. La imágen, asi como el vector de muestras para usadas para el testeo fueron provistas para la Dra. Salvia. 
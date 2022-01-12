import numpy as np
import rasterio as rio
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from matplotlib import pyplot as plt
from pathlib import Path






def load_landsat_image(img_folder, bands):
    
    image = {}
    path = Path(img_folder)
    for band in bands:
        # considering the landsat images end with *_SR_B#.TIF, we will use it to locate the correct file
        file = next(path.glob(f'*_SR_{band}.tif'))
        print(f'Opening file {file}')
        ds = rio.open(file)
        image.update({band: ds.read(1)})

    return image

ruta = '/Users/nazariocano/Desktop/2021/12/5/T14QKG'

RES = load_landsat_image(ruta, 'NDVI')
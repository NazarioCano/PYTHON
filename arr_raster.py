import numpy as np
import rasterio as rio
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from constants import BANDS, PRODUCTS
from matplotlib import pyplot as plt
from pathlib import Path








def load_landsat_image(ruta, bands, year, mes, dia):
    image = {}
    path = Path(ruta)
    for band in bands:
        file = Path(path,f'{year}/{mes}/{dia}/T14QKG/{band}.TIF')
        print(f'Opening file {file}')
        ds = rio.open(file)
        #image.update({band: ds.read(1)})
    return image

ruta = '/Users/nazariocano/Desktop/PYTHON'

#RES = load_landsat_image(ruta,['BO3'], '2021', '12', '5')
rio.open('/Users/nazariocano/Desktop/2021/12/5/T14QKG/BO3.TIF')

import numpy as np
import rasterio as rio
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from matplotlib import pyplot as plt
from pathlib import Path

def load_landsat_image(file):
    print(f'Opening file {file}')
    ds = rio.open(file)
    print(ds.profile)
    return ds

def calc_histograma(datos, bandas):
    print('Bandas',bandas)
    unique, counts = np.unique(datos, return_counts = True)
    valores = unique
    frecuencias = counts
    plt.plot(valores, frecuencias)
    plt.grid(True)
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.title('Histograma')
    plt.show()
    return unique, counts

ruta = '/Users/nazariocano/Desktop/2021/12/5'
raster = load_landsat_image('B03.TIF')

#show_hist(raster.read(1), bins=1000, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', title="Histograma")

ds = raster.read(1)
bandas = raster.count
valores, frecuencias = calc_histograma(ds, bandas)


#np.savetxt('salida.csv', valores, delimiter=',')#Imprimir valores en un rchivo de texto
#('Calculo', len(valores), len(frecuencias))
#plt.plot(valores, frecuencias)
#lt.show()
import numpy as np
import rasterio as rio
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from matplotlib import pyplot as plt
import statistics as stats


def load_landsat_image(file):
    print(f'Opening file {file}')
    ds = rio.open(file)
    return ds


def calc_medias(Datos):
    try:
        desviacionEstandar = np.std(Datos)
        print('Desviaion estandar: ',desviacionEstandar)
        media = np.mean(Datos)
        print('Media', media,)

        media_baja = stats.median_low(Datos)
        print('Media baja:', media_baja)

        media_alta = stats.median_high(Datos)
        print('Media alta:', media_alta)

        return media, media_baja, media_alta
    except: 
        print('Error al hacer los caculos')


def calc_histograma(datos, bandas):
    print('Bandas',bandas)
    try:
        unique, counts = np.unique(datos, return_counts = True)
        valores = unique
        frecuencias = counts
        plt.plot(valores, frecuencias)
        plt.grid(True)
        plt.xlabel('Valor')
        plt.ylabel('Frecuencia')
        plt.title('Histograma')
        #plt.show()
        return unique, counts
    except:
        print('Error en le calculo de histograma')

ruta = '/Users/nazariocano/Desktop/2021/12/5'
raster = load_landsat_image('2021/12/5/T14QKG/B01.TIF')

#show_hist(raster.read(1), bins=1000, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', title="Histograma")

ds = raster.read(1)
bandas = raster.count
valores, frecuencias = calc_histograma(ds, bandas)


calc_medias(valores)



#Calculo de Media, Media alta y Media baja





#np.savetxt('salida.csv', valores, delimiter=',')#Imprimir valores en un rchivo de texto
#('Calculo', len(valores), len(frecuencias))
#plt.plot(valores, frecuencias)
#lt.show()
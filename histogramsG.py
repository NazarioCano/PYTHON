#import gdal
from osgeo import gdal
import numpy as np
import os
import matplotlib.pyplot as plt


imgSat = gdal.Open('B06.TIF')  #Imagen tipo tif

print('Numero de bandas:', imgSat.RasterCount) #Numero de bandas
print('Filas:',imgSat.RasterXSize) #Numero de filas 
print('Columnas:',imgSat.RasterYSize) #Numero de columnas

#GetRasterCount   ------Numero de bandas
#ReadAsArray      ------Arreglo de numeros


#plt.figure(figsize=(8,8))
#plt.imshow(imgSat.GetRasterBand(1).ReadAsArray(), cmap='gray')
#plt.title('Banda 1 - Lansat')
Datos = imgSat.GetRasterBand(1).ReadAsArray()
print('Datos:', Datos)

MAX = np.amax(Datos)
print('Max:',MAX )
MIN = np.amin(Datos)
print('Min:', MIN)
#plt.show()  #VER GRAFICAS
plt.hist(Datos.ravel(), MAX, range=[MIN, MAX])
plt.show()
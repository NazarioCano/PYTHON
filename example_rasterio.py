import numpy as np
import rasterio as rio
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from matplotlib import pyplot as plt
import statistics as stats
from pyproj import Transformer, pyproj
from shapely.ops import transform





def load_landsat_image(file, coordenadas):
    print(f'Opening file {file}')
    ds = rio.open(file)
    salida = ds.meta.copy()
    print('salida', salida)
    recorte, Transform = mask(ds, coordenadas, crop = True)
    print('Se creo el recorte')
    salida.update({
        "driver": 'GTiff',
        "height": recorte.shape[1],
        "width": recorte.shape[2],
        "transform": Transform
    })

    Raster = rio.open('/Users/nazariocano/PYTHON' + 'recorte','w', salida )
    Raster.write(recorte)
    Raster.close()
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

coord = [{
      "type": "Polygon",
      "coordinates": [
          [
            [
              19.71807059924646
              -101.26888275146484,
            ],
            [
              19.71807059924646
              -101.23935699462889,
            ],
            [
              19.746024239625427
              -101.23935699462889,
            ],
            [
              19.746024239625427
              -101.26888275146484,
            ],
            [
              19.71807059924646
              -101.26888275146484,
            ]
          ]
        ]
      }
    

]
    
#geo = project_wsg_shape_to_csr(shapely.geo.shape(coord), 'epsg:32637')


raster = load_landsat_image('LC08_L1TP_027046_20211211_20211216_01_T1/LC08_L1TP_027046_20211211_20211216_01_T1_B1.TIF', coord)

#show_hist(raster.read(1), bins=1000, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', title="Histograma")

#ds = raster.read(1)
#bandas = raster.count
#valores, frecuencias = calc_histograma(ds, bandas)


#calc_medias(valores)



#Calculo de Media, Media alta y Media baja





#np.savetxt('salida.csv', valores, delimiter=',')#Imprimir valores en un rchivo de texto
#('Calculo', len(valores), len(frecuencias))
#plt.plot(valores, frecuencias)
#lt.show()


def project_wsg_shape_to_csr(shape, csr):
     transformer = Transformer.from_crs('epsg:4326', csr)
     project = lambda x, y: transformer.transform(x, y)
     return transform(project, shape)

def parseStringToPolygon(string):
    coordinates = [(float(item.split('/')[1]), float(item.split('/')[0])) for item in string[:-1].split('&')]
    return coordinates


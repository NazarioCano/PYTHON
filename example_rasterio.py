import numpy as np
import rasterio as rio
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from matplotlib import pyplot as plt
import statistics as stats
from pyproj import Transformer
from shapely.ops import transform
from shapely.geometry import Polygon
from rasterio.warp import calculate_default_transform, reproject, Resampling
import os


os.system ("clear")

def cambio_coordenadas(string):
    coordenadas = []
    for val in string:
      coordenadas.append([val[1], val[0]])
    return coordenadas


#Funcion trasform de wgs84 a ESPG:3857 
def project_wsg_shape_to_csr(shape, csr):
     transformer = Transformer.from_crs('epsg:4326', csr)
     project = lambda x, y: transformer.transform(x, y)
     return transform(project, shape)



#FUNCION QUE CALCULA LA REPROYECCION 
def reproject_crs(product):
  dts_crs = 'epsg:3857'
  try:
    with rio.open(product) as src:
           transform, width, height = calculate_default_transform(src.crs, dts_crs, src.width, src.height, *src.bounds)
           kwargs = src.meta.copy()
           kwargs.update({
                'crs': dts_crs,
                'transform': transform,
                'width': width,
                'height': height
            })
           with rio.open(f'reprojected.tif', 'w', **kwargs) as dst:
                for i in range(1, src.count + 1):
                    reproject(
                        source=rio.band(src, i),
                        destination=rio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=transform,
                        dst_crs=dts_crs,
                        resampling=Resampling.nearest
                    )
  except TypeError as err: 
    print('No se pudo reproyectar el tif al sistema epsg32614.\n  Error, ',err)


def load_landsat_image(file, coordenadas):
  print(f'Opening file {file}......')
  try:
      ds = rio.open(file)
      recorte, Transform = mask(ds, [coordenadas], crop = True, all_touched=True)
      salida = ds.meta.copy()
      salida.update({
        'driver': 'GTiff',
        'height': recorte.shape[1],
        "width": recorte.shape[2],
        "transform": Transform
      })

      Raster = rio.open('/Users/nazariocano/PYTHON/' + 'recorte.tif','w', **salida )
      Raster.write(recorte)
      Raster.close()
      return recorte
  except TypeError as err:
    print('No se creo el recorte \n Error,', err ) 



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
    except TypeError as err: 
        print('Error al hacer los caculos\n Error, ', err)


def calc_histograma(datos):
    print('Hiniciando calculo de histograma....')
    try:
        unique, counts = np.unique(datos, return_counts = True)
        valores = unique
        frecuencias = counts
        plt.plot(valores, frecuencias,color="blue", linewidth=0.5, linestyle="-")
        plt.grid(True)
        plt.xlabel('Valor')
        plt.ylabel('Frecuencia')
        plt.title('Histograma')
        plt.show()
        return unique, counts
    except:
        print('Error en le calculo de histograma')

coord = {
      "type": "Polygon",
      "coordinates": [
          [
            [
              -101.69563293457031,
              19.557202031700292
            ],
            [
              -101.51092529296875,
              19.557202031700292
            ],
            [
              -101.51092529296875,
              19.686879555099367
            ],
            [
              -101.69563293457031,
              19.686879555099367
            ],
            [
              -101.69563293457031,
              19.557202031700292
            ]
          ]
        ]
      }


cambio = cambio_coordenadas(coord['coordinates'][0])

poligono = project_wsg_shape_to_csr(Polygon(cambio), 'epsg:3857')
    

REP = reproject_crs('2021/12/5/T14QKG/B02.TIF')
raster = load_landsat_image('reprojected.tif', poligono)

valores, frecuencias = calc_histograma(raster)



















#show_hist(raster.read(1), bins=1000, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', title="Histograma")

#ds = raster.read(1)
#bandas = raster.count

#calc_medias(valores)
#Calculo de Media, Media alta y Media baja

#Convercion de cordenadas a poligono
#POLIG = Polygon([tuple(l) for l in coord['coordinates'][0]])
#print(POLIG)

#np.savetxt('salida.csv', valores, delimiter=',')#Imprimir valores en un rchivo de texto
#('Calculo', len(valores), len(frecuencias))
#plt.plot(valores, frecuencias)
#lt.show()





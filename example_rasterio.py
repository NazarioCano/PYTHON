import numpy as np
import rasterio as rio
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from matplotlib import pyplot as plt
import statistics as stats
from pyproj import Transformer
from shapely.ops import transform
from shapely.geometry import Polygon
from rasterio.warp import calculate_default_transform, reproject, Resampling, Affine




def parseStringToPolygon(string):
    coordinates = [(float(item.split('/')[1]), float(item.split('/')[0])) for item in string[:-1].split('&')]
    return coordinates

def project_wsg_shape_to_csr(shape, csr):
     transformer = Transformer.from_crs('epsg:4326', csr)
     print(transformer)
     project = lambda x, y: transformer.transform(x, y)
     return transform(project, shape)




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
  except: 
    print('No se pudo reproyectar el tif al sistema epsg32614.')


def load_landsat_image(file, coordenadas):
  print(f'Opening file {file}')
  try:
      ds = rio.open(file)
      recorte, Transform = mask(ds, [coordenadas], crop = True, all_touched=True)
      print('Recorte', recorte.shape[1],recorte.shape[1])
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
      return ds
  except:
    print('No se creo el recorte') 



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

coord = {
      "type": "Polygon",
      "coordinates": [
          [
            [
              19.35001948171314,
              -101.6015625
            ],
            [
              19.35001948171314,
              -101.1236572265625
            ],
            [
              19.621892180319374,
              -101.1236572265625
            ],
            [
              19.621892180319374,
              -101.6015625
            ],
            [
              19.35001948171314,
              -101.6015625
            ]
          ]
        ]
      }



POLIG = Polygon([tuple(l) for l in coord['coordinates'][0]])
#print(POLIG)

CORDE = project_wsg_shape_to_csr(Polygon(POLIG), 'epsg:3857')
#print('COODER', CORDE)
    
#geo = project_wsg_shape_to_csr(shapely.geo.shape(coord), 'epsg:32637')

#REP = reproject_crs('2021/12/5/T14QKG/B02.TIF')
raster = load_landsat_image('reprojected.tif', CORDE)

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





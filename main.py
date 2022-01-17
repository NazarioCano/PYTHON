from arr_raster import salida
import numpy as np
import rasterio as rio
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from matplotlib import pyplot as plt
from pyproj import Transformer
from shapely.ops import transform
from shapely.geometry import Polygon


def cambio_coord(string):
    coordenadas = []
    for val in string:
      coordenadas.append([val[1], val[0]])
    return coordenadas

def project_wsg_shape_to_csr(shape, csr):
     transformer = Transformer.from_crs('epsg:4326', csr)
     project = lambda x, y: transformer.transform(x, y)
     return transform(project, shape)


coord = {
      "type": "Polygon",
      "coordinates": [
          [
            [
              -101.25211358070374,
              19.677151311915576
            ],
            [
              -101.25096559524536,
              19.677151311915576
            ],
            [
              -101.25096559524536,
              19.67790898446818
            ],
            [
              -101.25211358070374,
              19.67790898446818
            ],
            [
              -101.25211358070374,
              19.677151311915576
            ]
          ]
        ]
      }

Ncoord = cambio_coord(coord['coordinates'][0])
poligono = project_wsg_shape_to_csr(Polygon(Ncoord), 'epsg:3857')
fecha_inicial = '2021-12-1'
fecha_final = '2021-12-25'

PRODUCTO = 'S10'
FILTRO = 'NDVI'
  


def main(fechaI, fechaF, producto, filtro, coord):

    try: 
        recortes = salida(fechaI, fechaF, coord, producto, filtro)
        for mes in recortes:
          res = recortes[mes]
          media = np.mean(res)
          alto = np.amax(res)
          bajo = np.amin(res)
          print('Alto: ', alto) 
          print('Bajo: ', bajo)
          print('Media ', media)
          print('\n')
    except TypeError as err:
        print('Error,', err)

RES = main(fecha_inicial, fecha_final, PRODUCTO, FILTRO, poligono)



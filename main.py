from arr_raster import salida
import numpy as np
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
              -101.5932047367096,
              19.648437934086825
            ],
            [
              -101.59238934516907,
              19.648437934086825
            ],
            [
              -101.59238934516907,
              19.64898355638197
            ],
            [
              -101.5932047367096,
              19.64898355638197
            ],
            [
              -101.5932047367096,
              19.648437934086825
            ]
          ]
        ]


      }

Ncoord = cambio_coord(coord['coordinates'][0])
poligono = project_wsg_shape_to_csr(Polygon(Ncoord), 'epsg:3857')
fecha_inicial = '2021-11-5'
fecha_final = '2021-12-11'

PRODUCTO = 'L30'
FILTRO = 'NDVI'
UNITARIO =  True



def main(fechaI, fechaF, producto, filtro, coord):  
    try: 
        recortes = salida(fechaI, fechaF, coord, producto, filtro)
        print(recortes)
        for mes in recortes:
          res = recortes[mes]
          media = np.mean(res)
          alto = np.amax(res)
          bajo = np.amin(res)
          print('Alto: ', alto) 
          print('Media ', media)
          print('Baja: ', bajo)
          print('\n')
    except TypeError as err:
        print('Error,', err)

RES = main(fecha_inicial, fecha_final, PRODUCTO, FILTRO, poligono)



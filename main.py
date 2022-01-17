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
              -101.26259565353394,
              19.679464727543987
            ],
            [
              -101.2575101852417,
              19.679464727543987
            ],
            [
              -101.2575101852417,
              19.682111476502076
            ],
            [
              -101.26259565353394,
              19.682111476502076
            ],
            [
              -101.26259565353394,
              19.679464727543987
            ]
          ]
        ]
      }

Ncoord = cambio_coord(coord['coordinates'][0])
poligono = project_wsg_shape_to_csr(Polygon(Ncoord), 'epsg:3857')
fecha_inicial = '2021-12-1'
fecha_final = '2021-12-25'

PRODUCTO = 'L30'
FILTRO = 'NDVI'

def main(fechaI, fechaF, producto, filtro, coord):
    try: 
        recortes = salida(fechaI, fechaF, coord, producto, filtro)
        print(recortes)

    except TypeError as err:
        print('Error,', err)

RES = main(fecha_inicial, fecha_final, PRODUCTO, FILTRO, poligono)
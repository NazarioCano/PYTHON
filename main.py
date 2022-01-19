from arr_raster import cambio_coord, project_wsg_shape_to_csr, salida
import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry import Polygon


def arreglo_valores(arrayVal):
  Altos = []
  Medios = []
  Bajos = []
  Fechas = []
  for fecha in arrayVal:
    Altos.append(fecha['valores'][0])
    Medios.append(fecha['valores'][1])
    Bajos.append(fecha['valores'][2])
    Fechas.append(fecha['fecha'])
  return Altos, Medios, Bajos, Fechas


coord = {
      "type": "Polygon",
      "coordinates":[
          [
            [
              -103.02017211914062,
              20.347845967700426
            ],
            [
              -102.98755645751953,
              20.347845967700426
            ],
            [
              -102.98755645751953,
              20.37295205137154
            ],
            [
              -103.02017211914062,
              20.37295205137154
            ],
            [
              -103.02017211914062,
              20.347845967700426
            ]
          ]
        ]
      }

Ncoord = cambio_coord (coord['coordinates'][0])
poligono = project_wsg_shape_to_csr(Polygon(Ncoord), 'epsg:3857')
fecha_inicial = '2021-11-1'
fecha_final = '2021-12-30'
PRODUCTO = 'L30'
FILTRO = 'NDVI'
bandera = True
  
def main(fechaI, fechaF, producto, filtro, coord, bandera):
  mesesInvalidos = []
  datosSalida = []
  try: 
      recortes,x = salida(fechaI, fechaF, coord, producto, filtro)
      i=0
      for recorte in recortes:
        for mes in recorte:
          res = recorte[mes]
          media = np.mean(res)
          alto = np.amax(res)
          bajo = np.amin(res)
          print('Mes:', x[i])
          print('Dia:',mes)
          print('Alto:', alto)
          print('Media:', media)
          print('Baja:', bajo)
          print('\n')
          if bandera == True:
            if alto > 1 or bajo < -1:
              mesesInvalidos.append({x[i]: mes})
              continue
            datosSalida.append({
              'fecha': str(x[i]) + '-' + str(mes),
              'valores': [alto, media, bajo]}
            ) 
          else:
            datosSalida.append({
              'fecha': str(x[i]) + '-' + str(mes),
              'valores': [alto, media, bajo]}
            ) 
        i=i+1
      altos, medios, bajos, fechas = arreglo_valores(datosSalida)
      return altos, medios, bajos, fechas, mesesInvalidos
  except TypeError as err:
    print('Error,', err)


altos, medios, bajos, fechas, mesesInvalidos = main(fecha_inicial, fecha_final, PRODUCTO, FILTRO, poligono, bandera)
print(mesesInvalidos)
fig, ax = plt.subplots()
ax.plot(fechas, altos, color = 'tab:purple', label = 'Altos')
ax.plot(fechas, medios, color = 'tab:green', label = 'Medio')
ax.plot(fechas, bajos, color = 'tab:red', label = 'Bajos')
ax.set_ylim([-1,1])
ax.legend(loc = 'upper right')
ax.set_xlabel("Fechas")
ax.set_ylabel("Valor")
ax.grid()
plt.show()

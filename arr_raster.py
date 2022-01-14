from constants import ALEJ, NAZ
from example_rasterio import calc_histograma
import numpy as np
import rasterio as rio
import glob
import re
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from matplotlib import pyplot as plt
from pathlib import Path

#ruta = '/Users/nazariocano/Desktop/PYTHON'
#RES = load_landsat_image(ruta,['BO3'], '2021', '12', '5')

def months(inicial,final):
    class RES : 
        meses = tuple
        año = ''
        inicio = ''
    
    fecha_init=re.findall('([A-Z0-9]{1,4})',inicial)
    year_init=int(fecha_init[0])
    month_init=int(fecha_init[1])
    day_init=int(fecha_init[2])

    fecha_fin=re.findall('([A-Z0-9]{1,4})',final)
    year_fin=int(fecha_fin[0])
    month_fin=int(fecha_fin[1])
    day_fin=int(fecha_fin[2])
    
    ruta = f'{NAZ}/{year_init}/*/'
    fechas = glob.glob(ruta)
    meses=[]
    try:
        for fecha in fechas:
            mes = int(re.findall('[0-9]+',fecha)[2])#Checar las rutas que contengan numeros #alejandro 2 nazario 1
            meses.append(mes)  #Se agregan los meses
            meses.sort()
        if month_init in meses:
            indice_in=meses.index(month_init)

        if month_fin in meses:
            indice_fin=meses.index(month_fin)+1

        rango= meses[indice_in:indice_fin]
        return(rango,year_init,day_init,day_fin) 

    except:
        print('Error, no se encontraron fechas disponibles')

def days(rango,year,day_init,day_fin):
    RES = {}
    days=[]
    i=1
    num_meses=len(rango)
    meses=rango
    #print(meses)
    #print(num_meses)
    try:
        for rang in rango:
            #print(i)
            ruta = f'{ALEJ}/{year}/{rang}/*/'
            fechas = glob.glob(ruta)
            dias=[]
            aux_dias=[]

            if  i==1 and num_meses!=1:  
                i=i+ 1
                for fecha in fechas:
                    dia = int(re.findall('[0-9]+',fecha)[3])#Cambiar con respecto a la ruta #alejandro 3 nazario 2
                    dias.append(dia)
                    dias.sort()
                    if day_init in dias:
                        indice_init=dias.index(day_init)
                x=dias[indice_init:]
                aux_dias=(x)
                days.append(aux_dias)
                RES.update({rang:aux_dias})

            elif  i==num_meses:  
                for fecha in fechas:
                    dia = int(re.findall('[0-9]+',fecha)[2])
                    dias.append(dia)
                    dias.sort()

                    if day_init in dias and i==num_meses:
                        indice_init=dias.index(day_init)
                    else:
                        indice_init=0

                    if day_fin in dias:
                        indice_fin=dias.index(day_fin)+1

                z=dias[indice_init:indice_fin]
                aux_dias=(z)
                days.append(aux_dias)
                RES.update({rang:aux_dias})
                #print(days)

            else:
                i=i+ 1
                for fecha in fechas:
                    dia = int(re.findall('[0-9]+',fecha)[3])#alejandro 3 nazario 2
                    aux_dias.append(dia)
                    aux_dias.sort() 
                days.append(aux_dias)
            RES.update({rang:aux_dias})

        return days,RES
    
            
    except:
     print('No hay fechas') 

#fecha_inicial = '2021-8-6'
fecha_inicial = '2021-8-29'
fecha_final = '2021-10-8'

y=months(fecha_inicial,fecha_final)
d, RES=days(y[0],y[1],y[2],y[3])
print(RES)
######

def array_raster(ruta, bands, year, mes, dia):
    image = {}
    path = Path(ruta)
    try:
        for band in bands:
            file = Path(path,f'{year}/{mes}/{dia}/T14QKG/{band}.TIF')
            print(f'Opening file {file}')
            ds = rio.open(file)
            image.update({band: ds.read(1).astype(np.float32)})
        return image
    except:
        print('No se encontraron acrchivos')


def salida(FECHA_INICIAL, FECHA_FINAL):
    fecha_I = FECHA_INICIAL
    fecha_F = FECHA_FINAL
    MESES = months(fecha_I, fecha_F)
    d = days(MESES.meses, MESES.año, MESES.inicio)
   # print('Dias ',d)

#RES = salida(fecha_inicial, fecha_final)

ruta = NAZ

#RES = array_raster(ruta,['B11'], '2021', '12', '5')
#print(type(RES['B11']))
#print(RES.shape)
#calc_histograma(RES['B11'],1)



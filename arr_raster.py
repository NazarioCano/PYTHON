import numpy as np
import rasterio as rio
import glob
import re
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from constants import ALEJANDRO, BANDS, PRODUCTS
from matplotlib import pyplot as plt
from pathlib import Path

#ruta = '/Users/nazariocano/Desktop/PYTHON'
#RES = load_landsat_image(ruta,['BO3'], '2021', '12', '5')

def months(inicial,final):
    fecha_init=re.findall('([A-Z0-9]{1,4})',inicial)
    year_init=int(fecha_init[0])
    month_init=int(fecha_init[1])
    day_init=int(fecha_init[2])

    fecha_fin=re.findall('([A-Z0-9]{1,4})',final)
    year_fin=int(fecha_fin[0])
    month_fin=int(fecha_fin[1])
    day_fin=int(fecha_fin[2])

    ruta = f'C:/Users/PC/S10/{year_init}/*/'
    fechas = glob.glob(ruta)
    meses=[]
    
    try:
        for fecha in fechas:
            mes = int(re.findall('[0-9]+',fecha)[2])
            meses.append(mes)
            meses.sort()

        if month_init in meses:
            indice_in=meses.index(month_init)

        if month_fin in meses:
            indice_fin=meses.index(month_fin)+1

        rango= meses[indice_in:indice_fin]   
        return(rango,year_init,day_init) 

    except:
        print('Error, no se encontraron fechas disponibles')

def days(rango,year,day_init):
    #print(rango,year,day_init)
    i=0
    num_meses=len(rango)
    #print(num_meses)
    try:
        for rang in rango:
            #print(rang)
            ruta = f'C:/Users/PC/S10/{year}/{rang}/*/'
            fechas = glob.glob(ruta)
            dias=[]
            aux_dias=[]
            if  i==0:  
                i=i+ 1
                #print('Entro al if')                      
                for fecha in fechas:
                    dia = int(re.findall('[0-9]+',fecha)[3])
                    dias.append(dia)
                    dias.sort()
                    if day_init in dias:
                        indice=dias.index(day_init)
                        #print(indice)
                x=dias[indice:]
                aux_dias=(x)
                #dias.sort()
                #print(aux_dias)

                    #f.update({rang:dias})                
            else:
                #print('Entro al else')
                for fecha in fechas:
                    dia = int(re.findall('[0-9]+',fecha)[3])
                    aux_dias.append(dia)
                    aux_dias.sort() 
                #print(aux_dias)

            print(aux_dias)

            
            #print(i)
    except:
     print('No hay fechas') 


mes_inicial=12
mes_final=12
fecha_inicial='2021-5-15'
fecha_final='2021-9-1'



y=months(fecha_inicial,fecha_final)
d=days(y[0],y[1],y[2])
print(d)
######
"""
dia=days(months(mes_inicial,mes_final))
year=2021
mes=12
path=ALEJANDRO
banda=['B03']
"""

def load_landsat_image(ruta, bands, year, mes, dia):
    image = {}
    path = Path(ruta)
    for band in bands:
        file = Path(path,f'{year}/{mes}/{dia}/T14QKG/{band}.TIF')
 #       print(f'Opening file {file}')
        ds = rio.open(file)
        image.update({band: ds.read(1)})
    return image
#RES=load_landsat_image(path,['B03','B05'],'2021','12','5')
#print(RES)
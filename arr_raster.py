from constants import ALEJ, NAZ
#from example_rasterio import calc_histograma
import numpy as np
import rasterio as rio
import glob
import re
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from matplotlib import pyplot as plt
from pathlib import Path
import os



def months(inicial,final,ruta, producto):
    fecha_init=re.findall('([A-Z0-9]{1,4})',inicial)
    year_init=int(fecha_init[0])
    month_init=int(fecha_init[1])
    day_init=int(fecha_init[2])

    fecha_fin=re.findall('([A-Z0-9]{1,4})',final)
    year_fin=int(fecha_fin[0])
    month_fin=int(fecha_fin[1])
    day_fin=int(fecha_fin[2])
    
    ruta = f'{ruta}/{producto}/{year_init}/*/'
    fechas = glob.glob(ruta)
    meses=[]
    try:
        for fecha in fechas:
            mes = int(re.findall('[0-9]+',fecha)[2])#Checar las rutas que contengan numeros #alejandro 2 nazario 1
            meses.append(mes)  #Se agregan los meses
            meses.sort()
        if month_init not in meses:
            for mes in meses:
                if mes > month_init:
                    month_init=mes
                    day_init=0
                    break


        if month_init in meses:
            indice_in=meses.index(month_init)

        if month_fin in meses:
            indice_fin=meses.index(month_fin)+1

        rango= meses[indice_in:indice_fin]
        return(rango,year_init,day_init,day_fin) 

    except TypeError as err:
        print('Error, ',  err)

def days(rango,year,day_init,day_fin,ruta, producto):
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
            ruta2 = f'{ruta}/{producto}/{year}/{rang}/*/'
            fechas = glob.glob(ruta2)
            print(fechas)
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

                if day_init not in dias:
                    for dia in dias:
                        if dia > day_init:
                            day_init=dia
                            #print(day_init)
                            break
                    if day_init in dias:
                        indice_init=dias.index(day_init)

 
               # print(day_fin)
   
                #print(day_init)        
                x=dias[indice_init:]
                aux_dias=(x)
                days.append(aux_dias)
                RES.update({rang:aux_dias})

            elif  i==num_meses:  
                for fecha in fechas:
                    dia = int(re.findall('[0-9]+',fecha)[3])
                    dias.append(dia)
                    dias.sort()
                #print(day_init)


              

                if day_fin in dias:
                    indice_fin=dias.index(day_fin)
                    print('Dia final', indice_fin)
                
                if day_init in dias:
                   indice_init=dias.index(day_init)-1
                   print('Dia inicial', indice_init)


                if day_init not in dias and i==num_meses:
                    print('No entro', day_init)
                    for dia in dias:
                        if dia > day_init:
                            day_init=dia
                            print(day_init)
                            break
                    if day_init in dias:
                        indice_init=dias.index(day_init)
 
                #if day_fin not in dias:
                 #   for diaf in dias:
                  #      if diaf > day_fin:
                   #         day_fin=diaf
                            #print(day_fin)
                            
                    #        break
                    #if day_fin in dias :
                     #   indice_fin=dias.index(day_fin)-1
                      #  indice_init=dias.index(day_init)-num_meses

                z=dias[indice_init:]
                aux_dias=(z)
                days.append(aux_dias)
                RES.update({rang:aux_dias})

            else:
                i=i+ 1
                for fecha in fechas:
                    dia = int(re.findall('[0-9]+',fecha)[3])#alejandro 3 nazario 2
                    aux_dias.append(dia)
                    aux_dias.sort() 
                days.append(aux_dias)
                #print(aux_dias)
            RES.update({rang:aux_dias})

        return RES
    
            
    except TypeError as err:
     print('Error ', err) 

#fecha_inicial = '2021-8-6'
fecha_inicial = '2021-10-14'
fecha_final = '2021-12-30'

#y = months(fecha_inicial,fecha_final)
#d, RES = days(y[0],y[1],y[2],y[3])



def array_raster(ruta, filtro, year, mes, dias, coordenadas, producto ):
    image = {}
    path = Path(ruta)
    try:
        for dia in dias:
            file = Path(path,f'{producto}/{year}/{mes}/{dia}/{filtro}.tif')
            print(f'Opening file {file}')
            ds = rio.open(file)  #Abrimos el archivo
            #RECORTE
            recorte, Transform = mask(ds, [coordenadas], crop = True, all_touched=True)
            image.update({dia: recorte})
        return image
    except TypeError as err:
        print('Error ', err)


def salida(FECHA_INICIAL, FECHA_FINAL, coord, producto, filtro):
    ruta = NAZ
    fecha_I = FECHA_INICIAL
    fecha_F = FECHA_FINAL
    try: 
        meses = months(fecha_I, fecha_F,ruta, producto)
        for mes in meses[0]:
            d = days(meses[0],meses[1],meses[2],meses[3],ruta, producto)
            print('Ruta:', ruta)
            print('Filtro:', filtro)
            print('Año:', meses[1])
            print('Mes', mes)
            print('Dias', d[mes])
            ArrayR = array_raster(ruta,filtro,meses[1],mes,d[mes], coord,producto)
        return ArrayR
    except TypeError as err:
        print('Error,',err)




#RES = salida(fecha_inicial, fecha_final)
#print('Salida:', RES)


#RES = array_raster(ruta,['B11'], '2021', '12', '5')
#print(type(RES['B11']))
#print(RES.shape)
#calc_histograma(RES['B11'],1)



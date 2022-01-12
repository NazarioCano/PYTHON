import numpy as np
import rasterio as rio
import glob
import re
from rasterio.plot import show_hist, show
from rasterio.mask import mask
from constants import BANDS, PRODUCTS
from matplotlib import pyplot as plt
from pathlib import Path








def load_landsat_image(ruta, bands, year, mes, dia):
    image = {}
    path = Path(ruta)
    for band in bands:
        file = Path(path,f'{year}/{mes}/{dia}/T14QKG/{band}.TIF')
        print(f'Opening file {file}')
        ds = rio.open(file)
        #image.update({band: ds.read(1)})
    return image

ruta = '/Users/nazariocano/Desktop/PYTHON'

#RES = load_landsat_image(ruta,['BO3'], '2021', '12', '5')
rio.open('/Users/nazariocano/Desktop/2021/12/5/T14QKG/BO3.TIF')

mes_inicial=10
mes_final=12

def months(inicial,final):
    ruta = 'C:/Users/PC/S10/2021/*/'
    fechas = glob.glob(ruta)
    meses=[]
    try:
        for fecha in fechas:
            mes = int(re.findall('[0-9]+',fecha)[2])
            meses.append(mes)
            meses.sort()
            #print(mes)

        if inicial in meses:
            indice_in=meses.index(inicial)
        if final in meses:
            indice_fin=meses.index(final)+1

        rango= meses[indice_in:indice_fin]   
        return(rango) 
    except:
        print('Error')

def days(rangos):
    try:
        for rango in rangos:
            ruta = f'C:/Users/PC/S10/2021/{rango}/*/'
            fechas = glob.glob(ruta)
            dias=[]
            
            for fecha in fechas:
                dia = int(re.findall('[0-9]+',fecha)[3])
                dias.append(dia)
                dias.sort()
            print (dias)    
    except:
        print('No hay fechas') 


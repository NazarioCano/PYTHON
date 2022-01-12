#CRECION DE HISTOGRAMAS DE IMGENES SATELITALES 0.01

import cv2  #IMPORTACION DE LA LIBRERIA DE CV2, Numpy y Matplotlib
import numpy as np 
from matplotlib import pyplot as plt



img = cv2.imread('B01.tif')  #IMAGEN DE PRUEBA
MAX = np.amax(img)
print('Max:',MAX )
MIN = np.amin(img)
print('Min:', MIN)

#CALCULO DE HISTOGRAMA CON CV2
#<------------------imagen---canal----mask-----Size------range---->
hist = cv2.calcHist( [img],   [0],    None,   [MAX],    [MIN, MAX])  


#FUGURAS
fig , ax = plt.subplots(1,2)

ax[0].imshow(img, cmap = 'gray')
ax[0].set_title('Rosa')
ax[0].axis('off')

ax[1].plot(hist, color = 'gray')
ax[1].set_title('OPEN CV2')

#ax[1,0].imshow(img, cmap = 'gray')
#ax[1,0].set_title('Rosa')
#ax[1,0].axis('off')

#ax[1,1].hist(img.ravel(), 256, [0,256])  #SEGINDO METODO DE HISTOGRAMA DE MATPLOTLIB
#ax[1,1].set_title('CON MATPLOTLIB')

plt.show()  #VER GRAFICAS

#u, th = cv2.threshold(img, 127,255, cv2.THRESH_BINARY)
#cv2.imshow('img', th)
cv2.waitKey(0)
cv2.destroyAllWindows()
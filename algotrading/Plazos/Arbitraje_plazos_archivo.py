# By Francisco Cucullu

import FuncionesFrancisco as FF
import pandas as pd

#Detecto dia
(DIA, MES, ANO) = FF.DetectaDia()
#Ruta del CSV
path = "Y:\\Git\\Data\\Algotrades\\Plazos\\"+ANO+MES+DIA+".csv"

#Creo el cvs incialcon el nombre de las filas correspondiente a los datos que scrapeo
tabla = pd.DataFrame(columns=['Hora','# Trade','Ticker','C/V','Plazo','Cantidad',
                                   'Precio','Monto','TNA','Caucion','Calzada?','Deteccion'])

tabla.to_csv(path, index=False, sep=';', decimal=',')  

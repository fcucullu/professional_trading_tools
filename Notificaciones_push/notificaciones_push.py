import sys
sys.path.append(r'Y:\Git\Funciones')
sys.path.append(r'Y:\Git\algotrading\API')
import FuncionesFrancisco as FF #Funciones varias
from funcionesAPI import Requests  #APIS 
requests = Requests()
import pandas as pd
import datetime


###############################################################################
'''                LEVANTO LOS TICKERS DEL PANEL LIDER                     '''
###############################################################################
csv_input = r'Y:\Git\Notificaciones_push\panel_lider.csv'
csv = pd.read_csv(csv_input, sep=';', decimal=',')

###############################################################################
'''                LOOP PARA OBTENER INFO HISTORICA                       '''
###############################################################################
fechaHasta, fechaDesde = FF.DeltaDateAyer(90) #Esta funcion me trae datos desde ayer hasta X dias atras

#Creo una pandas.DataFrame con todas las fechas como index
#Me interesa tener tambien los fines de semana para tener visibles los dias de la semana
#y analizar cuando mas se opera.
tabla = pd.DataFrame(index=[pd.date_range(fechaDesde, fechaHasta)])




tabla['GGAL'] = PanelLider_pd['Especie'].map(cant)
   


#Inicio loop que buscará los datos historicos de todos los tickers en el CSV
#calculara sus promedios y creará una tabla nueva solo con ellos.
for row in range(len(csv)):
    serie = requests.serie_diaria(csv.iloc[row][0], fechaDesde, fechaHasta)
    
    
    




   
    
    
    
    for i in range(len(serie)):
        'tab_' + ticker = serie.append({'Fecha': serie[i]['fechaHora'][0:10], 'Volumen': serie[i]['volumenNominal']}, ignore_index=True)
prom = pd.DataFrame({'Fecha': 'Promedio', 'Volumen': int(tab['Volumen'].mean())}, index=[0])
tab = pd.concat([prom, tab]).reset_index(drop = True) 

b = requests.cotizacion('GGAL', 'BCBA', 't2')['volumenNominal']

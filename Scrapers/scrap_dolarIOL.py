# By Francisco Cucullu

import sys
sys.path.append(r'Y:\Git\Funciones')
sys.path.append(r'Y:\Git\Scrapers')
import FuncionesFrancisco as FF
import csv
import pandas as pd
import traceback
import requests
from bs4 import BeautifulSoup as bs


##############################################################################
'''                 Funcion para crear archivo CSV                       '''
##############################################################################

def crea_csv_dolarIOL():

    #Detecto dia
    (DIA, MES, ANO) = FF.DetectaDia()
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_IOL.csv"
    #Creo el cvs incial con el nombre de las filas correspondiente a los datos que scrapeo
    with open(path, 'w', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        filewriter.writerow(['Horario','Compra','Venta'])

    return    
    
##############################################################################
'''                 Funcion para alimentar archivo CSV                    '''
##############################################################################


def escribe_dolarIOL():
    
    #Detecto dia y horario
    (DIA, MES, ANO) = FF.DetectaDia()
    horario = FF.DetectaHorario()
    
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_IOL.csv"
    
    try:
        #Scrap del Dolar IOL
        r = requests.get('https://dolar.invertironline.com/')
        soup = bs(r.content, 'xml')
        dolarC = soup.find(class_="precio-compra").text
        dolarC = float(dolarC.replace(',','.'))
        dolarV = soup.find(class_="precio-venta").text
        dolarV = float(dolarV.replace(',','.'))
     
        #Paso a armar los CSV para el historico
        csv_input = pd.read_csv(path, sep=';', decimal=',')
        csv_input = csv_input.append({'Horario': horario,
                                      'Compra': dolarC,
                                      'Venta': dolarV}, ignore_index=True)
        csv_input.to_csv(path, index=False, sep=';', decimal=',')
        print('DOLAR IOL: {}-{}'.format(dolarC, dolarV))
        
    except:
        print('Problema en actualizar DOLAR IOL las {}'.format(horario))
        traceback.print_exc()
        pass
    
    return
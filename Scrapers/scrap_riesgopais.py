# By Martin Dvorkin

import sys
sys.path.append(r'Y:\Git\algotrading\API')
sys.path.append(r'Y:\Git\Funciones')
import FuncionesFrancisco as FF
import csv
import pandas as pd
import traceback
import requests
from bs4 import BeautifulSoup as bs

##############################################################################
'''                 Funcion para crear archivo CSV                       '''
##############################################################################

def crea_csv_riesgopais():

    #Detecto dia
    (DIA, MES, ANO) = FF.DetectaDia()
    #Ruta del CSV
    path2 = "Y:\\Git\\Data\\RiesgoPais\\"+ANO+MES+DIA+".csv"
    #Creo el cvs incial con el nombre de las filas correspondiente a los datos que scrapeo
    with open(path2, 'w', newline="") as csvfile:
        filewriter2 = csv.writer(csvfile, delimiter=';')
        filewriter2.writerow(['Horario','Precio'])
    csvfile.close()
    
    return 

##############################################################################
'''                 Funcion para alimentar archivo CSV                    '''
##############################################################################

def escribe_riesgopais():
    
    #Detecto dia y horario
    (DIA, MES, ANO) = FF.DetectaDia()
    horario = FF.DetectaHorario()
    
    #Ruta del CSV
    path2 = "Y:\\Git\\Data\\RiesgoPais\\"+ANO+MES+DIA+".csv"
    
    try:
        #Scrap del RiesgoPais
        r2 = requests.get('https://www.rava.com/empresas/perfil.php?e=RIESGO%20PAIS')
        soup2 = bs(r2.content, 'lxml')
        riesgopais = soup2.select_one('.fontsize6').text                 
    
        #Escribe el Riesgo Pais
        csv_input2 = pd.read_csv(path2, sep=';', decimal=',')
        csv_input2 = csv_input2.append({'Horario': horario,
                                      'Precio': riesgopais}, ignore_index=True)
        csv_input2.to_csv(path2, index=False, sep=';', decimal=',')
        print('RIESGO PAIS a {}'.format(riesgopais))
        
    except:
        print('Problema en actualizar RIESGO PAIS las {}'.format(horario))
        traceback.print_exc()
        pass
    
    return

##############################################################################
'''                        Funcion para printear                          '''
##############################################################################

def print_riesgopais():
   
    try:
        #Scrap del RiesgoPais
        r2 = requests.get('https://www.rava.com/empresas/perfil.php?e=RIESGO%20PAIS')
        soup2 = bs(r2.content, 'lxml')
        riesgopais = soup2.select_one('.fontsize6').text       
        var = soup2.select_one('.fontsize3').text             
    except:
        riesgopais = 'ERROR'
        var = 'ERROR'

    return riesgopais, var

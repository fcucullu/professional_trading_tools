# By Francisco Cucullu

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

def crea_csv_dolarMAE():
    #Detecto dia
    (DIA, MES, ANO) = FF.DetectaDia()
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_MAE.csv"
    #Creo el cvs incial con el nombre de las filas correspondiente a los datos que scrapeo
    with open(path, 'w', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        filewriter.writerow(['Horario','Precio'])

    return    
    
##############################################################################
'''                 Funcion para alimentar archivo CSV                    '''
##############################################################################

def escribe_dolarMAE():
    #Detecto dia y horario
    (DIA, MES, ANO) = FF.DetectaDia()
    horario = FF.DetectaHorario()
    
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_MAE.csv"
    
    try:
        try:
            #Scrap del Dolar MAE
            r = requests.get('http://www.mae.com.ar/')
            soup = bs(r.content, 'lxml')
            dolar = soup.find_all('div', class_="col-md-3 col-sm-12 col-xs-12")[3].get_text().strip()
             
            #Trabajo la data para imprimir correctamente el Dolar MAE (precio por un lado, % por el otro)              
            dolar2=dolar.split("$")[2]       
            porcentajedolar=dolar2[-6:]+'%'
            preciodolar= dolar2[1:7]     
            subedolar=porcentajedolar[:1]
            if subedolar=="0":
                porcentajedolar="+"+porcentajedolar[1:]
        
        #Por que a veces cotiza el "USMEP000T"  
        except:
            r = requests.get('http://www.mae.com.ar/')
            soup = bs(r.content, 'lxml')
            dolar = soup.find_all('div', class_="col-md-3 col-sm-12 col-xs-12")[3].get_text().strip()
             
            #Trabajo la data para imprimir correctamente el Dolar MAE (precio por un lado, % por el otro)              
            dolar2=dolar.split("$")[1]       
            porcentajedolar=dolar2[-6:]+'%'
            preciodolar= dolar2[1:7]     
            subedolar=porcentajedolar[:1]
            if subedolar=="0":
                porcentajedolar="+"+porcentajedolar[1:]
                
        #Paso a armar los CSV para el historico
        #Escribe el Dolar MAE
        csv_input = pd.read_csv(path, sep=';', decimal=',')
        csv_input = csv_input.append({'Horario': horario,
                                      'Precio': preciodolar}, ignore_index=True)
        csv_input.to_csv(path, index=False, sep=';', decimal=',')
        print('DOLAR MAE a ${}'.format(preciodolar))
        
    except:
        print('Problema en actualizar DOLAR MAE las {}'.format(horario))
        traceback.print_exc()
        pass
    
    return
      
##############################################################################
'''                          Funcion para printear                        '''
##############################################################################

def print_dolarMAE():

    try:
        try:
            #Scrap del Dolar MAE
            r = requests.get('http://www.mae.com.ar/')
            soup = bs(r.content, 'lxml')
            dolar = soup.find_all('div', class_="col-md-3 col-sm-12 col-xs-12")[3].get_text().strip()
             
            #Trabajo la data para imprimir correctamente el Dolar MAE (precio por un lado, % por el otro)              
            dolar2=dolar.split("$")[2]       
            porcentajedolar=dolar2[-6:]+'%'
            preciodolar= dolar2[1:7]     
            subedolar=porcentajedolar[:1]
            if subedolar=="0":
                porcentajedolar="+"+porcentajedolar[1:]
        
        #Por que a veces cotiza el "USMEP000T"
        except:
            r = requests.get('http://www.mae.com.ar/')
            soup = bs(r.content, 'lxml')
            dolar = soup.find_all('div', class_="col-md-3 col-sm-12 col-xs-12")[3].get_text().strip()
             
            #Trabajo la data para imprimir correctamente el Dolar MAE (precio por un lado, % por el otro)              
            dolar2=dolar.split("$")[1]       
            porcentajedolar=dolar2[-6:]+'%'
            preciodolar= dolar2[1:7]     
            subedolar=porcentajedolar[:1]
            if subedolar=="0":
                porcentajedolar="+"+porcentajedolar[1:]
 
    except:
        preciodolar = 'ERROR'
        porcentajedolar = 'ERROR'
        

    return preciodolar, porcentajedolar



import eikon as ek
ek.set_app_key('0893175a10224620a7ad8f348be81b2e7a26d498')
def reuters_mae():
    #Para ir por scraper
    '''
    mae, a = dolarMAE.print_dolarMAE()
    mae_compra, mae_venta = round(float(mae.replace(',','.')),2), round(float(mae.replace(',','.')),2)
    mae_spread = mae_venta - mae_compra
    '''
    #Para ir por reuters
    try:
        df, err = ek.get_data('USTARTSD1=ME',
                          ['CF_LAST',
                          'PRIMACT_1',
                           'SEC_ACT_1'])
        return df['PRIMACT_1'].item(), df['SEC_ACT_1'].item(), df['CF_LAST'].item()
    except:
        return 0,0,0
    
  
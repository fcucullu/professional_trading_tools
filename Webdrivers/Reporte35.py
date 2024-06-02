# By Francisco Cucullu

import sys
sys.path.append(r'Y:\Git\Funciones')
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import FuncionesFrancisco as FF #Funciones varias
import csv
import traceback

##############################################################################
'''                 Funcion para crear archivo CSV                       '''
##############################################################################

def crea_csv_dolarSUPV():
    #Detecto dia
    (DIA, MES, ANO) = FF.DetectaDia()
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_SUPV.csv"
    #Creo el cvs incial con el nombre de las filas correspondiente a los datos que scrapeo
    with open(path, 'w', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        filewriter.writerow(['Horario','Compra','Venta'])

    return    

##############################################################################
'''                 Funcion para alimentar archivo CSV                    '''
##############################################################################

def escribe_dolarSUPV():
    #Inputs
    (DIA, MES, ANO) = FF.DetectaDia()
    horario = FF.DetectaHorario()
    fecha_hasta = FF.DeltaDateAyer(-2)[1]
    fecha_deste = FF.DeltaDateAyer(10)[1]
    desde = str(fecha_deste[8:10]+'/'+fecha_deste[5:7]+'/'+fecha_deste[0:4])
    hasta = str(fecha_hasta[8:10]+'/'+fecha_hasta[5:7]+'/'+fecha_hasta[0:4])
    credenciales = {'TUserName': 'fcucullu', 
               'tpassword': 'Fran2020'}
    headers = {'Llamar': '1',
           'MostrarConsulta': '',
           'Id_Moneda': '2',
           'FechaDesde': desde,
           'FechaHasta': hasta,
           'ID_TipoDolar': '47',
           'Solo_Cierre': '0',
           'TExportar': '0'}
    
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_SUPV.csv"
    
    try:
        #Tiro la request para la informacion de IOLNET
        session = requests.Session()
        request = session.post('http://iolnet.invertir.local/login.asp', data=credenciales)
        #print(session.cookies.get_dict())
        cookies = session.cookies.get_dict()
        response = session.post('http://iolnet.invertir.local/reportes/VerReporte.asp?ID_Reporte=35', data=headers, cookies=cookies)
        
        #Parseo la response
        soup = bs(response.content, 'lxml')        
        soup
        
        #Creo la Tabla y trabajo la info
        columnas = 3
        l = []
        for tr in soup:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            for i in range(len(row)):
                row[i] = row[i].replace('\n','')
                row[i] = row[i].replace('\t','')
                row[i] = row[i].replace('\r','')
            row = row[row.index('NingunoExcelPDF')+1:len(row)]
            l.append(row)
        reporte = pd.DataFrame(l)
        
        #Trabajo la inforacion para que sea como en IOLNet
        filas = int(len(reporte.columns) / columnas)
        reporte = pd.DataFrame(reporte.values.reshape(filas,columnas))
        reporte.columns = reporte.iloc[0]
        reporte = reporte.drop(0, axis=0)
        
        #Extraigo los ultimos valores de la tabla y los transformo en float
        compra = pd.to_numeric(reporte.iloc[0,1][2:].replace(',','.'))
        venta = pd.to_numeric(reporte.iloc[0,2][2:].replace(',','.'))
        
        #Paso a armar los CSV para el historico
        csv_input = pd.read_csv(path, sep=';', decimal=',')
        csv_input = csv_input.append({'Horario': horario,
                                      'Compra': compra,
                                      'Venta': venta}, ignore_index=True)
        csv_input.to_csv(path, index=False, sep=';', decimal=',')
        print('DOLAR SUPV: {}-{}'.format(compra,venta))
    
    except:
        print('Problema en actualizar DOLAR SUPV a las {}'.format(horario))
        traceback.print_exc()
        pass
    
    return


##############################################################################
'''                          Funcion para printear                        '''
##############################################################################

def print_dolarSUPV():

    #Veo cual fue el cierre de ayer para el % de variacion diaria
    for i in range(1,10):
        try:
            archivo = FF.DeltaDateHoy(i)[1].replace('-','')+'_SUPV.csv'
            path = "Y:\\Git\\Data\\Dolar\\" + archivo
            csv_input = pd.read_csv(path, sep=';', decimal=',')
            lastC = csv_input.iloc[-1,1]
            lastV = csv_input.iloc[-1,2]
            break
        except FileNotFoundError:
            continue
    
    try:
        fecha_hasta = FF.DeltaDateAyer(-2)[1]
        fecha_deste = FF.DeltaDateAyer(10)[1]
        desde = str(fecha_deste[8:10]+'/'+fecha_deste[5:7]+'/'+fecha_deste[0:4])
        hasta = str(fecha_hasta[8:10]+'/'+fecha_hasta[5:7]+'/'+fecha_hasta[0:4])
        credenciales = {'TUserName': 'fcucullu', 
                        'tpassword': 'Fran2020'}
        headers = {'Llamar': '1',
                   'MostrarConsulta': '',
                   'Id_Moneda': '2',
                   'FechaDesde': desde,
                   'FechaHasta': hasta,
                   'ID_TipoDolar': '47',
                   'Solo_Cierre': '0',
                   'TExportar': '0'}
       
        #Tiro la request para la informacion de IOLNET
        session = requests.Session()
        request = session.post('http://iolnet.invertir.local/login.asp', data=credenciales)
        #print(session.cookies.get_dict())
        cookies = session.cookies.get_dict()
        response = session.post('http://iolnet.invertir.local/reportes/VerReporte.asp?ID_Reporte=35', data=headers, cookies=cookies)
        
        #Parseo la response
        soup = bs(response.content, 'lxml')        
        #soup
        
        #Creo la Tabla y trabajo la info
        columnas = 3
        l = []
        for tr in soup:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            for i in range(len(row)):
                row[i] = row[i].replace('\n','')
                row[i] = row[i].replace('\t','')
                row[i] = row[i].replace('\r','')
            row = row[row.index('NingunoExcelPDF')+1:len(row)]
            l.append(row)
        reporte = pd.DataFrame(l)
        
        #Trabajo la inforacion para que sea como en IOLNet
        filas = int(len(reporte.columns) / columnas)
        reporte = pd.DataFrame(reporte.values.reshape(filas,columnas))
        reporte.columns = reporte.iloc[0] #Pongo la primer fila como encabezado
        reporte = reporte.drop(0, axis=0) #Borro la antigua primer linea
        
        #Extraigo los ultimos valores de la tabla y los transformo en float
        compra = pd.to_numeric(reporte.iloc[0,1][2:].replace(',','.'))
        venta = pd.to_numeric(reporte.iloc[0,2][2:].replace(',','.'))
        
        porcentajecompra = '+'+str(round((compra/lastC-1)*100,2))+'%' if round((compra/lastC-1)*100,2)>0 else '-'+str(round((compra/lastC-1)*100,2))+'%'
        porcentajeventa = '+'+str(round((venta/lastV-1)*100,2))+'%' if round((venta/lastV-1)*100,2)>0 else '-'+str(round((venta/lastV-1)*100,2))+'%'

    except:
        compra = 'ERROR'
        venta = 'ERROR'
        porcentajecompra = 'ERROR'
        porcentajeventa = 'ERROR'
        

    return compra, venta, porcentajecompra, porcentajeventa




##############################################################################
'''                          Funcion para Arbitradores                        '''
##############################################################################

def dolarSUPV_arbitraje(PsupvC, PsupvV):

    
    try:
        fecha_hasta = FF.DeltaDateAyer(-2)[1]
        fecha_deste = FF.DeltaDateAyer(10)[1]
        desde = str(fecha_deste[8:10]+'/'+fecha_deste[5:7]+'/'+fecha_deste[0:4])
        hasta = str(fecha_hasta[8:10]+'/'+fecha_hasta[5:7]+'/'+fecha_hasta[0:4])
        credenciales = {'TUserName': 'fcucullu', 
                        'tpassword': 'Fran2020'}
        headers = {'Llamar': '1',
                   'MostrarConsulta': '',
                   'Id_Moneda': '2',
                   'FechaDesde': desde,
                   'FechaHasta': hasta,
                   'ID_TipoDolar': '47',
                   'Solo_Cierre': '0',
                   'TExportar': '0'}
       
        #Tiro la request para la informacion de IOLNET
        session = requests.Session()
        request = session.post('http://iolnet.invertir.local/login.asp', data=credenciales)
        #print(session.cookies.get_dict())
        cookies = session.cookies.get_dict()
        response = session.post('http://iolnet.invertir.local/reportes/VerReporte.asp?ID_Reporte=35', data=headers, cookies=cookies)
        
        #Parseo la response
        soup = bs(response.content, 'lxml')        
        
        #Creo la Tabla y trabajo la info
        columnas = 3
        l = []
        for tr in soup:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            for i in range(len(row)):
                row[i] = row[i].replace('\n','')
                row[i] = row[i].replace('\t','')
                row[i] = row[i].replace('\r','')
            row = row[row.index('NingunoExcelPDF')+1:len(row)]
            l.append(row)
        reporte = pd.DataFrame(l)
        
        #Trabajo la inforacion para que sea como en IOLNet
        filas = int(len(reporte.columns) / columnas)
        reporte = pd.DataFrame(reporte.values.reshape(filas,columnas))
        reporte.columns = reporte.iloc[0] #Pongo la primer fila como encabezado
        reporte = reporte.drop(0, axis=0) #Borro la antigua primer linea
        
        #Extraigo los ultimos valores de la tabla y los transformo en float
        compra = pd.to_numeric(reporte.iloc[0,1][2:].replace(',','.'))
        venta = pd.to_numeric(reporte.iloc[0,2][2:].replace(',','.'))
        
    except:
        compra = 0
        venta = 0        
        
    PsupvC.value = compra
    PsupvV.value = venta
        
    return







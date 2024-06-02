# By Francisco Cucullu

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import ExcelWriter
from datetime import datetime, timedelta

def reporte90(fecha):
    # Hago la consulta a IOLNet    
    AAA = {'TUserName': 'automatizacioncucu', 
           'tpassword': 'jackperro02'}
    BBB = {'Llamar': '1',
           'MostrarConsulta': '',
           'fecha': fecha,
           'ID_Tipo_Cuenta': '1',
           'TExportar': '1'}
    session = requests.Session()
    session.post('http://iolnet.invertir.local/login.asp', data=AAA)
    #print(session.cookies.get_dict())
    cookies = session.cookies.get_dict()
    response = session.post('http://iolnet.invertir.local/Reportes/VerReporte.asp?ID_Reporte=90', data=BBB, cookies=cookies)
    #Parseo la response
    soup = bs(response.content, 'lxml')        
    #Creo la Tabla
    columnas = 22
    l = []
    for tr in soup:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        for i in range(len(row)):
            row[i] = row[i].replace('\n','')
            row[i] = row[i].replace('\t','')
            row[i] = row[i].replace('\r','')
        for index, element in enumerate(row):
            try:
                row[index] = pd.to_numeric(element.replace('.','').replace(',','.'))
            except:
                pass
        l.append(row)
    reporte = pd.DataFrame(l)
    filas = int(len(reporte.columns) / columnas)
    reporte = pd.DataFrame(reporte.values.reshape(filas,columnas))
    reporte.columns = reporte.iloc[0]
    reporte = reporte.drop(0, axis=0)

    return reporte




def r90_adm(fecha_inicio, fecha_final):
    
    #Creo lista de fechas
    start = datetime.strptime(fecha_inicio, "%d/%m/%Y")
    stop = datetime.strptime(fecha_final, "%d/%m/%Y")
    fechas = []
    while start <= stop:
        fechas.append(start)
        start = start + timedelta(days=1)  # increase day one by one
    
    # Creo el workbook
    dire = 'C:\\Users\\fcucullu\\Downloads\\' + datetime.today().strftime('Análisis R90 - %Y%m%d') +'.xlsx'
    writer = ExcelWriter(dire, engine='xlsxwriter')
    for numero,fecha in enumerate(fechas):
        fecha = fecha.strftime('%d/%m/%Y')
        if numero == 0:
            reporteA = reporte90(fecha)
            reporteA.to_excel(writer, fecha.replace('/','-'), index=False, float_format = "%0.2f")
        else:
            reporteB = reporte90(fecha)
            if len(reporteB) < 10:
                pass
            else:
                # El reporte tiene datos, creo la solapa y la incluyo en el workbook
                # Pero antes de incluirla, hago los cruces
                reporteB = reporteB.merge(reporteA[['Nº de Cuenta', 'Total']], how='left', on='Nº de Cuenta', suffixes=('', '_t-1')).fillna(0)
                reporteB['Variación'] = reporteB['Total_t-1'] - reporteB['Saldo Inicial']

                
                
                reporteB.to_excel(writer, fecha.replace('/','-'), index=False, float_format = "%0.2f")
                reporteA = reporteB
                del reporteB
    
    writer.save()
    
    return

print('By Francisco Cucullu')
print('')
print('Ingrese la fecha inicial con formato DD/MM/AAAA: ')
fecha_inicio = input()

start = datetime.strptime(fecha_inicio, "%d/%m/%Y")
if (start.weekday() == 5) or (start.weekday() == 6):
    input('No se puede comenzar un fin de semana')
    quit()

print('Ingrese la fecha final con formato DD/MM/AAAA: ')
fecha_final = input()
print('\nEl proceso demorará algunos minutos.')
print('\nAguarde por favor =D.')

r90_adm(fecha_inicio, fecha_final)

input('\nAnálisis terminado con éxito!')

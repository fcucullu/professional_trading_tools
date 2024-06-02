# By Francisco Cucullu

import requests
from bs4 import BeautifulSoup as bs
import datetime
import pandas as pd


startDate = datetime.datetime(2019,5,2).strftime('%m/%d/%Y')
endDate = datetime.datetime(2019,5,2).strftime('%m/%d/%Y')

AAA = {'TUserName': 'fcucullu', 
           'tpassword': 'fran2020'}
BBB = {'Llamar': '1',
       'MostrarConsulta': '',
       'mercado': '54',
       'fechdesd': '06/05/2019',
       'fechhasta': '06/05/2019',
       'NumeCuen': '',
       'IncluirMM': '0',
       'ID_Contraparte': '0',
       'TExportar': '1'}

session = requests.Session()
request = session.post('http://iolnet.invertir.local/login.asp', data=AAA)
print(session.cookies.get_dict())
cookies = session.cookies.get_dict()
response = session.post('http://iolnet.invertir.local/Reportes/VerReporte.asp?ID_Reporte=104', data=BBB, cookies=cookies)

#Parseo la response
soup = bs(response.content, 'lxml')        
soup

#Creo la Tabla
columnas = 20
l = []
for tr in soup:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    for i in range(len(row)):
        row[i] = row[i].replace('\n','')
        row[i] = row[i].replace('\t','')
        row[i] = row[i].replace('\r','')
    l.append(row)
reporte = pd.DataFrame(l)

filas = int(len(reporte.columns) / columnas)
reporte = pd.DataFrame(reporte.values.reshape(filas,columnas))
reporte.columns = reporte.iloc[0]
reporte = reporte.drop(0, axis=0)














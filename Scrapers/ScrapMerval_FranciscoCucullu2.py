# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 22:39:37 2018

@author: Francisco Cucullu
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import xlsxwriter
import time
import matplotlib.pyplot as plt


graph = []
#DEfino funcion para graficar el índice a medida que se va actualizando
def grafico(graph):
    plt.plot(graph, linewidth = 2, color = 'orange')
    plt.legend(('Índice',), loc = 'upper left')
    plt.title('Gráfico del índice scrapeado')
    plt.xlabel('Tiempo')
    plt.ylabel('Precio')
    plt.show()


while True == True:
    ############################################################################
    print("\n1) Traer todos los componentes del Merval \n")
    
    #Parseo la pagina del Merval - Cotizaciones del panel lider
    URL='http://www.merval.sba.com.ar/Vistas/Cotizaciones/acciones.aspx'
    page=requests.get(URL)
    soup=BeautifulSoup(page.content, 'html.parser')
    td=soup.find_all('td', class_= ('txtGrisTabla_ConBorde', 'txtRojoTabla_ConBorde', 'txtVerdeTabla_ConBorde'))
    info=[info.get_text() for info in td]
    
    #Parseo los encabezados
    URL='http://www.merval.sba.com.ar/Vistas/Cotizaciones/acciones.aspx'
    page=requests.get(URL)
    soup=BeautifulSoup(page.content, 'html.parser')
    td=soup.find_all('td', class_= 'txtGrisTabla_ConBorde_ArribaYAbajo')
    encabezados=[info.get_text() for info in td]
    
    
    '''
    #Parseo la pagina del Merval - Composición del índice
    URL2='http://www.merval.sba.com.ar/Vistas/Cotizaciones/Indices.aspx?Panel=0'
    page2=requests.get(URL2)
    soup2=BeautifulSoup(page2.content, 'html.parser')
    td2=soup2.find_all('td', class_='celdaPanelTablaContenidoIndice')
    info2=[info2.get_text() for info2 in td2]
    
    La pagina no es muy amigable. Tiene tablas sin nombre, datos no-numericos
    y resulta imposible parserlo. Voy a plantear excepcionalmente unos 
    diccionarios con inputs manuales para poder sortear el problema. No me gusta
    esta solución, pero voy a priorizar la resolución del ejercicio.
    Con bolsar ocurre algo parecido. Las tablas tienen classes/ids muy random.
    Investing tiene la info muy ordenada y facil de parsear, pero bloquean los
    parsers...
    Merval, Bolsar, Reuters, Investing y IAMC no coinciden entre sí
    '''
    
    #Creo una list of list con la info de cotizaciones
    #Primero creo una lista vacía
    PanelLider=[]
    for i in range(len(info)//11):
        PanelLider.append([])
    #La completo con la info parseada en la sección de cotizaciones.
    for i in range(len(info)):
        x = i//11
        PanelLider[x].append(info[i])
    '''    
    for i in range(len(PanelLider)):
        PanelLider[i].append(float(PanelLider[i][6].replace(",","."))/float(PanelLider[i][2].replace(",","."))-1)
    
    Al final no es necesario! Le incluyo a la línea 22 las diferentes classes
    al parsing y ahora levanto las variaciones directamente, sin importar si 
    las variaciones son negativas, positivas o nulas (los programadores de la 
    pagina del merval le cambian los nombres segun sea el caso, muy prácticos.)
    '''
    
    #Transformo la información en un Pandas.DataFrame por que queda mas 
    #"ordenado" y por que luego será más facil pasarlo a un .xls .
    PanelLider_pd = pd.DataFrame(PanelLider)
    PanelLider_pd.columns = encabezados
    
    #Imprimo la tabla para finalizar el primer punto
    print(PanelLider_pd)
    
    ############################################################################
    
    print("\n\n ------------------------------------------------------------ \n")
    
    print("\n2) Calcular el valor Spot del Merval* \n")
    
    #Ante la dificultad de parsear la pagina del Merval y la de Bolsar,
    #me concentro en la resolución del problema plantenado diccionarios.
    #Propongo diccionarios y no listas/tuplas para poder mapear el key value
    #a la hora de incorporar la nueva información a la tabla evitando el
    #riesgo de mapeo incorrecto.
        
    #Los componentes del índice estan pésimos!! Gran error del mercado!!
    #No incluyen a TS y ponen solo 19 papeles.
    #No hay información confiable! Reuters tiene una ponderación, bolsar tiene
    #otra, la pagina del merval otra diferente a las anteriores...
    #Luego de pasar gran tiempo haciendo research, termino omitiendo este
    #GRAN detalle para concentrarme en el código.
        
    pond = {"ALUA": 0.035319,
            "APBR": 0.08497,
            "BMA": 0.076038,
            "BYMA": 0.059466,
            "CEPU": 0.052042,
            "COME": 0.01983,
            "CVH": 0.023661,
            "EDN": 0.024469,
            "GGAL": 0.143424,
            "METR": 0.022479,
            "MIRG": 0.019271,
            "PAMP": 0.077425,
            "SUPV": 0.06983,
            "TGNO4": 0.02126,
            "TGSU2": 0.028979,
            "TRAN": 0.040185,
            "TXAR": 0.034453, 
            "VALO": 0.041636,
            "YPFD": 0.070441,
            "TS": 0.031629,
            "FRAN": 0.023195}
    
    #Mucho riesgo de error manual.
    #Checkeo si esta ok
    if abs(sum(pond.values())-1)<0.01:
        pass
    else:
        print('LAS PONDERACIONES SON INCORRECTAS. CHECKEAR!!')
        exit()
    #Perfecto, tiende a la unidad.
    
    cant = {"ALUA": 52.2936396,
            "APBR": 11.4163686,
            "BMA": 14.788527,
            "BYMA": 5.5296307,
            "CEPU": 42.3187712,
            "COME": 174.7832737,
            "CVH": 2.3441567,
            "EDN": 15.9605468,
            "GGAL": 45.4256593,
            "METR": 19.9784098,
            "MIRG": 1.739994,
            "PAMP": 50.849412,
            "SUPV": 36.5670641,
            "TGNO4": 10.9110005,
            "TGSU2": 8.077373,
            "TRAN": 27.7822568,
            "TXAR": 68.4188939, 
            "VALO": 231.4309395,
            "YPFD": 3.6597788,
            "TS": 1.52151,
            "FRAN": 4.850911}
    
    #Le agrego las cantidades teóricas a mi tabla
    PanelLider_pd['cant'] = PanelLider_pd['Especie'].map(cant)
    #Le agrego los ponderadores a mi tabla
    PanelLider_pd['pond'] = PanelLider_pd['Especie'].map(pond)
    
    #Transformo las variaciones en floats para manipularlas matemáticamente.
    for i in range(len(PanelLider)):
        PanelLider_pd.loc[i, 'VariaciónDiaria'] = PanelLider_pd.loc[i, 'VariaciónDiaria'].replace(",",".")
        PanelLider_pd.loc[i, 'VariaciónDiaria'] = PanelLider_pd.loc[i, 'VariaciónDiaria'].replace(" %","")
    PanelLider_pd['VariaciónDiaria'] = PanelLider_pd['VariaciónDiaria'].astype(float)
    
    #Transformo los últimos precios en floats para poder multiplicarlos  
    for i in range(len(PanelLider)):
        PanelLider_pd.loc[i, 'ÚltimoPrecio'] = PanelLider_pd.loc[i, 'ÚltimoPrecio'].replace(",",".")
    PanelLider_pd['ÚltimoPrecio'] = PanelLider_pd['ÚltimoPrecio'].astype(float)  
    
    #Calculo el valor ponderado por acción, para luego sumarlas y obtener el 
    #valor del índice.
    PanelLider_pd['ValorIndice'] = PanelLider_pd['ÚltimoPrecio'] * PanelLider_pd['cant'] * PanelLider_pd['pond']   
    
    indice = round(sum(PanelLider_pd['ValorIndice']), 2)
    print('El valor del índice es: ${}'.format(indice))
    print('\n*El valor del índice es incorrecto debido a la desactualización de la pagina oficial')
    
    #############################################################################
    
    print("\n\n ------------------------------------------------------------ \n")
    
    print("\n3) Clasificar los papeles por sector \n")
    
    '''
    Hubiese sido muy fácil volver a hacer un diccionario y mapear los sectores
    como hice con las cantidades teóricas y los ponderadores, pero para hacer
    algo diferente vo a levantar un .txt que era lo que hacia el parser original
    '''
    #Detecto en dónde están guardados los archivos
    path = os.getcwd()
    #Abro el archivo
    archivo = open(path + '\\Sectores.txt','r')
    #Leo las líneas
    sectores = archivo.readlines()
    #Le quito los saltos de línea (\n)
    sectores = [x.strip() for x in sectores]
    #Separo cada línea del archivo
    for linea in range(len(sectores)):
        sectores[linea] = sectores[linea].split()
    #Lo transformo en diccionario para usar la funcion map()
    sectores = dict(sectores)
    #Mapeo a mi PanelLider_pd
    PanelLider_pd['Sector'] = PanelLider_pd['Especie'].map(sectores)
    #Ordeno por sectores para que la salida al excel sea mas ordenada
    PanelLider_pd = PanelLider_pd.sort_values('Sector', ascending=True)
    
    print('La clasificación de la tabla por sector es la siguiente:\n')
    print(PanelLider_pd)
    
    #############################################################################
    print("\n\n ------------------------------------------------------------ \n")
    
    print("\n4) Pegar ordenadamente la información en un XLS \n")
    
    # Creo un nuevo archivo de excel para alimentarlo con la info del script.
    wb = xlsxwriter.Workbook(path + '\\Francisco_Cucullu.xlsx')
    wb.add_worksheet('Tabla')
    writer = pd.ExcelWriter(path + '\\Francisco_Cucullu.xlsx')
    
    #Voy a transformar las columnas que nunca use en números para que en el excel
    #no salga el cartel de convertir a número (antiestético y molesto).
    for i in range(len(PanelLider)):
        PanelLider_pd.loc[i, 'CierreAnterior'] = PanelLider_pd.loc[i, 'CierreAnterior'].replace(",",".")
        PanelLider_pd.loc[i, 'PrecioApertura'] = PanelLider_pd.loc[i, 'PrecioApertura'].replace(",",".")
        PanelLider_pd.loc[i, 'PrecioMáximo'] = PanelLider_pd.loc[i, 'PrecioMáximo'].replace(",",".")
        PanelLider_pd.loc[i, 'PrecioMínimo'] = PanelLider_pd.loc[i, 'PrecioMínimo'].replace(",",".")
        PanelLider_pd.loc[i, 'Precio Prom. Pond.'] = PanelLider_pd.loc[i, 'Precio Prom. Pond.'].replace(",",".")
        PanelLider_pd.loc[i, 'VolumenEfectivo ($)'] = PanelLider_pd.loc[i, 'VolumenEfectivo ($)'].replace(".","")
        PanelLider_pd.loc[i, 'Volumen Nominal'] = PanelLider_pd.loc[i, 'Volumen Nominal'].replace(".","")
    PanelLider_pd['CierreAnterior'] = PanelLider_pd['CierreAnterior'].astype(float)  
    PanelLider_pd['PrecioApertura'] = PanelLider_pd['PrecioApertura'].astype(float)  
    PanelLider_pd['PrecioMáximo'] = PanelLider_pd['PrecioMáximo'].astype(float)  
    PanelLider_pd['PrecioMínimo'] = PanelLider_pd['PrecioMínimo'].astype(float)  
    PanelLider_pd['Precio Prom. Pond.'] = PanelLider_pd['Precio Prom. Pond.'].astype(float)  
    PanelLider_pd['VolumenEfectivo ($)'] = PanelLider_pd['VolumenEfectivo ($)'].astype(float)  
    PanelLider_pd['Volumen Nominal'] = PanelLider_pd['Volumen Nominal'].astype(float)  
    
    #Voy a crear una última fila en el DataFrame para contener los datos del índice
    CierreAnterior = round(sum(PanelLider_pd['CierreAnterior'] * PanelLider_pd['cant'] * PanelLider_pd['pond']), 2)
    PrecioApertura = round(sum(PanelLider_pd['PrecioApertura'] * PanelLider_pd['cant'] * PanelLider_pd['pond']), 2)
    PrecioMáximo = round(sum(PanelLider_pd['PrecioMáximo'] * PanelLider_pd['cant'] * PanelLider_pd['pond']), 2)
    PrecioMínimo = round(sum(PanelLider_pd['PrecioMínimo'] * PanelLider_pd['cant'] * PanelLider_pd['pond']), 2)
    ÚltimoPrecio = round(sum(PanelLider_pd['ÚltimoPrecio'] * PanelLider_pd['cant'] * PanelLider_pd['pond']), 2)
    VariaciónDiaria = round((ÚltimoPrecio / CierreAnterior - 1), 4)
    VolumenEfectivo = sum(PanelLider_pd['VolumenEfectivo ($)'])
    VolumenNominal = sum(PanelLider_pd['Volumen Nominal'])
    ind = pd.Series(["INDICE", '', CierreAnterior, PrecioApertura, PrecioMáximo,
                     PrecioMínimo, ÚltimoPrecio, VariaciónDiaria,
                     VolumenEfectivo, VolumenNominal,'','','',indice,''], index=[
                    'Especie', 'Hora Cotización', 'CierreAnterior', 'PrecioApertura',
                    'PrecioMáximo', 'PrecioMínimo', 'ÚltimoPrecio', 'VariaciónDiaria',
                    'VolumenEfectivo ($)', 'Volumen Nominal', 'Precio Prom. Pond.',
                    'cant', 'pond', 'ValorIndice', 'Sector'])
    PanelLider_pd = PanelLider_pd.append(ind, ignore_index=True)
    
    #Se exporta a Excel.
    PanelLider_pd.to_excel(writer, 'Tabla', index=False)
    wb.close()    
    
    print("Se crea un nuevo archivo y se extrae la información")
    print("\nLa ruta del archivo es: \n"+path+"\\Francisco_Cucullu.xlsx")
    
    graph.append(indice)
    grafico(graph)
    
    time.sleep(5)


# FIN DEL SCRIPT 

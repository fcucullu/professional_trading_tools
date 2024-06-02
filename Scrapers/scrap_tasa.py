# By Francisco Cucullu

import sys
sys.path.append(r'Y:\Git\Funciones')
import FuncionesFrancisco as FF
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import traceback

##############################################################################
'''                 Funcion para crear archivo CSV                       '''
##############################################################################

def crea_csv():
    
    #Detecto dia
    (DIA, MES, ANO) = FF.DetectaDia()
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Short Rates\\"+ANO+MES+DIA+".csv"
    
    #Creo el cvs incialcon el nombre de las filas correspondiente a los datos que scrapeo
    with open(path, 'w', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        filewriter.writerow(['Horario'])
        filewriter.writerow(['Precio'])
        filewriter.writerow(['Volumen'])
        
    csvfile.close()
    
##############################################################################
'''                 Funcion para alimentar archivo CSV                    '''
##############################################################################

def escribe_tasa():

    #Detecto dia y horario
    (DIA, MES, ANO) = FF.DetectaDia()
    horario = FF.DetectaHorario()
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Short Rates\\"+ANO+MES+DIA+".csv"
    
    try:
        #Parser
        plazo = 7 #establezco un plazo inicial
        while True:  #Hago loop hasta encontrar el plazo mas corto operado en el dia
            URL='http://10.0.0.137/home/quote?ticker=PESOS&mercado=bcba&plazo='+str(plazo)
            page=requests.get(URL)
            soup=BeautifulSoup(page.content, 'xml')
            fecha = soup.Cotizacion['fecha']
            hora = int(soup.Cotizacion['hora'][:2])
            
            if fecha == str(str(int(MES))+'/'+str(int(DIA))+'/'+ANO) and hora > 10: #condicion de break
                #Le agrego un INT al mes para que cuando sean meses con un solo numero, solo venga "1" y no "01", asi matchea con la pagina
                break
            
            plazo += 1
        
        #Scrapeo datos que me interesan
        last = soup.Cotizacion['precioUlt']
        vol = int(str(soup.Cotizacion['totalNominal']).split('.')[0])
        tick = pd.DataFrame({horario: [last, float(vol)]}) #le agrego float al volumen para que se agregue bien
        tick = tick.astype(float) #Para que todos los datos sean numeros
        
        #Levanto info del CSV y le agrego la info nueva
        csv_input = pd.read_csv(path, sep=';', decimal=',')
        csv_input = csv_input.join(tick)
        csv_input.to_csv(path, index=False, sep=';', decimal=',')
        print('TASA ({} dias) esta en {}%'.format(plazo, last))
        
    except:
        print('Hubo un problema en la actualización de tasa a las {}'.format(horario))
        pass
    
##############################################################################
'''                     Funcion para los arbitradores                     '''
##############################################################################

def tasa_multiprocessing(v, lock):
    
    #Detecto dia y horario
    (DIA, MES, ANO) = FF.DetectaDia()
    
    print('\nComienza la actualización de tasa para operatoria')
    
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < 16:
            time.sleep(10)
            try:
                #Parser
                plazo = 7 #establezco un plazo inicial
                while True:  #Hago loop hasta encontrar el plazo mas corto operado en el dia
                    URL='http://10.0.0.137/home/quote?ticker=PESOS&mercado=bcba&plazo='+str(plazo)
                    page=requests.get(URL)
                    soup=BeautifulSoup(page.content, 'xml')
                    fecha = soup.Cotizacion['fecha']
                    hora = int(soup.Cotizacion['hora'][:2])
                    
                    plazo += 1
                    if fecha == str(str(int(MES))+'/'+str(int(DIA))+'/'+ANO) and hora > 10: #condicion de break
                        #Le agrego un INT al mes para que cuando sean meses con un solo numero, solo venga "1" y no "01", asi matchea con la pagina
                        break
                
                #Scrapeo datos que me interesan
                last = float(soup.Cotizacion['precioUlt'])/100
                
                #   CRITICAL   #
                lock.acquire()
                v.value = last
                #print('\nTasa para operatoria = '+str(round(v.value,4)))
                lock.release()
                #   CRITICAL   #
                now = datetime.datetime.now()
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR ACTUALIZANDO LA TASA DE OPERATORIA --- ')
                traceback.print_exc()
                continue
        else:
            BREAK = True
            print('\nSe detiene la actualización de tasa para operatoria')
            break
            
    return


##############################################################################
'''                          Funcion para printear                       '''
##############################################################################

def print_tasa():
    
   #Veo cual fue el cierre de ayer para el % de variacion diaria
    for i in range(1,10):
        try:
            archivo = FF.DeltaDateHoy(i)[1].replace('-','')+'.csv'
            path = "Y:\\Git\\Data\\Short Rates\\" + archivo
            csv_input = pd.read_csv(path, sep=';', decimal=',')
            prev = csv_input.iloc[0,-1]
            break
        except FileNotFoundError:
            continue
    
    #Detecto dia y horario
    (DIA, MES, ANO) = FF.DetectaDia()
    
    try:
        #Parser
        plazo = 7 #establezco un plazo inicial
        while plazo < 30:  #Hago loop hasta encontrar el plazo mas corto operado en el dia
            URL='http://10.0.0.137/home/quote?ticker=PESOS&mercado=bcba&plazo='+str(plazo)
            page=requests.get(URL)
            soup=BeautifulSoup(page.content, 'xml')
            fecha = soup.Cotizacion['fecha']
            hora = int(soup.Cotizacion['hora'][:2])
            
            if fecha == str(str(int(MES))+'/'+str(int(DIA))+'/'+ANO) and hora > 10: #condicion de break
                #Le agrego un INT al mes para que cuando sean meses con un solo numero, solo venga "1" y no "01", asi matchea con la pagina
                break
            
            plazo += 1
        
        #Scrapeo datos que me interesan
        last = float(soup.Cotizacion['precioUlt'])
        var = '+'+str(round((last/prev-1)*100,2))+'%' if round((last/prev-1)*100,2)>0 else str(round((last/prev-1)*100,2))+'%'

        
    except:
        last = 'N/D'
        var = 'N/D'
        pass
    
    
    return last, var

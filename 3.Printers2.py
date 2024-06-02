#By Francisco Cucullu

import schedule
import time
import sys
sys.path.append(r'Y:\Git\Funciones')
sys.path.append(r'Y:\Git\Scrapers')
sys.path.append(r'Y:\Git\Webdrivers')
sys.path.append(r'Y:\Git\algotrading\Varios')
import Reporte35 as dolarSUPV
import FuncionesFrancisco as FF #Funciones varias
import pandas as pd
import numpy as np
from tabulate import tabulate
import multiprocessing
import datetime
import Streaming
import traceback


lista = pd.read_csv('Y:\\Git\\algotrading\\Dolar\\tickers_MEP.csv', sep=';', decimal=',')

##############################################################################
'''                         Funciones individuales                         '''
##############################################################################

def printear(cotizaciones, PsupvC, PsupvV):
    np.set_printoptions(suppress=True)
    try:
        while True==True:
            time.sleep(0.5)
            headers = ['Titulo',"ProfC", "PrecioC", "PrecioV", "ProfV"]
            printt = np.array([['SUPV',9999, PsupvC.value, PsupvV.value, 9999]])    
            try:
                rows = np.where((cotizaciones.value[:,15] != 0) | (cotizaciones.value[:,16] != 0))[0]
                for row in rows:
                    printt = np.append(printt, [[lista.iloc[row,0],cotizaciones.value[row,14], cotizaciones.value[row,15], cotizaciones.value[row,16], cotizaciones.value[row,17]]])
            except:
                pass
            
            printt = tabulate( np.reshape(printt, (int(len(printt)/5+ (0 if len(printt)>1 else 1)),5)),
                              headers, tablefmt="fancy_grid", stralign="center", numalign="center")
            
            print(printt)
    except:
        traceback.print_exc()
    
def streaming(path_tickers, cotizaciones, lock):
    Streaming.streaming_MEP_inmediato(path_tickers, cotizaciones, lock)
    return
  
def dolar_supv(PsupvC, PsupvV):   
    while True==True:
        dolarSUPV.dolarSUPV_arbitraje(PsupvC, PsupvV)
   
##############################################################################
'''                       Funcion GLOBAL                               '''
##############################################################################
 
    
def Global(): 
    if __name__ == "__main__":    
        print('Comienza el Printer')
        
        now = datetime.datetime.now() #Hora en la que comienza la funcion        
        
        m = multiprocessing.Manager() #Declaro el Manager de multiprocessing
        lock = m.Lock() #Declaro la proteccion para que solo un script manipule info al a vez
        PsupvC = m.Value('d', 0)
        PsupvV = m.Value('d', 0)
        cotizaciones = m.Value('d', 1) #Tabla de cotizaciones
        p = multiprocessing.Pool(processes=10) #Declaro pool de workers
        path_tickers = 'Y:\\Git\\algotrading\\Dolar\\tickers_MEP.csv'

        try:
            p.starmap_async(streaming, [(path_tickers, cotizaciones, lock)])
            p.starmap_async(dolar_supv, [(PsupvC, PsupvV)])
            p.starmap_async(printear, [(cotizaciones, PsupvC, PsupvV)])
            
        except:
            traceback.print_exc()
        
        #Espero a que sean las 16hrs para liquidar parets and childs
        while now.hour < 16:
            time.sleep(1)
            now = datetime.datetime.now()
        
        time.sleep(200) #Le doy un tiempo para que todos los workers hagan su ultima vuelta
        p.terminate() #Liquido pool de procesos
        p.join() #Joineo memoria del pool al main
                          
    return



##############################################################################
'''                            EMERGENCIA                              '''
'''                            EMERGENCIA                              '''
##############################################################################
          
if __name__ == '__main__':
    Global()
#    
###############################################################################
#'''                 Defino horarios para dispara scripts                   '''
###############################################################################
#
#schedule.every().day.at("10:50").do(crea_csv).tag('files')
#
#schedule.every(5).seconds.do(print_5seg)  #Aqui definí intervalos de 15 segs para el script
#
###############################################################################
#'''                       Incicio el scheduler                           '''
###############################################################################
#
#horario = FF.DetectaHorario()
##while horario != '11:00':
##    time.sleep(1)
#    
#while horario != '16:01': #Que corra mientras el horario sea diferente a 16:01 y despues que cierre!
#    schedule.run_pending()
#    time.sleep(1)
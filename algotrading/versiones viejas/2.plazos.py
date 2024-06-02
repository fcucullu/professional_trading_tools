#By Francisco Cucullu

import schedule
import time
import datetime #Para detener el algoritmo a las 16hrs (por CI)
import sys
sys.path.append(r'Y:\Git\Funciones')
sys.path.append(r'Y:\Git\algotrading')
import FuncionesFrancisco as FF #Funciones varias
import multiprocessing #modulo para disparar varios scripts al mismo tiempoo
import Arbitraje_plazos_generico
import Worker_plazos_generico
import scrap_tasa as tasa
(DIA, MES, ANO) = FF.DetectaDia()
import pandas as pd

##############################################################################
'''                 Funciones individuales                       '''
##############################################################################

def csv_plazos(): #Funcion para crear el archivo donde se guardaran los trades
    exec(open(r'Y:\Git\algotrading\Arbitraje_plazos_archivo.py').read())
    print('Archivo CSV de arbitraje de plazos creado.')   
    
def plazos(ticker, q, lock, v, contador, feriados): #Funcion que dispara los arbitradores
    Arbitraje_plazos_generico.arbitraje_plazos_value(ticker, q, lock, v, contador, feriados)
    return

def worker_plazos(csv_input, q, lock): #Funcion que alimenta el archivo
    Worker_plazos_generico.worker(csv_input, q, lock)
    return

def tasa_plazos(v, lock): #Funcion que actualiza la memoria compartida entre arbitradores
    v.value = tasa.tasa_multiprocessing(v, lock)
    return

def detener(job_func_tag): #Funcion que quita del scheduler las tareas de plazos
    schedule.clear(job_func_tag)
    hora = FF.DetectaHorario()
    print('Se detuvo {} a las {}'.format(job_func_tag, hora))      
    return
    

##############################################################################
'''                       Funcion GLOBAL                               '''
##############################################################################
def Global(feriados): 
    if __name__ == "__main__":    
        now = datetime.datetime.now() #Hora en la que comienza la funcion        
        
        m = multiprocessing.Manager() #Declaro el Manager de multiprocessing
        q = m.Queue() #Declaro la Queue compartida donde los arbitradores colocaran la info
        lock = m.Lock() #Declaro la proteccion para que solo un script manipule info al a vez
        v = m.Value('d', 1) #Declaro el value que tendra la tasa spot realtime con valor de inicio suficientemente alto para que no arranque hasta scanear la tasa
        contador = m.Value('d', 1) #Declaro un contador compartido que empiece en 1 y contara los trades.
        p = multiprocessing.Pool(processes=200) #Declaro pool de workers
        csv_input = "Y:\\Git\\Data\\Algotrades\\"+ANO+MES+DIA+".csv"
            
        scaners = pd.read_csv('Y:\\Git\\algotrading\\tickers2.csv', sep=';', decimal=',')        
        args = []
        for i in scaners.iloc[:,0]:
            args.append(tuple([i, q, lock, v, contador, feriados]))
#        args = [('AY24', q,lock,v,contador,feriados)]
                
        #Comienzo workers sin sincronizar (para que todos vayan al mismo tiempo)
        p.starmap_async(plazos, args)
        p.starmap_async(worker_plazos, [(csv_input, q, lock)])
        p.starmap_async(tasa_plazos, [(v, lock)])
        
        #Espero a que sean las 16hrs para liquidar parets and childs
        while now.hour < 16:
            time.sleep(1)
            now = datetime.datetime.now()
        
        time.sleep(120) #Le doy un tiempo para que todos los workers hagan su ultima vuelta
        p.terminate() #Liquido pool de procesos
        p.join() #Joineo memoria del pool al main
                          
    return

##############################################################################
'''                    Declaro cantidad de feriados                       '''
##############################################################################

if __name__ == '__main__':
    print("¿Cuantos feriados hay en las proximas 48hrs habiles?")
    feriados = int(input())

##############################################################################
'''                            EMERGENCIA                              '''
'''                            EMERGENCIA                              '''
##############################################################################
          
if __name__ == '__main__':
    Global(feriados)
#
###############################################################################
#'''                 Defino horarios para dispara scripts                   '''
###############################################################################
#
#'''NOTA: Para correr los scripts es necesario declarar "if __name__ == '__main__'"
#por que el modulo de multiprocessing dispara varios scripts en paralelo y
#si no declaro esto, cada corrida en simultaneo volverá a correr estas lineas
#que solo quiero que sean leidas por el __main__'''
#
###Agendo tareas para realizarse automaticamente en horarios especificos
#if __name__ == '__main__': 
#    # CREAR ARCHIVOS
#    schedule.every().day.at("10:50").do(csv_plazos).tag('files')
#    
#    # ARBITRAJE DE PLAZOS
#    schedule.every().day.at('11:00').do(Global, feriados).tag('plazos')
#    schedule.every().day.at("16:03").do(detener, 'plazos').tag('stop')    
#
###############################################################################
#'''                       Incicio el scheduler                           '''
###############################################################################
#if __name__ == '__main__':
#    horario = FF.DetectaHorario()
#    while horario != '16:01': #Que corra mientras el horario sea diferente a 16:01 y despues que cierre!
#        schedule.run_pending()
#        time.sleep(1)
#     

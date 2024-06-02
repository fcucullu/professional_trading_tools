#By Francisco Cucullu

import sys
sys.path.append(r'Y:\Git\Funciones')
sys.path.append(r'Y:\Git\algotrading\Dolar')
sys.path.append(r'Y:\Git\algotrading\API')
sys.path.append(r'Y:\Git\algotrading\Varios')
sys.path.append(r'Y:\Git\Webdrivers')
import schedule
import time
import datetime #Para detener el algoritmo a las 16hrs (por CI)
import FuncionesFrancisco as FF #Funciones varias
import multiprocessing #modulo para disparar varios scripts al mismo tiempoo
import Worker_csv
import Actualizador_token
(DIA, MES, ANO) = FF.DetectaDia()
import Ejecutador_dolar
import Arbitrador_dolar
import Streaming
#import logs
from funcionesAPI import Requests, Sandbox  #APIS 
requests = Requests()
sandbox = Sandbox()
import traceback
import pandas as pd
import csv
import Reporte35 as dolarSUPV
import App_MEP


##############################################################################
'''                 Funciones individuales                       '''
##############################################################################

def crea_csv(path):

    #Detecto dia
    (DIA, MES, ANO) = FF.DetectaDia()
    
    #Creo el cvs incialcon el nombre de las filas correspondiente a los datos que scrapeo
    with open(path, 'w', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        filewriter.writerow(['Hora','# Trade','N TR','Ticker','C/V','Plazo','Cantidad','Precio',
                             'TC MEP','TC SUPV','Diferencia','Ganancia','Calzada?',
                             'Deteccion','PcP','PvP','PcD','PvD','ProfC','TC_C','TC_V','ProfV'])
 
    csvfile.close()
    print(' --------------- ARCHIVO CSV CREADO ---------------------')

def streaming(path_tickers, cotizaciones, lock):
    Streaming.streaming_MEP_inmediato(path_tickers, cotizaciones, lock)
    return

def worker(csv_input, contador, q, lock, hora_stop): #Funcion que alimenta el archivo
    Worker_csv.worker(csv_input, contador, q, lock, hora_stop)
    return

def actualiza_token(hora_stop, token, lock):
    Actualizador_token.actualizar_token(hora_stop, token, lock)
    return

def ejecutar_compras(hora_stop, inputs_compra, tr_compra, lock, semaforo, token):
    Ejecutador_dolar.flujo_compra_dolar(hora_stop, inputs_compra, tr_compra, lock, semaforo, token)
    return 

def ejecutar_ventas(hora_stop, inputs_venta, tr_venta, lock, semaforo, token):
    Ejecutador_dolar.flujo_venta_dolar(hora_stop, inputs_venta, tr_venta, lock, semaforo, token)
    return 
'''
def ejecutar_operaciones(hora_stop, inputs_compra, inputs_venta, tr_compra, tr_venta, lock, semaforo, token):
    Ejecutador_dolar.flujo_operatoria_xiolnet_testing(hora_stop, inputs_compra, inputs_venta, tr_compra, tr_venta, lock, semaforo, token)
    return 
'''

def ejecutar_operaciones(hora_stop, inputs_compra, inputs_venta, tr_compra, tr_venta, lock, semaforo, token):
    Ejecutador_dolar.flujo_operatoria_secuencial(hora_stop, inputs_compra, inputs_venta, tr_compra, tr_venta, lock, semaforo, token)
    return 


def detener(job_func_tag): #Funcion que quita del scheduler las tareas de plazos
    schedule.clear(job_func_tag)
    hora = FF.DetectaHorario()
    print('Se detuvo {} a las {}'.format(job_func_tag, hora))      
    return

def ventana(cotizaciones, inputs_compra, inputs_venta, semaforo, lock):
    App_MEP.ventana(cotizaciones, inputs_compra, inputs_venta, semaforo, lock)
    
def dolar_supv(PsupvC, PsupvV):   
    while True==True:
        dolarSUPV.dolarSUPV_arbitraje(PsupvC, PsupvV)

def control_streaming(hora_stop, path_tickers, cotizaciones, control_ok):
    Streaming.control_streaming(hora_stop, path_tickers, cotizaciones, control_ok)
    
def arbitrador_dolar(hora_stop, trades_a_registrar, control_ok, lock, PsupvC, PsupvV, contador, cotizaciones, saldo, saldo_ya_operado, operacion_maxima, tr_compra, tr_venta, inputs_compra, inputs_venta, semaforo, token):
    Arbitrador_dolar.arbitrador_dolar(hora_stop, trades_a_registrar, control_ok, lock, PsupvC, PsupvV, contador, cotizaciones, saldo, saldo_ya_operado, operacion_maxima, tr_compra, tr_venta, inputs_compra, inputs_venta, semaforo, token)


##############################################################################
'''                       Funcion GLOBAL                               '''
##############################################################################
def Global(saldo_ya_operado): 
    if __name__ == "__main__":    
        now = datetime.datetime.now() #Hora en la que comienza la funcion        
        
        hora_stop = 15
        
        m = multiprocessing.Manager() #Declaro el Manager de multiprocessing
        trades_a_registrar = m.Queue() #Declaro la Queue compartida donde los arbitradores colocaran la info
        lock = m.Lock() #Declaro la proteccion para que solo un script manipule info al a vez
        contador = m.Value('d', 1) #Declaro un contador compartido que empiece en 1 y contara los trades.
        cotizaciones = m.Value('d', 1) #Tabla de cotizaciones
        saldo = m.Value('d', 0)  #Saldo para operar en todo el dia
        tok = m.Value('d', 0)  #Token
        Actualizador_token.actualizar_token_once(tok, lock)
        saldo.value = sandbox.saldo_arg_pesos_inmediato_notok()
        p = multiprocessing.Pool(processes=10) #Declaro pool de workers
        path_tickers = 'Y:\\Git\\algotrading\\Dolar\\tickers_MEP.csv'

        #Variables para el ejecutador
        tr_compra = m.Value('d', 0)
        tr_venta = m.Value('d', 0)
        PsupvC = m.Value('d', 0)
        PsupvV = m.Value('d', 0)
        inputs_compra = m.Value('d', 0)
        inputs_venta = m.Value('d', 0)
        semaforo = m.Value('d', 0)
        control_ok = m.Value('d', 0) #0=OK / 0!=ERROR
        
        operacion_maxima = 10000 #dolares
        SALDO_MAXIMO_PARA_OPERAR = 5000 #Dolares
        saldo.value = SALDO_MAXIMO_PARA_OPERAR
        
        try:
                        
            #Comienzo workers sin sincronizar (para que todos vayan al mismo tiempo)
            p.starmap_async(streaming, [(path_tickers, cotizaciones, lock)])
            p.starmap_async(actualiza_token, [(hora_stop, tok, lock)])
            p.starmap_async(worker, [(path, contador, trades_a_registrar, lock, hora_stop)])
            #p.starmap_async(arbitrador, [(hora_stop, tr_compra, tr_venta, PsupvC, PsupvV, trades_a_registrar, semaforo, contador, lock)])
            p.starmap_async(arbitrador_dolar, [(hora_stop, trades_a_registrar, control_ok, lock, PsupvC, PsupvV, contador, cotizaciones, saldo, saldo_ya_operado, operacion_maxima, tr_compra, tr_venta, inputs_compra, inputs_venta, semaforo, tok)])
            p.starmap_async(dolar_supv, [(PsupvC, PsupvV)])
            #p.starmap_async(ejecutar_compras, [(hora_stop, inputs_compra, tr_compra, lock, semaforo, tok)])
            #p.starmap_async(ejecutar_ventas, [(hora_stop, inputs_venta, tr_venta, lock, semaforo, tok)])
            p.starmap_async(ejecutar_operaciones, [(hora_stop, inputs_compra, inputs_venta, tr_compra, tr_venta, lock, semaforo, tok)])
            p.starmap_async(ventana, [(cotizaciones, inputs_compra, inputs_venta, semaforo, lock)])  
            p.starmap_async(control_streaming, [(hora_stop, path_tickers, cotizaciones, control_ok)])
            
        except:
            traceback.print_exc()
        
        
        #Espero a que sean las 16hrs para liquidar parets and childs
        while now.hour < hora_stop:
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
    now = datetime.datetime.now()
    path = "Y:\\Git\\Data\\Algotrades\\Dolar\\"+ANO+MES+DIA+".csv"  
    print("¿Cuantos dolares ya se operaron?")
    saldo_ya_operado = int(input())
    if now.hour < 11:
        crea_csv(path)
    Global(saldo_ya_operado)
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
#    path = "Y:\\Git\\Data\\Algotrades\\Dolar\\"+ANO+MES+DIA+".csv"
#    schedule.every().day.at("10:50").do(crea_csv, path).tag('files')
#    
#    # ARBITRAJE DOLAR
#    schedule.every().day.at('11:00').do(Global).tag('dolar')
#    schedule.every().day.at("16:03").do(detener, 'dolar').tag('stop')    
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

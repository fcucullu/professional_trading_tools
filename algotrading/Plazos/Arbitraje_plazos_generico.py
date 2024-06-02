#By Francisco Cucullu

'''                         ARBITRAJE DE PLAZOS                        '''
#print(__name__)
def arbitraje_plazos_value(ticker, q, lock, v, contador, feriados, cotizaciones, saldo, tr_compra, tr_venta, inputs_compra, inputs_venta, semaforo, token):
    
    import sys  #para traer varios paths con diferentes recursos
    path = r'Y:\Git\algotrading'
    path2 = r'Y:\Git\algotrading\API'
    path3 = r'Y:\Git\Funciones'
    sys.path.append(path)
    sys.path.append(path2)
    sys.path.append(path3)
    from funcionesAPI import Sandbox  #APIS 
    sandbox = Sandbox()
    import pandas as pd #Para manejar la info
    import numpy as np
    import FuncionesFrancisco as FF #Funciones varias
    import datetime #Para detener el algoritmo a las 16hrs (por CI)
    import traceback
    from tabulate import tabulate
    import time
    dia, mes, ano = FF.DetectaDia()
    hoy=str(ano+"-"+mes+"-"+dia) 

    
    ##############################################################################
    '''       Identifico fines de semana y feriados para calculo de TNA       '''
    ##############################################################################
    
    if FF.weekday() == 'jueves' or FF.weekday() == 'viernes':
        TNA_days = 4 + feriados
    else:
        TNA_days = 2 + feriados    
    
    ##############################################################################
    '''       Declaro derechos de mercado, IVA, si es un bono y IDTitulo       '''
    ##############################################################################
    
    #Lista de activos escaneados
    lista = pd.read_csv('Y:\\Git\\algotrading\\tickers.csv', sep=';', decimal=',')
    
    #Derechos de mercado
    derechos = {'acciones': 0.0008*1.21,
                'bonos': 0.0001,
                'letras': 0.00001}
    
    lista['derechos'] = lista['tipo'].map(derechos)
    
    derecho = float(lista.loc[lista['tickers'] == ticker]['derechos'])
    ID = lista.loc[lista['tickers'] == ticker]['ID'].item()
    bono = True if lista.loc[lista['tickers'] == ticker]['tipo'].item() == 'bonos' else False
    #Lo pongo float por que luego en los condicionales no me tome pandas.series

    ##############################################################################
    '''                         Arranco el arbitrador                         '''
    ##############################################################################
    print('\nComienza el arbitraje de plazos en '+ticker)
        
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < 16:
            
            try: #le pongo este TRY para que al encontrar un error en "i", vaya al siguiente sin detenerse
                
                #Parametros de las cotizaciones
                while True: #loop infinito hasta que la tabla de cotizaciones este hecha
                    try:        
                        row_CI = np.where((cotizaciones.value[:,0] == ID) & (cotizaciones.value[:,1] == 1))[0].item()
                        row_48 = np.where((cotizaciones.value[:,0] == ID) & (cotizaciones.value[:,1] == 3))[0].item()        
                    except:
                        time.sleep(5)
                        continue
                    break #Si no salta la excepcion, cotizaciones ya esta hecha, entonces sale del loop
                        

                Qc_CI, Pc_CI, Pv_CI, Qv_CI = cotizaciones.value[row_CI, 2:6]
                Qc_48, Pc_48, Pv_48, Qv_48 = cotizaciones.value[row_48, 2:6]                

                ##############################################################################
                '''                        CONDICIONES para OPERAR                                      '''
                ##############################################################################
                
                '''PARAMETROS'''
                    #CANTIDAD
                cantidad = min(Qv_CI, Qc_48)

                
                '''CONDICIONES DE ARBITRAJE'''
                    #TASA 
                try:
                    if Pv_CI > 0:
                        TNA = ((Pc_48*(1-derecho))/(Pv_CI*(1+derecho))-1)*(365/TNA_days)
                    else:
                        TNA = 0
                except:
                    TNA = 0

                
                tasa_mp = v.get()
                try:                        #MARK-UP
                    condicion_tasa = TNA > (tasa_mp + 0) and Pv_CI > 0 
                except: 
                    condicion_tasa = False                
                
                    #MONTO
                monto = Pv_CI*(1+derecho)*cantidad / (1 if bono == False else 100)
                try:
                    '''#######################################'''
                    if saldo.value > 500:
                        if monto > 500:
                            cantidad = ( 500 / (Pv_CI*(1+derecho)) * (1 if bono == False else 100) ) // 1
                    else:
                        if saldo.value < 500:
                            cantidad = ( saldo.value / (Pv_CI*(1+derecho)) * (1 if bono == False else 100) ) // 1
                    
                    '''#######################################'''
                        
#                    if monto > saldo.value:
#                        cantidad = ( saldo.value / (Pv_CI*(1+derecho)) * (1 if bono == False else 100) ) // 1
                except:
                    cantidad == 0 #Por si Pv_CI es cero ya que no se puede dividir por cero.
                    
                if cantidad == 0:
                    condicion_monto = False
                else:
                    condicion_monto = True

                '''DEFINICION'''
                if condicion_tasa == True and condicion_monto == True:
                    arbitrar = True
                else:
                    arbitrar = False

                ##############################################################################
                '''                        EJECUCION                                      '''
                ##############################################################################
                
                if arbitrar == True and semaforo.value == 0:
                    
#################### ''' S T A R T  of  C R I T I C A L  Z O N E  #
                    lock.acquire()
                    
                    semaforo.value = 1 #Pongo el semáforo como "en proceso"
                    
                    horario0 = FF.DetectaHorarioSegundos()
                    print('\nSE ENCONTRO UN ARBITRAJE EN -{}- A LAS {} - Enviando ordenes al mercado'.format(ticker, horario0))
                
                    inputs_compra.value = (ticker, cantidad, Pv_CI, hoy)
                    inputs_venta.value = (ticker, cantidad, Pc_48, hoy)
                
                    trs = contador.get()

                    lock.release()
#################### '''E N D  of  C R I T I C A L  Z O N E'''
                
                    '''Termino con la critical zone para habilitar a los ejecutadores a que
                    cambien los valores de las variables compartidas (semaforos) para así 
                    darle la señal a los arbitradores para continuar '''
                    
                    #Espera hasta que las trs hayan sido ejecutadas
                    while semaforo.value != 5: #Ambos arbitradores habrán sumado +2 al valor de detención =1
                        time.sleep(0.0001)

#################### ''' S T A R T  of  C R I T I C A L  Z O N E  #
                    lock.acquire()

                    #Tomo los resultados de los ejecutadores
                    resultado = (tr_compra.value, tr_venta.value)
                    horario = FF.DetectaHorarioSegundos()
                    
                    #dejo los valores limpios para la proxima ejecucion
                    tr_compra.value = 0 
                    tr_venta.value = 0

                
                    try:
                        if (resultado[0][1][0] == resultado[1][1][0]):
                            TNA_final = np.round( ((resultado[1][1][1]*(1-derecho))/(resultado[0][1][1]*(1+derecho))-1)*(365/TNA_days) *100 ,4)
                        else:
                            TNA_final = 0                            
                    except:
                        TNA_final = 0
                        
                    tr = pd.DataFrame({'Hora': [horario, horario],
                                   '# Trade': [trs, trs],
                                   'Ticker': ticker,
                                   'C/V': ['C', 'V'],
                                   'Plazo': ['T0', 'T2'],
                                   'Cantidad': [resultado[0][1][0], resultado[1][1][0] ],
                                   'Precio': [resultado[0][1][1], resultado[1][1][1]],
                                   'Monto': [-resultado[0][1][1]*(1+derecho)*resultado[0][1][0] / (1 if bono == False else 100), 
                                             resultado[1][1][1]*(1-derecho)*resultado[1][1][0] / (1 if bono == False else 100)],
                                   'TNA': [TNA_final, TNA_final],
                                   'Caucion': [np.round(tasa_mp,4), np.round(tasa_mp,4)],
                                   'Calzada?': ['OK' if (resultado[0][1][0]==resultado[1][1][0]) else 'CERRAR',
                                                'OK' if (resultado[0][1][0]==resultado[1][1][0]) else 'CERRAR'],
                                   'Deteccion': horario0})
                    
                    
                    ##############################################################################
                    '''                        CONTIGENCIA                         '''
                    ##############################################################################
                    calzada = (resultado[0][1][0] == resultado[1][1][0])
                      
                    if calzada == False:
                        TNA_final = 0
                        try:
                            if (resultado[0][1][0] > resultado[1][1][0]): #Hay que VENDER por que se compro de mas
                                cant_cont = resultado[0][1][0] - resultado[1][1][0]
                                side = 'V'
                                plazo = 'T2'
                                p_cont = Pc_48
                                tr_contingencia = sandbox.vender(ticker, cant_cont, p_cont, plazo, hoy, token)
                                
                            elif (resultado[0][1][0] < resultado[1][1][0]): #Hay que COMPRAR por que se vendio de mas
                                cant_cont = resultado[1][1][0] - resultado[0][1][0]
                                side = 'C'
                                plazo = 'T0'
                                p_cont = Pv_CI
                                tr_contingencia = sandbox.comprar(ticker, cant_cont, p_cont, plazo, hoy, token)
                            
                            horario = FF.DetectaHorarioSegundos()
                            tr = tr.append({'Hora': horario,
                                       '# Trade': trs,
                                       'Ticker': ticker,
                                       'C/V': side,
                                       'Plazo': plazo,
                                       'Cantidad': cant_cont,
                                       'Precio': 0,
                                       'Monto': 0,
                                       'TNA': TNA_final,
                                       'Caucion': np.round(tasa_mp,4),
                                       'Calzada?': 'CONTINGENCIA',
                                       'Deteccion': horario0} ,ignore_index=True)
                            
                            for i in range(5):
                                print('¡¡¡ URGENTE !!!: ARBITRAJE DE {} NO CALZO, EJECUTAR TR {} DEL CC 127 !!! \n'.format(ticker, tr_contingencia))
                                time.sleep(5)
            
                        except:
                            for i in range(5):
                                print('¡¡¡ URGENTE !!!: ARBITRAJE DE {} NO CALZO, CERRAR MANUALMENTE!!! (no se genero tr)\n'.format(ticker))
                                time.sleep(5)
    
                
                    ##############################################################################
                    '''                        CIERRE Y PRINTEOS FINALES                       '''
                    ##############################################################################
                    
                    q.put(tr)  
                    contador.value = trs + 1
                    saldo.value = sandbox.saldo_arg_pesos_inmediato(token)
                    
                    semaforo.value = 0 #Vuelvo al valor de continuidad para el resto de los arbitradores
                    
                    lock.release()
                
#################### '''E N D  of  C R I T I C A L  Z O N E'''
                
                    print('\nEl arbitraje de {} se cerro con TNA del {}% a las {}'.format(tr['Ticker'][0], TNA_final, horario))
                    print(tabulate(tr[['Hora','Ticker','C/V','Plazo','Cantidad','Precio','Calzada?']],
                       headers='keys', tablefmt='fancy_grid', showindex=False, stralign="center", numalign="center"))
    
                    now = datetime.datetime.now()
            
            except Exception:
                now = datetime.datetime.now()
                print(' --- HUBO UN ERROR EN EL SCRIPT DE PLAZOS DE {} --- '.format(ticker))
                traceback.print_exc()
                continue
        else:
            print('Se detiene el arbitraje de plazos en '+ticker)
            BREAK = True
            break


    return
    
#  
#if __name__ == '__main__':
#    ticker = 'AY24'
#    import multiprocessing
#    import sys  #para traer varios paths con diferentes recursos
#    path = r'Y:\Git\algotrading'
#    path2 = r'Y:\Git\algotrading\API'
#    path3 = r'Y:\Git\Funciones'
#    sys.path.append(path)
#    sys.path.append(path2)
#    sys.path.append(path3)
#    from funcionesAPI import Requests, Sandbox  #APIS 
#    requests = Requests()
#    sandbox = Sandbox()
#    m = multiprocessing.Manager() #Declaro el Manager de multiprocessing
#    q = m.Queue() #Declaro la Queue compartida donde los arbitradores colocaran la info
#    lock = m.Lock() #Declaro la proteccion para que solo un script manipule info al a vez
#    v = m.Value('d', 0) #Declaro el value que tendra la tasa spot realtime con valor de inicio suficientemente alto para que no arranque hasta scanear la tasa
#    contador = m.Value('d', 1) #Declaro un contador compartido que empiece en 1 y contara los trades.
#    p = multiprocessing.Pool(processes=200) #Declaro pool de workers
#    feriados = -1
#    cotizaciones = m.Value('d', 0)
#       
#    #Variables para el ejecutador
#    tr_compra = m.Value('d', 0)
#    tr_venta = m.Value('d', 0)
#    saldo = m.Value('d', 0)
#    p_ejecucion = multiprocessing.Pool(processes=2)
#    
#    saldo.value = sandbox.saldo_arg_pesos_inmediato()
#    print('El saldo para operar es de: ${}'.format(saldo.value))
#    
#if __name__ == '__main__':
#    arbitraje_plazos_value(ticker, q, lock, v, contador, feriados, cotizaciones, saldo, m, tr_compra, tr_venta, p_ejecucion)
#By Francisco Cucullu

'''                         ARBITRAJE DE DOLAR                        '''
#print(__name__)
def arbitrador_dolar(hora_stop, trades_a_registrar, control_ok, lock, PsupvC, PsupvV, contador, cotizaciones, saldo, saldo_ya_operado, operacion_maxima, tr_compra, tr_venta, inputs_compra, inputs_venta, semaforo, token):
    
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
    import Ejecutador_dolar
    import FuncionesFrancisco as FF #Funciones varias
    import datetime #Para detener el algoritmo a las 16hrs (por CI)
    import traceback
    from tabulate import tabulate
    import time
    dia, mes, ano = FF.DetectaDia()
    hoy=str(ano+"-"+mes+"-"+dia) 
    from notify_run import Notify
    notify = Notify()

    #Codigos de especie
    lista = pd.read_csv('Y:\\Git\\algotrading\\Dolar\\tickers_MEP.csv', sep=';', decimal=',')
    '''LIMITES'''
    OPERACION_MAXIMA = operacion_maxima #Dolares
    saldo_operar = saldo.value - saldo_ya_operado
    spread = 0.02
    
    ##############################################################################
    '''                         Arranco el arbitrador                         '''
    ##############################################################################
    time.sleep(30) #Para darle tiempo al streaming a armar la tabla
    print('\nComienza el arbitraje de dolar')
        
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if (now.hour < hora_stop):
            
            try: 
                
                ##############################################################################
                '''                           OPERAR DOLAR MEP                             '''
                ##############################################################################
                
                #Parametros de las cotizaciones
                VENDER_AL_SUPV = False
                COMPRAR_AL_SUPV = False
                if control_ok.value == 0: #Solo opera si el control esta OK
                    
                    tabla = cotizaciones.value #Para fijar los valores
                    
                    #Comprar dolar y vender al supv           para agrandar la diferencia
                    if len(np.where((tabla[:,16] < PsupvC.value-spread) & (tabla[:,16] > 0))[0]) > 0:
                        row = np.where((tabla[:,16] == np.min(tabla[:,16][np.nonzero(tabla[:,16])])) )[0].item()
                        if tabla[row,17] > 0:
                            horario0 = FF.DetectaHorarioSegundos()
                            print('\nSE ENCONTRO UN ARBITRAJE A LAS {} - Enviando ordenes al mercado'.format(horario0))
                            VENDER_AL_SUPV = True
                    #vender dolar y comprar al supv         para agrandar la diferencia
                    if len(np.where((tabla[:,15] > PsupvV.value+spread) & (PsupvV.value > 0))[0]) > 0:
                        row = np.where((tabla[:,15] == max(tabla[:,15])) )[0].item()
                        if tabla[row,14] > 0:
                            horario0 = FF.DetectaHorarioSegundos()
                            print('\nSE ENCONTRO UN ARBITRAJE EN A LAS {} - Enviando ordenes al mercado'.format(horario0))
                            COMPRAR_AL_SUPV = True

                if (VENDER_AL_SUPV == True) or (COMPRAR_AL_SUPV == True):
                    
                    ticker = lista.loc[lista.iloc[:,1] == tabla[row,0], 'tickers'].item()
                    PcP, PvP = tabla[row,3], tabla[row,5]
                    PcD, PvD = tabla[row,9], tabla[row,11]
                    ProfC, ProfV = tabla[row,14], tabla[row,17]
                    tcC, tcV = tabla[row,15], tabla[row,16]
                    
                    #Parametros para el caso de comprar MEP y vender SUPV
                    if VENDER_AL_SUPV == True:
                        dolares = min(OPERACION_MAXIMA, ProfV*0.8, saldo.value) #lo multiplico por 0.8 para dejarle margen a la profundidad
                        cantidad = int((dolares / PcD) * 100)
                        
                        lock.acquire()
                        trs = contador.get()
                        inputs_compra.value = [ticker, cantidad, PvP, hoy]
                        inputs_venta.value = [ticker+"D", cantidad, PcD, hoy]
                        inputs_compra_cont = inputs_compra.value
                        inputs_venta_cont = inputs_venta.value
                        semaforo.value = 1
                        lock.release()
                        
                    #Parametros para el caso de vender MEP y comprar SUPV
                    if COMPRAR_AL_SUPV == True:
                        dolares = min(OPERACION_MAXIMA, ProfC*0.8, saldo.value) #lo multiplico por 0.8 para dejarle margen a la profundidad
                        cantidad = int((dolares / PvD) * 100)
                        
                        lock.acquire()
                        trs = contador.get()
                        inputs_compra.value = [ticker+"D", cantidad, PvD, hoy]
                        inputs_venta.value = [ticker, cantidad, PcP, hoy]
                        semaforo.value = 1
                        lock.release()
    
    
                    ##############################################################################
                    '''                           WAIT                     '''
                    ##############################################################################
                    '''Termino con la critical zone para habilitar a los ejecutadores a que
                    cambien los valores de las variables compartidas (semaforos) para así 
                    darle la señal a los arbitradores para continuar '''
                    #Espera hasta que las trs hayan sido ejecutadas
                    while semaforo.value != 5: #Ambos arbitradores habrán sumado +2 al valor de detención =1
                        time.sleep(0.0001)


                    ##############################################################################
                    '''                           REGISTRO LAS OPERACIONES                     '''
                    ##############################################################################
#################### ''' S T A R T  of  C R I T I C A L  Z O N E  #
                    lock.acquire()
    
                    #Tomo los resultados de los ejecutadores
                    horario = FF.DetectaHorarioSegundos()
                    
                    if tr_compra.value[1][1][0] != 0: #ACA SE ABRE UN IF PARA EL CASO EN QUE NO SE PUDO CONCERTAR LA COMPRA
                        if tr_venta.value[0].endswith('D'): #ES UNA COMPRA DE DOLARES
                            direccion = 'V'
                            TC_SUPV = PsupvC.value
                            try:
                               TC_MEP = np.round( tr_compra.value[1][1][1] / tr_venta.value[1][1][1] * ((1 + 0.0001) / (1 - 0.0001)) ,2)
                               diferencia = np.round(TC_SUPV - TC_MEP ,2)
                               #ganancia = (-tr_compra.value[1][1][1]*(1 + 0.0001)*tr_compra.value[1][1][0] / 100) + (monto * TC_SUPV)
                            except:
                               TC_MEP = 0
                               diferencia = 0
                               #ganancia = 0
                        else: #ES UNA VENTA DE DOLARES
                            direccion = 'C'
                            #monto = -monto
                            TC_SUPV = PsupvV.value
                            try:
                               TC_MEP = np.round( tr_venta.value[1][1][1] / tr_compra.value[1][1][1] * ((1 - 0.0001) / (1 + 0.0001)) ,2)
                               diferencia = np.round(TC_MEP - TC_SUPV ,2)
                               #ganancia = (tr_venta.value[1][1][1]*(1 - 0.0001)*tr_venta.value[1][1][0] / 100) + (monto * TC_SUPV)
                            except:
                               TC_MEP = 0
                               diferencia = 0
                               #ganancia = 0
                            
                        tr = pd.DataFrame({'Hora': [horario, horario],
                                           '# Trade': [trs, trs],
                                           'N TR': [tr_compra.value[3], tr_venta.value[3]],
                                           'Ticker': [tr_compra.value[0], tr_venta.value[0]],
                                           'C/V': ['C', 'V'],
                                           'Plazo': ['T0', 'T0'],
                                           'Cantidad': [tr_compra.value[1][1][0], tr_venta.value[1][1][0] ],
                                           'Precio': [tr_compra.value[1][1][1], tr_venta.value[1][1][1] ],
                                           'TC MEP': [TC_MEP, TC_MEP],
                                           'TC SUPV': [ TC_SUPV , TC_SUPV],
                                           'Diferencia': [diferencia, diferencia],
                                           'Ganancia': [0, 0],
                                           'Calzada?': ['OK' if (tr_compra.value[1][1][0]==tr_venta.value[1][1][0]) else 'CERRAR',
                                                        'OK' if (tr_compra.value[1][1][0]==tr_venta.value[1][1][0]) else 'CERRAR'],
                                           'Deteccion': [tr_compra.value[2], tr_venta.value[2] ],
                                           'PcP': [PcP,PcP],
                                           'PvP': [PvP,PvP],
                                           'PcD': [PcD,PcD],
                                           'PvD': [PvD,PvD],
                                           'ProfC': [ProfC,ProfC],
                                           'TC_C': [tcC,tcC],
                                           'TC_V': [tcV,tcV],
                                           'ProfV': [ProfV,ProfV]})
                    
    
                        ##############################################################################
                        '''                             CONTIGENCIA                             '''
                        ##############################################################################
                        calzada = (tr_compra.value[1][1][0]==tr_venta.value[1][1][0])
                                            
                        if calzada == False:
                            try:
                                notify.send('DESCALCE en operacion de DOLAR')
                            except Exception:
                                traceback.print_exc()
                                continue
                            try:
                                if (tr_compra.value[1][1][0] > tr_venta.value[1][1][0]): #Hay que VENDER por que se compro de mas
                                    cant_cont = tr_compra.value[1][1][0] - tr_venta.value[1][1][0]
                                    side = 'V'
                                    ticker_cont = inputs_venta_cont[0]
                                    tr_contingencia = sandbox.vender( ticker_cont, cant_cont, inputs_venta_cont[2], 'T0', inputs_venta_cont[3], token)
                                    
                                elif (tr_compra.value[1][1][0] < tr_venta.value[1][1][0]): #Hay que COMPRAR por que se vendio de mas
                                    cant_cont = tr_venta.value[1][1][0] - tr_compra.value[1][1][0]
                                    side = 'C'
                                    ticker_cont = inputs_compra_cont[0]
                                    #tr_contingencia = sandbox.comprar(ticker, cant_cont, p_cont, plazo, hoy, token)
                                    tr_contingencia = Ejecutador_dolar.compra_CI_por_iolnet(127, ticker_cont, inputs_compra_cont[2], cant_cont)
                                
                                horario = FF.DetectaHorarioSegundos()
                                tr = tr.append({'Hora': horario,
                                           '# Trade': trs,
                                           'N TR': tr_contingencia,
                                           'Ticker': ticker_cont,
                                           'C/V': side,
                                           'Plazo': 'T0',
                                           'Cantidad': cant_cont,
                                           'Precio': 'CHECK',
                                           'TC MEP': 'CHECK',
                                           'TC_SUPV': TC_SUPV,
                                           'Diferencia': 'CHECK',
                                           'Ganancia': 'CHECK',
                                           'Calzada?': 'CONTINGENCIA',
                                           'Deteccion': horario,
                                           'PcP': PcP,
                                           'PvP': PvP,
                                           'PcD': PcD,
                                           'PvD': PvD,
                                           'ProfC': ProfC,
                                           'TC_C': tcC,
                                           'TC_V': tcV,
                                           'ProfV': ProfV} ,ignore_index=True)
                                
                                for i in range(5):
                                    print('¡¡¡ URGENTE !!!: ARBITRAJE DE DOLAR NO CALZO, EJECUTAR TR {} DEL CC 127 !!! \n'.format(tr_contingencia))
                                    time.sleep(5)
                
                            except:
                                for i in range(5):
                                    print('¡¡¡ URGENTE !!!: ARBITRAJE DE DOLAR CALZO, CERRAR MANUALMENTE!!! (no se genero tr)\n')
                                    time.sleep(5)
        
                        
                        ##############################################################################
                        '''                           OPERAR DOLAR SUPV                          '''
                        ##############################################################################
                            
                        if calzada == True:
                            try:
                                notify.send('EXITO en operacion de DOLAR')
                            except Exception:
                                traceback.print_exc()
                                continue
                            #Parametros para el caso de comprar MEP y vender SUPV
                            if VENDER_AL_SUPV == True:
                                direccion = 'V'
                                TC_SUPV = PsupvC.value
                                monto = sandbox.saldo_arg_dolares_inmediato(token)
                                tr_dolar = sandbox.vender_dolar('Dolar_Estadounidense', monto, token)
                                #Ejecutador_dolar.vender_dolar_supv(monto)
                                ganancia = -(tr_compra.value[1][1][1]*tr_compra.value[1][1][0]*(1 + 0.000205)/100) + (monto * TC_SUPV)
                                                    
                            #Parametros para el caso de vender MEP y comprar SUPV
                            if COMPRAR_AL_SUPV == True:
                                direccion = 'C'
                                TC_SUPV = PsupvV.value
                                monto = (-1) * sandbox.saldo_arg_dolares_inmediato(token)
                                tr_dolar = sandbox.comprar_dolar('Dolar_Estadounidense', monto, token)
                                #Ejecutador_dolar.comprar_dolar_supv(monto)
                                ganancia = (tr_venta.value[1][1][1]*(1 - 0.000205)*tr_venta.value[1][1][0] / 100) - (monto * TC_SUPV)
    
    
                            tr = tr.append({'Hora': horario,
                                           '# Trade': trs,
                                           'N TR': tr_dolar,
                                           'Ticker': 'DLR_SUPV' ,
                                           'C/V': direccion,
                                           'Plazo': 'T0',
                                           'Cantidad': monto,
                                           'Precio': TC_SUPV,
                                           'TC MEP': TC_MEP,
                                           'TC SUPV': TC_SUPV,
                                           'Diferencia': diferencia,
                                           'Ganancia': ganancia,
                                           'Calzada?': 'OK',
                                           'Deteccion': horario,
                                           'PcP': PcP,
                                           'PvP': PvP,
                                           'PcD': PcD,
                                           'PvD': PvD,
                                           'ProfC': ProfC,
                                           'TC_C': tcC,
                                           'TC_V': tcV,
                                           'ProfV': ProfV} ,ignore_index=True)
    
                        
                        ##############################################################################
                        '''                        CIERRE Y PRINTEOS FINALES                       '''
                        ##############################################################################
                        
                        trades_a_registrar.put(tr)  
                        contador.value = trs + 1
                        saldo.value = saldo_operar - dolares #Para respetar el monto maximo diario
                        #dejo los valores limpios para la proxima ejecucion
                        tr_compra.value = 0 
                        tr_venta.value = 0
                        semaforo.value = 0 #Vuelvo al valor de continuidad para el resto de los arbitradores
                        
                        lock.release()
                
####################### '''E N D  of  C R I T I C A L  Z O N E'''
                
                        print('\nEl arbitraje de DOLAR se cerro con TC del {} (+{}ctvs) a las {}'.format(TC_MEP, diferencia, horario))
                        print(tabulate(tr[['Hora','Ticker','C/V','Plazo','Cantidad','Precio','Calzada?']],
                           headers='keys', tablefmt='fancy_grid', showindex=False, stralign="center", numalign="center"))
        
                        now = datetime.datetime.now()
                        
                    else:
                        print('No se pudo abrir posición, continua el arbitrador')
                        lock.acquire()
                        tr_compra.value = 0 
                        tr_venta.value = 0
                        semaforo.value = 0 #Vuelvo al valor de continuidad para el resto de los arbitradores
                        lock.release()
                        continue
        
            except Exception:
                now = datetime.datetime.now()
                print(' --- HUBO UN ERROR EN EL ARBITRADOR DE DOLAR --- ')
                traceback.print_exc()
                continue
        else:
            print('Se detiene el arbitraje de dolar')
            BREAK = True
            break


    return
    

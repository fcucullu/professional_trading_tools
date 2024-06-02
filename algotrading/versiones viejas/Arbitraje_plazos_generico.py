#By Francisco Cucullu

'''                         ARBITRAJE DE PLAZOS                        '''

def arbitraje_plazos_value(ticker, q, lock, v, contador, feriados):
    import sys  #para traer varios paths con diferentes recursos
    path = r'Y:\Git\algotrading'
    path2 = r'Y:\Git\algotrading\API'
    path3 = r'Y:\Git\Funciones'
    sys.path.append(path)
    sys.path.append(path2)
    sys.path.append(path3)
    from funcionesAPI import Requests  #APIS 
    requests = Requests()
    import pandas as pd #Para manejar la info
    import FuncionesFrancisco as FF #Funciones varias
    import datetime #Para detener el algoritmo a las 16hrs (por CI)
    import traceback
    from tabulate import tabulate
    import time
    
    ##############################################################################
    '''       Identifico fines de semana y feriados para calculo de TNA       '''
    ##############################################################################
    
    if FF.weekday() == 'jueves' or FF.weekday() == 'viernes':
        TNA_days = 4 + feriados
    else:
        TNA_days = 2 + feriados    
    
    ##############################################################################
    '''                  Declaro derechos de mercado e IVA                  '''
    ##############################################################################
    
    #Lista de activos escaneados
    lista = pd.read_csv('Y:\\Git\\algotrading\\tickers.csv', sep=';', decimal=',')
    
    #Derechos de mercado
    derechos = {'acciones': 0.0008*1.21,
                'bonos': 0.0001,
                'letras': 0.00001}
    
    lista['derechos'] = lista['tipo'].map(derechos)
    
    derecho = float(lista.loc[lista['tickers'] == ticker]['derechos'])
    bono = True if lista.loc[lista['tickers'] == ticker]['tipo'].item() == 'bonos' else False
    #Lo pongo float por que luego en los condicionales no me tome pandas.series
    
    ##############################################################################
    '''                        Arranco el arbitrador                         '''
    ##############################################################################
    print('Comienza el arbitraje de plazos en '+ticker)
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < 16:
            try: #le pongo este TRY para que al encontrar un error en "i", vaya al siguiente sin detenerse
                t0 = requests.puntas(ticker, 'BCBA', 'T0')
                t2 = requests.puntas(ticker, 'BCBA', 'T2') 
                #Condicion de arbitraje 
                
                try:
                    TNA = ((t2['precioCompra']*(1-derecho))/(t0['precioVenta']*(1+derecho))-1)*(365/TNA_days)
                except:
                    TNA = 0
                
                tasa_mp = v.get()
                
                try:                        #MARK-UP
                    arbitrar = TNA > (tasa_mp + 0) and t0['precioVenta'] > 0 
                except:
                    arbitrar = False
                    
                #Ejecución
                if arbitrar == True:
                    
                    #  CRITICAL  #
                    lock.acquire() 
                    
                    ###########################
                    '''#INSERTAR EJECUTADOR#'''
                    ###########################
                    
                    trs = contador.get()
                    horario = FF.DetectaHorarioSegundos()
                    cantidad = min(t0['cantidadVenta'], t2['cantidadCompra']) 
                    tr = pd.DataFrame({'Hora': [horario, horario],
                                   '# Trade': [trs, trs],
                                   'Ticker': ticker,
                                   'C/V': ['C', 'V'],
                                   'Plazo': ['T0', 'T2'],
                                   'Cantidad': [cantidad, cantidad],
                                   'Precio': [t0['precioVenta'], t2['precioCompra']],
                                   'Monto': [-t0['precioVenta']*(1+derecho)*cantidad / (1 if bono == False else 100), 
                                             t2['precioCompra']*(1-derecho)*cantidad / (1 if bono == False else 100)],
                                   'TNA': [TNA, TNA],
                                   'Caucion': [tasa_mp, tasa_mp],
                                   'Calzada?': ['OK' if (cantidad==cantidad) else 'CERRAR',
                                                'OK' if (cantidad==cantidad) else 'CERRAR']})
                    
   
                    q.put(tr)  
                    contador.value = trs + 1
                    
                    lock.release()
                    #  CRITICAL  #
                    
                    print('Se encontro un arbitraje en {} con TNA del {}% a las {}'.format(tr['Ticker'][0], round(tr['TNA'][0]*100,2), tr['Hora'][0]))
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
    
    
import pandas as pd
import numpy as np
import datetime
import time
import sys
path = r'Y:\Git\algotrading\API'
path2 = r'Y:\Git\Funciones'
sys.path.append(path)
sys.path.append(path2)
from funcionesAPI import Requests
API = Requests()
import FuncionesFrancisco as FF
dia, mes, ano = FF.DetectaDia()
hoy=str(ano+"-"+mes+"-"+dia) 
import traceback


def streaming(cotizaciones, lock):   
    from signalr import Connection
    time.sleep(1)
    from gevent import monkey #es importante para que no salgan errores
    time.sleep(1)
    from requests import Session

    
    temp = np.array([0,1,2,3,4,5])
    lista = pd.read_csv('Y:\\Git\\algotrading\\tickers.csv', sep=';', decimal=',')
    
    for i in lista.iloc[:,2]:
        new = np.array([[float(i), 1.0, 0.0, 0.0, 0.0, 0.0],
                        [float(i), 3.0, 0.0, 0.0, 0.0, 0.0]])
        temp = np.vstack([temp, new])
    
    temp = np.delete(temp, 0, 0)
    
    lock.acquire()
    cotizaciones.value = temp 
    lock.release()
    
    print('\nComienza Streaming')
    
    session = Session()
    #create a connection
    connection = Connection("https://streaming.invertironline.com/signalr", session)
    
    #get chat hub
    chat = connection.register_hub('markethub')
    
    #start a connection
    connection.start()
    
    def print_received_message(data):
        asd(data, cotizaciones)
        
    def asd(data, cotizaciones):
        
        if [data['IDTitulo'], data['PlazoOperatoria']] in cotizaciones.value[:,0:2]: #Checkeo si el ticker me interesa
                        
            #   CRITICAL   #
            lock.acquire()
            try:
                row = np.where((cotizaciones.value[:,0] == data['IDTitulo']) & (cotizaciones.value[:,1] == data['PlazoOperatoria']))
                temp = cotizaciones.value
                temp[row,:] = np.array([data['IDTitulo'],
                                       data['PlazoOperatoria'],
                                       data['Ultimas'][0]['CantidadCompra'],
                                       data['Ultimas'][0]['PrecioCompra'],
                                       data['Ultimas'][0]['PrecioVenta'],
                                       data['Ultimas'][0]['CantidadVenta']])
                cotizaciones.value = temp
            except:
                pass               
            
            lock.release()
            #   CRITICAL   #
            
            if datetime.datetime.now().minute % 5 == 0 and datetime.datetime.now().second == 0:
                print('\nSTREAMING: ACTIVE')    
        return 
        
    #create error handler
    def print_error():
        print('ERROR')
    
    #receive new chat messages from the hub
    chat.client.on('newPuntas', print_received_message)
    
    #process errors
    connection.error += print_error
    
    
    #start a connection
    connection.start()
    connection.wait(22000) #PAra que arranque 5 minutos antes, 5 horas de mercado y un minuto despues





def streaming_MEP_inmediato(path_tickers, cotizaciones, lock):   
    from signalr import Connection
    time.sleep(1)
    from gevent import monkey #es importante para que no salgan errores
    time.sleep(1)
    from requests import Session
    #Para hacer los numeros de numpy como floats normales
    np.set_printoptions(suppress=True)

    
    DM_AlVender = (1 - 0.0001) / (1 + 0.0001)
    DM_AlComprar = (1 + 0.0001) / (1 - 0.0001)
    Banda = 0.015

    
    #ARMA TABLA DE COTIZACIONES
    temp = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
    lista = pd.read_csv(path_tickers, sep=';', decimal=',')
    
    for i in range(len(lista)):
        new = np.array([float(lista.iloc[i,1]), float(lista.iloc[i,2]), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        temp = np.vstack([temp, new])
    
    temp = np.delete(temp, 0, 0)
    lock.acquire()
    cotizaciones.value = temp 
    lock.release()
    
    
    print('\nComienza Streaming')
    
    session = Session()
    #create a connection
    connection = Connection("https://streaming.invertironline.com/signalr", session)
    
    #get chat hub
    chat = connection.register_hub('markethub')
    
    #start a connection
    connection.start()
    
    def wrapper_puntas(data):
        new_message_punta(data, cotizaciones)
        
    def wrapper_ultimo(data):
        new_message_ultimo(data, cotizaciones)
        
    def new_message_punta(data, cotizaciones):
        
        #Actualiza parte PESOS
        if (data['IDTitulo'] in cotizaciones.value[:,0]) and (data['PlazoOperatoria'] == 1): #Checkeo si el ticker me interesa
            
            #   CRITICAL   #
            lock.acquire()
            try:
                row = np.where(cotizaciones.value[:,0] == data['IDTitulo'])
                temp = cotizaciones.value
                
                temp[row,2] = data['Ultimas'][0]['CantidadCompra']
                temp[row,3] = data['Ultimas'][0]['PrecioCompra']
                temp[row,5] = data['Ultimas'][0]['PrecioVenta']
                temp[row,6] = data['Ultimas'][0]['CantidadVenta']

                #Calculo dolar mep
                #   Profundidad de puntas
                temp[row,14] = (min(temp[row,2], temp[row,12]) * temp[row,11] /100 ) //100*100
                temp[row,17] = (min(temp[row,6], temp[row,8]) * temp[row,9] /100 ) //100*100
                #   Precio del MEP considerando DM
                if (temp[row,4] != 0) and (temp[row,10] != 0): #Para calcular las bandas
                   
                    #Compra
                    if ((temp[row,3]/temp[row,4])>= (1-Banda)) and ((temp[row,11]/temp[row,10]) <= (1+Banda)) and (temp[row,11] != 0): 
                        temp[row,15] = (temp[row,3] / temp[row,11]) * DM_AlVender
                    else:
                        temp[row,15] = 0
                    #Venta
                    if ((temp[row,5]/temp[row,4]) <= (1+Banda)) and ((temp[row,9]/temp[row,10]) >= (1-Banda)) and (temp[row,9] != 0): 
                        temp[row,16] = (temp[row,5] / temp[row,9]) * DM_AlComprar
                    else:
                        temp[row,16] = 0
                    
                else:
                    temp[row,15] = 0
                    temp[row,16] = 0
                
                cotizaciones.value = temp
            except:
                pass               
            
            lock.release()
            #   CRITICAL   #
            
            # datetime.datetime.now().minute % 5 == 0 and datetime.datetime.now().second == 0:
            #    print('\nSTREAMING: ACTIVE')    
                
        #Actualiza parte DOLARES        
        if (data['IDTitulo'] in cotizaciones.value[:,1]) and (data['PlazoOperatoria'] == 1): #Checkeo si el ticker me interesa
            
            #   CRITICAL   #
            lock.acquire()
            try:
                row = np.where(cotizaciones.value[:,1] == data['IDTitulo'])
                temp = cotizaciones.value
                temp[row,8] = data['Ultimas'][0]['CantidadCompra']
                temp[row,9] = data['Ultimas'][0]['PrecioCompra']
                temp[row,11] = data['Ultimas'][0]['PrecioVenta']
                temp[row,12] = data['Ultimas'][0]['CantidadVenta']
    
                #Calculo dolar mep
                #   Profundidad de puntas
                temp[row,14] = (min(temp[row,2], temp[row,12]) * temp[row,11] /100 ) //100*100
                temp[row,17] = (min(temp[row,6], temp[row,8]) * temp[row,9] /100 ) //100*100
                #   Precio del MEP considerando DM
                if (temp[row,4] != 0) and (temp[row,10] != 0): #Para calcular las bandas
                   
                    #Compra
                    if ((temp[row,3]/temp[row,4])>= (1-Banda)) and ((temp[row,11]/temp[row,10]) <= (1+Banda)) and (temp[row,11] != 0): 
                        temp[row,15] = (temp[row,3] / temp[row,11]) * DM_AlVender
                    else:
                        temp[row,15] = 0
                    #Venta
                    if ((temp[row,5]/temp[row,4]) <= (1+Banda)) and ((temp[row,9]/temp[row,10]) >= (1-Banda)) and (temp[row,9] != 0): 
                        temp[row,16] = (temp[row,5] / temp[row,9]) * DM_AlComprar
                    else:
                        temp[row,16] = 0
                    
                else:
                    temp[row,15] = 0
                    temp[row,16] = 0

                cotizaciones.value = temp
            except:
                pass               
            
            lock.release()
            #   CRITICAL   #
            
            #if datetime.datetime.now().minute % 5 == 0 and datetime.datetime.now().second == 0:
            #    print('\nSTREAMING: ACTIVE')    
        
        return 
      
        
    def new_message_ultimo(data, cotizaciones):
       
    
        #Ultimo PESOS
        if (data['IDTitulo'] in cotizaciones.value[:,0]) and (data['PlazoOperatoria'] == 1): #Checkeo si el ticker me interesa
              
            #   CRITICAL   #
            lock.acquire()
            try:
                row = np.where(cotizaciones.value[:,0] == data['IDTitulo'])
                temp = cotizaciones.value
                temp[row, 4] = data['UltimoPrecio']
                
                #Calculo dolar mep
                #   Profundidad de puntas
                temp[row,14] = (min(temp[row,2], temp[row,12]) * temp[row,11] /100 ) //100*100
                temp[row,17] = (min(temp[row,6], temp[row,8]) * temp[row,9] /100 ) //100*100
                #   Precio del MEP considerando DM
                if (temp[row,4] != 0) and (temp[row,10] != 0): #Para calcular las bandas
                   
                    #Compra
                    if ((temp[row,3]/temp[row,4])>= (1-Banda)) and ((temp[row,11]/temp[row,10]) <= (1+Banda)) and (temp[row,11] != 0): 
                        temp[row,15] = (temp[row,3] / temp[row,11]) * DM_AlVender
                    else:
                        temp[row,15] = 0
                    #Venta
                    if ((temp[row,5]/temp[row,4]) <= (1+Banda)) and ((temp[row,9]/temp[row,10]) >= (1-Banda)) and (temp[row,9] != 0): 
                        temp[row,16] = (temp[row,5] / temp[row,9]) * DM_AlComprar
                    else:
                        temp[row,16] = 0
                    
                else:
                    temp[row,15] = 0
                    temp[row,16] = 0

                cotizaciones.value = temp
            except:
                pass               
            
            lock.release()
            #   CRITICAL   #
            
            #if datetime.datetime.now().minute % 5 == 0 and datetime.datetime.now().second == 0:
            #    print('\nSTREAMING: ACTIVE')    
            
        #Ultimo DOLARES  
        if (data['IDTitulo'] in cotizaciones.value[:,1]) and (data['PlazoOperatoria'] == 1): #Checkeo si el ticker me interesa
                        
            #   CRITICAL   #
            lock.acquire()
            try:
                row = np.where(cotizaciones.value[:,1] == data['IDTitulo'])
                temp = cotizaciones.value
                temp[row, 10] = data['UltimoPrecio']
                
                #Calculo dolar mep
                #   Profundidad de puntas
                temp[row,14] = (min(temp[row,2], temp[row,12]) * temp[row,11] /100 ) //100*100
                temp[row,17] = (min(temp[row,6], temp[row,8]) * temp[row,9] /100 ) //100*100
                #   Precio del MEP considerando DM
                if (temp[row,4] != 0) and (temp[row,10] != 0): #Para calcular las bandas
                   
                    #Compra
                    if ((temp[row,3]/temp[row,4])>= (1-Banda)) and ((temp[row,11]/temp[row,10]) <= (1+Banda)) and (temp[row,11] != 0): 
                        temp[row,15] = (temp[row,3] / temp[row,11]) * DM_AlVender
                    else:
                        temp[row,15] = 0
                    #Venta
                    if ((temp[row,5]/temp[row,4]) <= (1+Banda)) and ((temp[row,9]/temp[row,10]) >= (1-Banda)) and (temp[row,9] != 0): 
                        temp[row,16] = (temp[row,5] / temp[row,9]) * DM_AlComprar
                    else:
                        temp[row,16] = 0
                    
                else:
                    temp[row,15] = 0
                    temp[row,16] = 0

                cotizaciones.value = temp
            except:
                pass               
            
            lock.release()
            #   CRITICAL   #
            
            #if datetime.datetime.now().minute % 5 == 0 and datetime.datetime.now().second == 0:
            #    print('\nSTREAMING: ACTIVE')    

        return 

        
    #create error handler
    def print_error():
        print('ERROR')
    
    #receive new chat messages from the hub
    chat.client.on('newPuntas', wrapper_puntas)
    chat.client.on('newCotizacion', wrapper_ultimo)
    
    #process errors
    connection.error += print_error
    
    
    #start a connection
    connection.start()
    connection.wait(22000) #PAra que arranque 5 minutos antes, 5 horas de mercado y un minuto despues

'''
  0  |   1  | 2 | 3 |  4  | 5 | 6 |7|  8 |  9 |  10  | 11 | 12 |13|  14 | 15| 16| 17 |
Bono$|BonoU$|Qc$|Pc$|Last$|Pv$|Qv$|0|QcU$|PcU$|LastU$|PcU$|QvUS|0 |ProfC|TCc|TCv|ProfV
'''

''' PUNTAS 
{'IDTitulo': 83755,
 'PlazoOperatoria': 3,
 'Ultimas': [{'CantidadCompra': 3011.0, 'PrecioCompra': 54.35, 'PrecioVenta': 54.45, 'CantidadVenta': 4000.0, 'TasaCompra': 0.0, 'TasaVenta': 0.0}, {'CantidadCompra': 500.0, 'PrecioCompra': 54.3, 'PrecioVenta': 54.5, 'CantidadVenta': 2044.0, 'TasaCompra': 0.0, 'TasaVenta': 0.0}, {'CantidadCompra': 4906.0, 'PrecioCompra': 54.25, 'PrecioVenta': 54.55, 'CantidadVenta': 1000.0, 'TasaCompra': 0.0, 'TasaVenta': 0.0}, {'CantidadCompra': 1100.0, 'PrecioCompra': 54.2, 'PrecioVenta': 54.65, 'CantidadVenta': 3390.0, 'TasaCompra': 0.0, 'TasaVenta': 0.0}, {'CantidadCompra': 5750.0, 'PrecioCompra': 54.0, 'PrecioVenta': 54.8, 'CantidadVenta': 13953.0, 'TasaCompra': 0.0, 'TasaVenta': 0.0}]}
'''

''' ULTIMO OPERADO
{'IDTitulo': 88094,
 'UltimoPrecio': 67.0,
 'Variacion': -0.14,
 'VariacionPuntos': -0.1,
 'Tendencia': 0,
 'FechaHoraFormated': '12:15',
 'Apertura': 67.5,
 'Maximo': 67.5,
 'Minimo': 67.0,
 'UltimoCierre': 67.1,
 'VolumenNominal': 20144.0,
 'CantidadOperaciones': 10,
 'PrecioAjuste': 0.0,
 'InteresesAbiertos': 0.0,
 'PlazoOperatoria': 3,
 'FechaHora': '2019-05-22T12:15:07.023501-03:00',
 'MontoOperado': 13533.18,
 'UltimaTasa': 0.0}
'''

def control_streaming(hora_stop, path_tickers, cotizaciones, control_ok):
    print('\nComienza el control de streaming')
    
    def checkear(row):
        fila = np.where(cotizaciones.value[:,0] == row[1])
        puntasP = API.puntas(row[0], 'BCBA', 'T0')
        puntaCP_api = puntasP['precioCompra']
        puntaVP_api = puntasP['precioVenta']
        puntasD = API.puntas(row[0]+"D", 'BCBA', 'T0')
        puntaCD_api = puntasD['precioCompra']
        puntaVD_api = puntasD['precioVenta']
        condiciones = [True if (cotizaciones.value[fila,3] == 0 or cotizaciones.value[fila,3] == puntaCP_api) else False,
                       True if (cotizaciones.value[fila,5] == 0 or cotizaciones.value[fila,5] == puntaVP_api) else False,
                       True if (cotizaciones.value[fila,9] == 0 or cotizaciones.value[fila,9] == puntaCD_api) else False,
                       True if (cotizaciones.value[fila,11] == 0 or cotizaciones.value[fila,11] == puntaVD_api) else False]
        if condiciones == [True, True, True, True]:
            check = True
        else:
            check = False
        return check
    
    print('Control streaming aguarda un minuto')
    time.sleep(60)    
    lista = pd.read_csv(path_tickers, sep=';', decimal=',')
    now = datetime.datetime.now()
    BREAK = False
    control = list([0]*len(lista))
    
    while BREAK == False:
        if now.hour < hora_stop:

            try:
                for index, row in lista.iterrows():
                    check = checkear(row)
                    if check == False:
                        check = checkear(row)
                        if check == False:
                            check = checkear(row)
                    
                    if check == True:
                        control[index] = 0
                        
                    if check == False:
                        print('ERROR EN STREAMING CON {}'.format(row[0]))
                        control_ok.value = 1 #Le pongo un valor diferente de cero para frenar el arbitrador.
                        control[index] = 1
                        
                if (control == list([0]*len(lista))) and (control_ok.value == 1):
                    control_ok.value = 0 #Le pongo un valor igual a cero para habilitar el arbitrador.
                    print('SE RESTABLECE STREAMING')
                    
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR EN EL CONTROL DE STREAMING --- ')
                traceback.print_exc()
                continue    
        else:
            BREAK = True
            print('\nSe detiene el control de streaming.')    
            break
           
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    
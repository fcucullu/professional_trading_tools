#By Francisco Cucullu

#Todo este bloque tarda 0.0 segundos en cargar
import sys
path = r'Y:\Git\algotrading\API'
path2 = r'Y:\Git\Funciones'
sys.path.append(path)
sys.path.append(path2)
from funcionesAPI import Sandbox
sandbox = Sandbox()
import FuncionesFrancisco as FF
dia, mes, ano = FF.DetectaDia()
hoy=str(ano+"-"+mes+"-"+dia) 
import time
import datetime
import traceback

import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
pd.options.mode.chained_assignment = None  # Para que no printee warnings
pd.options.display.float_format = '{:20,.2f}'.format #Para evitar la cientific notation
credenciales = {'TUserName': 'automatizacioncucu', 
                'tpassword': 'jackperro02',
                'submit1': 'Aceptar',
                'goto': ''}



def flujo_compra_dolar(hora_stop, inputs_compra, tr_compra, lock, semaforo, token):
    
    print('\nComienza el ejecutador de compras')
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < hora_stop:
    
            try:
                
                if inputs_compra.value != 0:
                    deteccion = FF.DetectaHorarioSegundos()
                    print('COMPRA ENVIADA a las: {}. {} {}@{}'.format(deteccion,inputs_compra.value[0],inputs_compra.value[1],inputs_compra.value[2]))
                    
                    tr_compra.value = sandbox.comprar(inputs_compra.value[0], inputs_compra.value[1], inputs_compra.value[2], 'T0', inputs_compra.value[3], token)
                    
                    while tr_compra.value == 0: #Espero hasta que la orden este generada
                            time.sleep(0.0001)
                    
                    horario = FF.DetectaHorarioSegundos()
                    print('COMPRA INICIADA a las {}'.format(horario))
                            
                    while sandbox.tr_check(tr_compra.value, token)[0] == 'iniciada': #espero hasta que la tr este en proceso (llego al mercado)
                        time.sleep(0.0001) 
                    print('COMPRA EN PROCESO a las: {}'.format(FF.DetectaHorarioSegundos()))
                    
                    time.sleep(30)
                    try:
                        tr_compra.value = inputs_compra.value[0], sandbox.tr_delete(tr_compra.value, token), deteccion, tr_compra.value
                    except:
                        print('\nERROR AL CANCELAR LA COMPRA ({})'.format(tr_compra.value))
                        traceback.print_exc()
                        
#################### '''S T A R T  of  C R I T I C A L  Z O N E'''
                    lock.acquire()
                    
                    inputs_compra.value = 0 #retorno el valor de la compra a cero
                    semaforo.value += 2 #Le da la señal el arbitrador para seguir
                    
                    lock.release()
#################### '''E N D  of  C R I T I C A L  Z O N E'''
                
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR EN EL SCRIPT DE FLUJO DE COMPRA --- ')
                inputs_compra.value = 0
                tr_compra.value = 0
                semaforo.value = 0
                traceback.print_exc()
                continue    
                    
        else:
            BREAK = True
            print('\nSe detiene el ejecutador de compras')
            break
        
    return

def flujo_venta_dolar(hora_stop, inputs_venta, tr_venta, lock, semaforo, token):
    
    print('\nComienza el ejecutador de ventas')
    
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < hora_stop:
            
            try:
                
                if inputs_venta.value != 0:
                    deteccion = FF.DetectaHorarioSegundos()
                    print('VENTA ENVIADA a las: {}. {} {}@{}'.format(deteccion,inputs_venta.value[0],inputs_venta.value[1],inputs_venta.value[2]))
                    
                    tr_venta.value = sandbox.vender(inputs_venta.value[0], inputs_venta.value[1], inputs_venta.value[2], 'T0', inputs_venta.value[3], token)
                    
                    while tr_venta.value == 0: #Espero hasta que la orden este generada
                        time.sleep(0.0001)
    
                    horario = FF.DetectaHorarioSegundos()
                    print('VENTA INICIADA a las {}'.format(horario))
            
                    while sandbox.tr_check(tr_venta.value, token)[0] == 'iniciada': #espero hasta que la tr este en proceso (llego al mercado)
                        time.sleep(0.0001) 
                    print('VENTA EN PROCESO a las: {}'.format(FF.DetectaHorarioSegundos()))
                    
                    time.sleep(30)
                    try:
                        tr_venta.value = inputs_venta.value[0], sandbox.tr_delete(tr_venta.value, token), deteccion, tr_venta.value
                    except:
                        print('\nERROR AL CANCELAR LA VENTA ({})'.format(tr_venta.value))
                        traceback.print_exc()
                    
                    
#################### '''S T A R T  of  C R I T I C A L  Z O N E'''
                    lock.acquire()
                    
                    inputs_venta.value = 0 #retorno el valor de la compra a cero
                    semaforo.value += 2 #Le da la señal el arbitrador para seguir
                    
                    lock.release()
#################### '''E N D  of  C R I T I C A L  Z O N E'''
               
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR EN EL SCRIPT DE FLUJO DE VENTA --- ')
                inputs_venta.value = 0
                tr_venta.value = 0
                semaforo.value = 0
                traceback.print_exc()
                continue    
                            
        else:
            BREAK = True
            print('\nSe detiene el ejecutador de ventas')
            break
    
    return



def compra_CI_por_iolnet(comitente, ticker, precio, cantidad):
    #Me loggeo para obtener cookies
    session = rq.Session()
    r = session.post('http://iolnet.invertir.local/login.asp', data=credenciales)
    cookies = session.cookies.get_dict() 
    
    #Le pego a alta de transaccion
    data = {'Permiso_Saldo_Insuficiente': 0,
            'Permiso_Saldo_Insuficiente_Monto': 1,
            'CTipo': 1,
            'TNumeCuen': comitente,
            'CMercado': 1,
            'TSimbolox': ticker,
            'TCantidad': cantidad,
            'TMercado': precio,
            'XPlazo': 3,
            'ID_Fuente': 5,
            'ID_Fuente_IFFI': 4,
            'Grabar': 'Grabar',
            'esiffi': '',
            'brokerto': 0}
   
    r = session.post('http://iolnet.invertir.local/Transacciones/Inmediatas.asp?Grabar=1', cookies=cookies, data=data)
    #Extraigo la fecha y la hora de la transaccion generada
    soup = bs(r.content, 'lxml')      
    
    
    tabla = soup.find_all('table')[9]
    l = []
    for tr in tabla:
        try:
            td = tr.find_all('td')
            row = [tr.text.rstrip() for tr in td] #el text es para sacar solo el valor de texto y el rstrip es para sacarle los espacios al final del string
            for i in range(len(row)):
                row[i] = row[i].replace('\n','')
                row[i] = row[i].replace('\t','')
                row[i] = row[i].replace('\r','')
            l.append(row)
        except:
            pass
    tabla = pd.DataFrame(l)
    tabla.columns = tabla.iloc[0]
    tabla = tabla.reindex(tabla.index.drop(0))
    XFechLogx = tabla.loc[tabla['Comitente IOL'] == str(comitente), 'Fecha'].item()
    
    
    data= {'Grabar': 2,
           'XID_Cliente': 595257, #Pedir a IT. Es equivalente al CC pero en otra tabla
           'XID_Tipo_Transaccion': 1,
           'XFechLogx': XFechLogx}
    
    r = session.post('http://iolnet.invertir.local/Transacciones/Inmediatas.asp?Grabar=2', cookies=cookies, data=data)
    #Extraigo el numero de la transaccion generada
    soup = bs(r.content, 'lxml')        
    tr = soup.find_all('table')[9].findAll('td')[0]
    tr = int(tr.text[-8:])
    
    return tr



def venta_CI_por_iolnet(comitente, ticker, precio, cantidad):
    #Me loggeo para obtener cookies
    session = rq.Session()
    r = session.post('http://iolnet.invertir.local/login.asp', data=credenciales)
    cookies = session.cookies.get_dict() 
    
    #Le pego a alta de transaccion
    data = {'Permiso_Saldo_Insuficiente': 0,
            'Permiso_Saldo_Insuficiente_Monto': 0,
            'CTipo': 2,
            'TNumeCuen': comitente,
            'CMercado': 1,
            'TSimbolox': ticker,
            'TCantidad': cantidad,
            'TMercado': precio,
            'XPlazo': 3,
            'ID_Fuente': 5,
            'ID_Fuente_IFFI': 4,
            'Grabar': 'Grabar',
            'esiffi': '',
            'brokerto': 0}
   
    r = session.post('http://iolnet.invertir.local/Transacciones/Inmediatas.asp?Grabar=1', cookies=cookies, data=data)
    #Extraigo la fecha y la hora de la transaccion generada
    soup = bs(r.content, 'lxml')    
    
    tabla = soup.find_all('table')[9]
    l = []
    for tr in tabla:
        try:
            td = tr.find_all('td')
            row = [tr.text.rstrip() for tr in td] #el text es para sacar solo el valor de texto y el rstrip es para sacarle los espacios al final del string
            for i in range(len(row)):
                row[i] = row[i].replace('\n','')
                row[i] = row[i].replace('\t','')
                row[i] = row[i].replace('\r','')
            l.append(row)
        except:
            pass
    tabla = pd.DataFrame(l)
    tabla.columns = tabla.iloc[0]
    tabla = tabla.reindex(tabla.index.drop(0))
    XFechLogx = tabla.loc[tabla['Comitente IOL'] == str(comitente), 'Fecha'].item()

    data= {'Grabar': 2,
           'XID_Cliente': 595257, #Es una equivalencia del CC en otra tabla. Preguntar a IT.
           'XID_Tipo_Transaccion': 2,
           'XFechLogx': XFechLogx}
    
    r = session.post('http://iolnet.invertir.local/Transacciones/Inmediatas.asp?Grabar=2', cookies=cookies, data=data)
    #Extraigo el numero de la transaccion generada
    soup = bs(r.content, 'lxml')        
    tr = soup.find_all('table')[9].findAll('td')[0]
    tr = int(tr.text[-8:])
    
    return tr




def flujo_operatoria_xiolnet(hora_stop, inputs_compra, inputs_venta, tr_compra, tr_venta, lock, semaforo, token):
    
    print('\nComienza el ejecutador de operaciones por IOLNet')
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < hora_stop:
    
            try:
                
                if inputs_compra.value != 0:
                    deteccion = FF.DetectaHorarioSegundos()
                    print('COMPRA ENVIADA a las: {}. {} {}@{}'.format(deteccion,inputs_compra.value[0],inputs_compra.value[1],inputs_compra.value[2]))
                    
                    #tr_compra.value = sandbox.comprar(inputs_compra.value[0], inputs_compra.value[1], inputs_compra.value[2], 'T0', inputs_compra.value[3], token)
                    tr_compra.value = compra_CI_por_iolnet(127, inputs_compra.value[0], inputs_compra.value[2], inputs_compra.value[1])
                    
                    while tr_compra.value == 0: #Espero hasta que la orden este generada
                            time.sleep(0.0001)
                    
                    horario = FF.DetectaHorarioSegundos()
                    print('COMPRA INICIADA a las {}'.format(horario))
                            
                    while sandbox.tr_check(tr_compra.value, token)[0] == 'iniciada': #espero hasta que la tr este en proceso (llego al mercado)
                        time.sleep(0.0001) 
                    print('COMPRA EN PROCESO a las: {}'.format(FF.DetectaHorarioSegundos()))
                    
                    time.sleep(3)
                    try:
                        tr_compra.value = inputs_compra.value[0], sandbox.tr_delete(tr_compra.value, token), deteccion, tr_compra.value
                    except:
                        print('\nERROR AL CANCELAR LA COMPRA ({})'.format(tr_compra.value))
                        traceback.print_exc()
                        
#################### '''S T A R T  of  C R I T I C A L  Z O N E'''
                    lock.acquire()
                    
                    inputs_compra.value = 0 #retorno el valor de la compra a cero
                    semaforo.value += 2 #Le da la señal el arbitrador para seguir
                    
                    lock.release()
#################### '''E N D  of  C R I T I C A L  Z O N E'''
                
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR EN EL SCRIPT DE FLUJO DE COMPRA --- ')
                inputs_compra.value = 0
                tr_compra.value = 0
                semaforo.value = 0
                traceback.print_exc()
                continue    
                    
            #AQUI COMIENZA LA VENTA -> OPERACIONES SECUENCIALES POR IOLNET
            try:
                
                if inputs_venta.value != 0:
                    deteccion = FF.DetectaHorarioSegundos()
                    print('VENTA ENVIADA a las: {}. {} {}@{}'.format(deteccion,inputs_venta.value[0],inputs_venta.value[1],inputs_venta.value[2]))
                
                    #tr_venta.value = sandbox.vender(inputs_venta.value[0], inputs_venta.value[1], inputs_venta.value[2], 'T0', inputs_venta.value[3], token)
                    tr_venta.value = venta_CI_por_iolnet(127, inputs_venta.value[0], inputs_venta.value[2], tr_compra.value[1][1][0]) #Le pongo input de compra para que venda lo mismo que ejecuto la compra
                    
                    while tr_venta.value == 0: #Espero hasta que la orden este generada
                        time.sleep(0.0001)
    
                    horario = FF.DetectaHorarioSegundos()
                    print('VENTA INICIADA a las {}'.format(horario))
            
                    while sandbox.tr_check(tr_venta.value, token)[0] == 'iniciada': #espero hasta que la tr este en proceso (llego al mercado)
                        time.sleep(0.0001) 
                    print('VENTA EN PROCESO a las: {}'.format(FF.DetectaHorarioSegundos()))
                    
                    time.sleep(3)
                    try:
                        tr_venta.value = inputs_venta.value[0], sandbox.tr_delete(tr_venta.value, token), deteccion, tr_venta.value
                    except:
                        print('\nERROR AL CANCELAR LA VENTA ({})'.format(tr_venta.value))
                        traceback.print_exc()
                    
                    
#################### '''S T A R T  of  C R I T I C A L  Z O N E'''
                    lock.acquire()
                    
                    inputs_venta.value = 0 #retorno el valor de la compra a cero
                    semaforo.value += 2 #Le da la señal el arbitrador para seguir
                    
                    lock.release()
#################### '''E N D  of  C R I T I C A L  Z O N E'''
               
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR EN EL SCRIPT DE FLUJO DE VENTA --- ')
                inputs_venta.value = 0
                tr_venta.value = 0
                semaforo.value = 0
                traceback.print_exc()
                continue    
                            
        else:
            BREAK = True
            print('\nSe detiene el ejecutador de ventas')
            break
    
    return


def flujo_operatoria_secuencial(hora_stop, inputs_compra, inputs_venta, tr_compra, tr_venta, lock, semaforo, token):
    
    print('\nComienza el ejecutador de operaciones por IOLNet SECUENCIAL')
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < hora_stop:
    
            try:
                
                if inputs_compra.value != 0:
                    deteccion = FF.DetectaHorarioSegundos()
                    print('COMPRA ENVIADA a las: {}. {} {}@{}'.format(deteccion,inputs_compra.value[0],inputs_compra.value[1],inputs_compra.value[2]))
                    
                    #tr_compra.value = sandbox.comprar(inputs_compra.value[0], inputs_compra.value[1], inputs_compra.value[2], 'T0', inputs_compra.value[3], token)
                    tr_compra.value = sandbox.comprar(inputs_compra.value[0], inputs_compra.value[1], inputs_compra.value[2], 'T0', inputs_compra.value[3], token)
                    
                    while tr_compra.value == 0: #Espero hasta que la orden este generada
                            time.sleep(0.0001)
                    
                    horario = FF.DetectaHorarioSegundos()
                    print('COMPRA INICIADA a las {}'.format(horario))
                            
                    while sandbox.tr_check(tr_compra.value, token)[0] == 'iniciada': #espero hasta que la tr este en proceso (llego al mercado)
                        time.sleep(0.0001) 
                    print('COMPRA EN PROCESO a las: {}'.format(FF.DetectaHorarioSegundos()))
                    
                    time.sleep(3)
                    try:
                        tr_compra.value = inputs_compra.value[0], sandbox.tr_delete(tr_compra.value, token), deteccion, tr_compra.value
                    except:
                        print('\nERROR AL CANCELAR LA COMPRA ({})'.format(tr_compra.value))
                        traceback.print_exc()
                        
#################### '''S T A R T  of  C R I T I C A L  Z O N E'''
                    lock.acquire()
                    
                    inputs_compra.value = 0 #retorno el valor de la compra a cero
                    semaforo.value += 2 #Le da la señal el arbitrador para seguir
                    
                    lock.release()
#################### '''E N D  of  C R I T I C A L  Z O N E'''
                
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR EN EL SCRIPT DE FLUJO DE COMPRA --- ')
                inputs_compra.value = 0
                tr_compra.value = 0
                semaforo.value = 0
                traceback.print_exc()
                continue    
                    
            #AQUI COMIENZA LA VENTA -> OPERACIONES SECUENCIALES POR IOLNET
            try:
                
                if inputs_venta.value != 0:
                    if tr_compra.value[1][1][0] != 0:
                        
                        deteccion = FF.DetectaHorarioSegundos()
                        print('VENTA ENVIADA a las: {}. {} {}@{}'.format(deteccion,inputs_venta.value[0],tr_compra.value[1][1][0],inputs_venta.value[2]))
                        
                        #Le pongo input de compra para que venda lo mismo que ejecuto la compra
                        tr_venta.value = sandbox.vender(inputs_venta.value[0], tr_compra.value[1][1][0], inputs_venta.value[2], 'T0', inputs_venta.value[3], token)
                        
                        while tr_venta.value == 0: #Espero hasta que la orden este generada
                            time.sleep(0.0001)
        
                        horario = FF.DetectaHorarioSegundos()
                        print('VENTA INICIADA a las {}'.format(horario))
                
                        while sandbox.tr_check(tr_venta.value, token)[0] == 'iniciada': #espero hasta que la tr este en proceso (llego al mercado)
                            time.sleep(0.0001) 
                        print('VENTA EN PROCESO a las: {}'.format(FF.DetectaHorarioSegundos()))
                        
                        time.sleep(3)
                        try:
                            tr_venta.value = inputs_venta.value[0], sandbox.tr_delete(tr_venta.value, token), deteccion, tr_venta.value
                        except:
                            print('\nERROR AL CANCELAR LA VENTA ({})'.format(tr_venta.value))
                            traceback.print_exc()
                        
                        
####################### '''S T A R T  of  C R I T I C A L  Z O N E'''
                        lock.acquire()
                        
                        inputs_venta.value = 0 #retorno el valor de la compra a cero
                        semaforo.value += 2 #Le da la señal el arbitrador para seguir
                        
                        lock.release()
####################### '''E N D  of  C R I T I C A L  Z O N E'''
                        
                    else: #PARA EL CASO EN QUE NO SE EJECUTA NADA EN LA COMPRA
####################### '''S T A R T  of  C R I T I C A L  Z O N E'''
                        lock.acquire()
                        
                        inputs_venta.value = 0 #retorno el valor de la compra a cero
                        semaforo.value += 2 #Le da la señal el arbitrador para seguir
                        
                        lock.release()
####################### '''E N D  of  C R I T I C A L  Z O N E'''
               
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR EN EL SCRIPT DE FLUJO DE VENTA --- ')
                inputs_venta.value = 0
                tr_venta.value = 0
                semaforo.value = 0
                traceback.print_exc()
                continue    
                            
        else:
            BREAK = True
            print('\nSe detiene el ejecutador de ventas')
            break
    
    return





def comprar_dolar_supv(monto):
    credenciales = {'Username': 'algotrading', 
                'Password': 'fcucullu1'}
    #Me loggeo para obtener cookies
    session = rq.Session()
    session.post('https://dolar.invertironline.com/User/Login', data=credenciales)
    data= {'MonedaMontoExpresado': 2,
           'Monto': monto}
    session.post('https://dolar.invertironline.com/Comprar/Confirmar', data=data)
    session.post('https://dolar.invertironline.com/Comprar/ConfirmarCompra')
    
def vender_dolar_supv(monto):
    credenciales = {'Usuario': 'algotrading', 
                'Password': 'fcucullu1'}
    #Me loggeo para obtener cookies
    session = rq.Session()
    session.post('https://micuenta.invertironline.com/ingresar?url=https://dolar.invertironline.com/', data=credenciales)
    data= {'MonedaMontoExpresado': 2,
           'Monto': monto}
    session.post('https://dolar.invertironline.com/Vender/Confirmar', data=data)
    session.post('https://dolar.invertironline.com/Vender/ConfirmarVenta')
 
# bs(r.content, 'xml')
#####################################################################################
    
    
def comprar_dolar_supv_testing(monto):
    credenciales = {'Username': 'algotrading997', 
                'Password': 'testeo123'}
    #Me loggeo para obtener cookies
    session = rq.Session()
    session.post('http://dolar.testing.invertironline.com/User/Login', data=credenciales)
    data= {'MonedaMontoExpresado': 2,
           'Monto': monto}
    session.post('http://dolar.testing.invertironline.com/Comprar/Confirmar', data=data)
    session.post('http://dolar.testing.invertironline.com/Comprar/ConfirmarCompra')
    
def vender_dolar_supv_testing(monto):
    credenciales = {'Username': 'algotrading997', 
                'Password': 'testeo123'}
    #Me loggeo para obtener cookies
    session = rq.Session()
    session.post('http://dolar.testing.invertironline.com/User/Login', data=credenciales)
    data= {'MonedaMontoExpresado': 2,
           'Monto': monto}
    session.post('http://dolar.testing.invertironline.com/Vender/Confirmar', data=data)
    session.post('http://dolar.testing.invertironline.com/Vender/ConfirmarVenta')

def compra_CI_por_iolnet_testing(comitente, ticker, precio, cantidad):
    
    credenciales = {'TUserName': 'apensel', 
                'tpassword': 'testeo123',
                'submit1': 'Aceptar',
                'goto': ''}
    
    #Me loggeo para obtener cookies
    session = rq.Session()
    r = session.post('http://testing-iolnet/login.asp', data=credenciales)
    cookies = session.cookies.get_dict() 
    
    #Le pego a alta de transaccion
    data = {'Permiso_Saldo_Insuficiente': 0,
            'Permiso_Saldo_Insuficiente_Monto': 0,
            'CTipo': 1,
            'TNumeCuen': comitente,
            'CMercado': 1,
            'TSimbolox': ticker,
            'TCantidad': cantidad,
            'TMercado': precio,
            'XPlazo': 3,
            'ID_Fuente': 5,
            'ID_Fuente_IFFI': 4,
            'Grabar': 'Grabar',
            'esiffi': '',
            'brokerto': 0}
   
    r = session.post('http://testing-iolnet/Transacciones/Inmediatas.asp?Grabar=1', cookies=cookies, data=data)
    #Extraigo la fecha y la hora de la transaccion generada
    soup = bs(r.content, 'lxml')      
    
    
    tabla = soup.find_all('table')[9]
    l = []
    for tr in tabla:
        try:
            td = tr.find_all('td')
            row = [tr.text.rstrip() for tr in td] #el text es para sacar solo el valor de texto y el rstrip es para sacarle los espacios al final del string
            for i in range(len(row)):
                row[i] = row[i].replace('\n','')
                row[i] = row[i].replace('\t','')
                row[i] = row[i].replace('\r','')
            l.append(row)
        except:
            pass
    tabla = pd.DataFrame(l)
    tabla.columns = tabla.iloc[0]
    tabla = tabla.reindex(tabla.index.drop(0))
    XFechLogx = tabla.loc[tabla['Comitente IOL'] == str(comitente), 'Fecha'].item()
    
    
    data= {'Grabar': 2,
           'XID_Cliente': 538014, #Pedir a IT. Es equivalente al CC pero en otra tabla
           'XID_Tipo_Transaccion': 1,
           'XFechLogx': XFechLogx}
    
    r = session.post('http://testing-iolnet/Transacciones/Inmediatas.asp?Grabar=2', cookies=cookies, data=data)
    #Extraigo el numero de la transaccion generada
    soup = bs(r.content, 'lxml')        
    tr = soup.find_all('table')[9].findAll('td')[0]
    tr = int(tr.text[-8:])
    
    return tr



def venta_CI_por_iolnet_testing(comitente, ticker, precio, cantidad):
    
    credenciales = {'TUserName': 'apensel', 
                'tpassword': 'testeo123',
                'submit1': 'Aceptar',
                'goto': ''}

    #Me loggeo para obtener cookies
    session = rq.Session()
    r = session.post('http://testing-iolnet/login.asp', data=credenciales)
    cookies = session.cookies.get_dict() 
    
    #Le pego a alta de transaccion
    data = {'Permiso_Saldo_Insuficiente': 0,
            'Permiso_Saldo_Insuficiente_Monto': 0,
            'CTipo': 2,
            'TNumeCuen': comitente,
            'CMercado': 1,
            'TSimbolox': ticker,
            'TCantidad': cantidad,
            'TMercado': precio,
            'XPlazo': 3,
            'ID_Fuente': 5,
            'ID_Fuente_IFFI': 4,
            'Grabar': 'Grabar',
            'esiffi': '',
            'brokerto': 0}
   
    r = session.post('http://testing-iolnet/Transacciones/Inmediatas.asp?Grabar=1', cookies=cookies, data=data)
    #Extraigo la fecha y la hora de la transaccion generada
    soup = bs(r.content, 'lxml')    
    
    tabla = soup.find_all('table')[9]
    l = []
    for tr in tabla:
        try:
            td = tr.find_all('td')
            row = [tr.text.rstrip() for tr in td] #el text es para sacar solo el valor de texto y el rstrip es para sacarle los espacios al final del string
            for i in range(len(row)):
                row[i] = row[i].replace('\n','')
                row[i] = row[i].replace('\t','')
                row[i] = row[i].replace('\r','')
            l.append(row)
        except:
            pass
    tabla = pd.DataFrame(l)
    tabla.columns = tabla.iloc[0]
    tabla = tabla.reindex(tabla.index.drop(0))
    XFechLogx = tabla.loc[tabla['Comitente IOL'] == str(comitente), 'Fecha'].item()

    data= {'Grabar': 2,
           'XID_Cliente': 538014, #Es una equivalencia del CC en otra tabla. Preguntar a IT.
           'XID_Tipo_Transaccion': 2,
           'XFechLogx': XFechLogx}
    
    r = session.post('http://testing-iolnet/Transacciones/Inmediatas.asp?Grabar=2', cookies=cookies, data=data)
    #Extraigo el numero de la transaccion generada
    soup = bs(r.content, 'lxml')        
    tr = soup.find_all('table')[9].findAll('td')[0]
    tr = int(tr.text[-8:])
    
    return tr


def flujo_operatoria_xiolnet_testing(hora_stop, inputs_compra, inputs_venta, tr_compra, tr_venta, lock, semaforo, token):
    
    print('\nComienza el ejecutador de operaciones por IOLNet - TESTING')
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < hora_stop:
    
            try:
                
                if inputs_compra.value != 0:
                    deteccion = FF.DetectaHorarioSegundos()
                    print('COMPRA ENVIADA a las: {}. {} {}@{}'.format(deteccion,inputs_compra.value[0],inputs_compra.value[1],inputs_compra.value[2]))
                    
                    #tr_compra.value = sandbox.comprar(inputs_compra.value[0], inputs_compra.value[1], inputs_compra.value[2], 'T0', inputs_compra.value[3], token)
                    tr_compra.value = compra_CI_por_iolnet_testing(99165, inputs_compra.value[0], inputs_compra.value[2], inputs_compra.value[1])
                    
                    while tr_compra.value == 0: #Espero hasta que la orden este generada
                            time.sleep(0.0001)
                    
                    horario = FF.DetectaHorarioSegundos()
                    print('COMPRA INICIADA a las {}'.format(horario))
                            
                    while sandbox.tr_check(tr_compra.value, token)[0] == 'iniciada': #espero hasta que la tr este en proceso (llego al mercado)
                        time.sleep(0.0001) 
                    print('COMPRA EN PROCESO a las: {}'.format(FF.DetectaHorarioSegundos()))
                    
                    time.sleep(3)
                    try:
                        tr_compra.value = inputs_compra.value[0], sandbox.tr_delete(tr_compra.value, token), deteccion, tr_compra.value
                    except:
                        print('\nERROR AL CANCELAR LA COMPRA ({})'.format(tr_compra.value))
                        traceback.print_exc()
                        
#################### '''S T A R T  of  C R I T I C A L  Z O N E'''
                    lock.acquire()
                    
                    inputs_compra.value = 0 #retorno el valor de la compra a cero
                    semaforo.value += 2 #Le da la señal el arbitrador para seguir
                    
                    lock.release()
#################### '''E N D  of  C R I T I C A L  Z O N E'''
                
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR EN EL SCRIPT DE FLUJO DE COMPRA --- ')
                inputs_compra.value = 0
                tr_compra.value = 0
                semaforo.value = 0
                traceback.print_exc()
                continue    
                    
            #AQUI COMIENZA LA VENTA -> OPERACIONES SECUENCIALES POR IOLNET
            try:
                
                if inputs_venta.value != 0:
                    deteccion = FF.DetectaHorarioSegundos()
                    print('VENTA ENVIADA a las: {}. {} {}@{}'.format(deteccion,inputs_venta.value[0],inputs_venta.value[1],inputs_venta.value[2]))
                
                    #tr_venta.value = sandbox.vender(inputs_venta.value[0], inputs_venta.value[1], inputs_venta.value[2], 'T0', inputs_venta.value[3], token)
                    tr_venta.value = venta_CI_por_iolnet_testing(99165, inputs_venta.value[0], inputs_venta.value[2], inputs_venta.value[1])
                    
                    while tr_venta.value == 0: #Espero hasta que la orden este generada
                        time.sleep(0.0001)
    
                    horario = FF.DetectaHorarioSegundos()
                    print('VENTA INICIADA a las {}'.format(horario))
            
                    while sandbox.tr_check(tr_venta.value, token)[0] == 'iniciada': #espero hasta que la tr este en proceso (llego al mercado)
                        time.sleep(0.0001) 
                    print('VENTA EN PROCESO a las: {}'.format(FF.DetectaHorarioSegundos()))
                    
                    time.sleep(3)
                    try:
                        tr_venta.value = inputs_venta.value[0], sandbox.tr_delete(tr_venta.value, token), deteccion, tr_venta.value
                    except:
                        print('\nERROR AL CANCELAR LA VENTA ({})'.format(tr_venta.value))
                        traceback.print_exc()
                    
                    
#################### '''S T A R T  of  C R I T I C A L  Z O N E'''
                    lock.acquire()
                    
                    inputs_venta.value = 0 #retorno el valor de la compra a cero
                    semaforo.value += 2 #Le da la señal el arbitrador para seguir
                    
                    lock.release()
#################### '''E N D  of  C R I T I C A L  Z O N E'''
               
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR EN EL SCRIPT DE FLUJO DE VENTA --- ')
                inputs_venta.value = 0
                tr_venta.value = 0
                semaforo.value = 0
                traceback.print_exc()
                continue    
                            
        else:
            BREAK = True
            print('\nSe detiene el ejecutador de ventas')
            break
    
    return

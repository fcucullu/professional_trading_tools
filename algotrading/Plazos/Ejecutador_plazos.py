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

def flujo_compra_plazos(inputs_compra, tr_compra, lock, semaforo, token):
    
    print('\nComienza el ejecutador de compras')
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < 16:
    
            try:
                
                if inputs_compra.value != 0:
                    print('COMPRA ENVIADA a las: {}'.format(FF.DetectaHorarioSegundos()))
                    
                    tr_compra.value = sandbox.comprar(inputs_compra.value[0], inputs_compra.value[1], inputs_compra.value[2], 'T0', inputs_compra.value[3], token)
                    
                    while tr_compra.value == 0: #Espero hasta que la orden este generada
                            time.sleep(0.0001)
                    
                    horario = FF.DetectaHorarioSegundos()
                    print('COMPRA INICIADA a las {}'.format(horario))
                            
                    while sandbox.tr_check(tr_compra.value, token)[0] == 'iniciada': #espero hasta que la tr este en proceso (llego al mercado)
                        time.sleep(0.0001) 
                    print('COMPRA EN PROCESO a las: {}'.format(FF.DetectaHorarioSegundos()))
                    time.sleep(5)
                    try:
                        tr_compra.value = sandbox.tr_delete(tr_compra.value, token) #Simulo una fill or kill
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
            print('\nSe detiene la actualización de tasa para operatoria')
            break
        
    return

def flujo_venta_plazos(inputs_venta, tr_venta, lock, semaforo, token):
    
    print('\nComienza el ejecutador de ventas')
    
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < 16:
            
            try:
                
                if inputs_venta.value != 0:
                    print('VENTA ENVIADA a las: {}'.format(FF.DetectaHorarioSegundos()))
                
                    tr_venta.value = sandbox.vender(inputs_venta.value[0], inputs_venta.value[1], inputs_venta.value[2], 'T2', inputs_venta.value[3], token)
                    
    
                    while tr_venta.value == 0: #Espero hasta que la orden este generada
                        time.sleep(0.0001)
    
                    horario = FF.DetectaHorarioSegundos()
                    print('VENTA INICIADA a las {}'.format(horario))
            
                    while sandbox.tr_check(tr_venta.value, token)[0] == 'iniciada': #espero hasta que la tr este en proceso (llego al mercado)
                        time.sleep(0.0001) 
                    print('VENTA EN PROCESO a las: {}'.format(FF.DetectaHorarioSegundos()))
                    time.sleep(5)
                    try:
                        tr_venta.value = sandbox.tr_delete(tr_venta.value, token)
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
            print('\nSe detiene la actualización de tasa para operatoria')
            break
    
    return




#
#def ejecutar(tr_compra,tr_venta,p_ejecucion, simbolo, cantidad, precioC, precioV):
#    #if __name__ == "__main__":    
#        
#         
#    p_ejecucion.starmap_async(flujo_compra_plazos, [(simbolo, cantidad, precioC, hoy, tr_compra)])
#    p_ejecucion.starmap_async(flujo_venta_plazos, [(simbolo, cantidad, precioV, hoy, tr_venta)])
#
#    while type(tr_compra.value) == int or type(tr_venta.value) == int: #Si todo marcha bien son tuples, si marcha mal son dics. Solo son int cuando hay algo pendiente.
#        time.sleep(0.001)
#       
#    compra = tr_compra.value
#    venta = tr_venta.value
#    
#    tr_compra.value = 0 #dejo los valores limpios para la proxima ejecucion
#    tr_venta.value = 0
##    p_ejecucion.terminate() #Liquido pool de procesos
##    p_ejecucion.join() #Joineo memoria del pool al main
#   
#    return compra, venta


#############################################################################
'''                                  PRUEBA                              '''
#############################################################################

#
#if __name__ == "__main__": 
#    a = time.time()
#    m = multiprocessing.Manager() #Declaro el Manager de multiprocessing
#    b = time.time()
#    print('Tiempo en generar manager = '+str(b-a))
#    tr_compra = m.Value('d', 0)
#    tr_venta = m.Value('d', 0)
#    c = time.time()
#    print('Tiempo en generar VALUES = '+str(c-b))
#    p = multiprocessing.Pool(processes=10) #Declaro pool de workers
#    d = time.time()
#    print('Tiempo en generar manager = '+str(b-a))
#    
#print('asdasdasd')




#if __name__ == "__main__": 
#    asd = ejecutar(m,tr_compra,tr_venta,p, 'COME',10,1,2)
#    asd


        

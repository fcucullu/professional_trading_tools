''' By Francisco Cucullu '''

import sys
path = r'Y:\Git\algotrading\API'
sys.path.append(path)
from funcionesAPI import Sandbox
sandbox = Sandbox()
import time
import datetime
import traceback

def actualizar_token(hora_stop, token, lock):
    
    print('\nComienza el actualizador del token')
    
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < hora_stop:
        
            try:
                sandbox.get_token()
                tok = sandbox.token.access
                lock.acquire()
                token.value = tok
                lock.release()
                print('\nSe actualizo el token con exito.')
                time.sleep(600)
        
            except Exception:
                print('\n --- HUBO UN ERROR EN EL ACTULIZADOR DE TOKEN --- ')
                traceback.print_exc()
                time.sleep(600)
                continue 
            
            
        else:
            BREAK = True
            print('\nSe detiene el actualizador de token.')    
            break
    
    return



def actualizar_token_once(token, lock):
    
    try:
        sandbox.get_token()
        tok = sandbox.token.access
        lock.acquire()
        token.value = tok
        lock.release()

    except Exception:
        print('\n --- HUBO UN ERROR EN EL ACTULIZADOR DE TOKEN --- ')
        traceback.print_exc()
    
    return
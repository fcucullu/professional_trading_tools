# By Francisco Cucullu

def logs(txt_input, q, lock, hora_stop):
    import datetime #Para detener el algoritmo a las "hora_stop" horas
    import time
    import traceback
    
    print('\nComienza a almacenarse los LOGS')
    
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < hora_stop:
            time.sleep(60) 
            #print(q.empty())
            try:
                if q.empty() is False:
                    print('\nSe guardan LOGS')
                    #  CRITICAL  #
                    lock.acquire()
                    txt = open(txt_input, "a" ) #open file in append mode
                    while q.empty() is False:    
                        line = q.get()
                        txt.write(line + '\n')
                    txt.close()
                    lock.release()
                    #  CRITICAL  #
                    now = datetime.datetime.now()
                else:
                    print('\nNo hay LOGS que guardar')
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR CON LOS LOGS --- ')
                traceback.print_exc()
                continue 
        else:
            BREAK = True
            print('\nSe detienen los LOGS')    
            break
        
    #DA LA UTLIMA VUELTA DOS MINUTOS DESPUES
    time.sleep(90)
    try:
        if q.empty() is False:
            print('\nSe guardan LOGS - ULTIMA VUELTA')
            #  CRITICAL  #
            lock.acquire()
            txt = open(txt_input, "a" ) #open file in append mode
            while q.empty() is False:    
                line = q.get()
                txt.write(line + '\n')
            txt.close()
            lock.release()
            #  CRITICAL  #
            now = datetime.datetime.now()
        else:
            print('\nNo hay LOGS que guardar - ULTIMA VUELTA')
    except Exception:
        now = datetime.datetime.now()
        print('\n --- HUBO UN ERROR CON LOS LOGS --- ')
        traceback.print_exc()
        pass
        
    return

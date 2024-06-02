# By Francisco Cucullu

def worker(csv_input, q, lock):
    import datetime #Para detener el algoritmo a las 16hrs (por CI)
    import time
    import pandas as pd
    import traceback
    
    print('\nComienza el Worker de Plazos')
    
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < 16:
            time.sleep(30) 
            try:
                #  CRITICAL  #
                lock.acquire()
                csv = pd.read_csv(csv_input, sep=';', decimal=',')
                if q.empty() is False:
                    print('\nWorker alimenta CSV de plazos')
                else:
                    print('\nWorker no trabaja por que la cola esta vacia')
                while q.empty() is False:    
                    i = q.get()
                    csv = csv.append(i, ignore_index=True)   
                csv.to_csv(csv_input, index=False, sep=';', decimal=',')  
                lock.release()
                #  CRITICAL  #
                now = datetime.datetime.now()
            except Exception:
                now = datetime.datetime.now()
                print('\n --- HUBO UN ERROR EN EL WORKER --- ')
                traceback.print_exc()
                continue 
        else:
            BREAK = True
            print('\nSe detiene el Worker de arbitraje de plazos.')    
            break
        
    #DA LA UTLIMA VUELTA DOS MINUTOS DESPUES
    time.sleep(90)
    try:
        #  CRITICAL  #
        lock.acquire()
        csv = pd.read_csv(csv_input, sep=';', decimal=',')
        if q.empty() is False:
            print('\nWorker alimenta CSV de plazos ULTIMA VUELTA')
        else:
            print('\nWorker no trabaja por que la cola esta vacia ULTIMA VUELTA')
        while q.empty() is False:    
            i = q.get()
            csv = csv.append(i, ignore_index=True)   
        csv.to_csv(csv_input, index=False, sep=';', decimal=',')  
        lock.release()
        #  CRITICAL  #
        now = datetime.datetime.now()
    except:
        now = datetime.datetime.now()
        print('\nHubo algun problema con el Worker ULTIMA VUELTA')
        pass
        
    return
# By Francisco Cucullu

def worker(csv_input, contador, q, lock, hora_stop):
    import datetime #Para detener el algoritmo a las "hora_stop" horas
    import time
    import pandas as pd
    import traceback
    
    print('\nComienza el Worker')
    
    csv = pd.read_csv(csv_input, sep=';', decimal=',')
    lock.acquire()
    try:
        contador.value = csv['# Trade'].max() +1
    except:
        contador.value = 1
    lock.release()
    
    now = datetime.datetime.now()
    BREAK = False
    while BREAK == False:
        if now.hour < hora_stop:
            time.sleep(60) 
            #print(q.empty())
            try:
                #  CRITICAL  #
                lock.acquire()
                csv = pd.read_csv(csv_input, sep=';', decimal=',')
                columns = csv.columns.to_list()
                if q.empty() is False:
                    print('\nWorker alimenta CSV')
                else:
                    print('\nWorker no trabaja por que la cola esta vacia')
                while q.empty() is False:    
                    i = q.get()
                    csv = csv.append(i, ignore_index=True, sort=False) 
                csv = csv[columns]
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
            print('\nSe detiene el Worker')    
            break
        
    #DA LA UTLIMA VUELTA DOS MINUTOS DESPUES
    time.sleep(90)
    try:
        #  CRITICAL  #
        lock.acquire()
        csv = pd.read_csv(csv_input, sep=';', decimal=',')
        if q.empty() is False:
            print('\nWorker alimenta CSV ULTIMA VUELTA')
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

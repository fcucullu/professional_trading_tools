import sys 
path = 'Y:\Git\algotrading\API'
sys.path.append(path)
from __requests__ import Requests
requests = Requests()
import time



# #PRUEBA COTIZACION EN DISTINTOS PLAZOS
start_time = time.time()
a = requests.ultimoPrecio('GGAL', 'BCBA', 'T2')
c = requests.ultimoPrecio('GGAL', 'BCBA', 'T0')
print(a)
print(c)
end_time = time.time()
print("\nTiempo de ejecucion fue de", end_time - start_time, "segundos")
 
#PRUEBA TOMAR PUNTAS
start_time = time.time()
a = requests.puntas('A2E2D', 'BCBA', 'T2')
c = requests.puntas('A2E2D', 'BCBA', 'T0')
print(a)
print(c)
end_time = time.time()
print("\nTiempo de ejecucion fue de", end_time - start_time, "segundos")



#PRUEBA SERIE HISTORICA
start_time = time.time()
a = requests.serie_diaria('GGAL','2018-11-13','2018-12-13')
a
b = requests.serie_intradiaria('GGAL','2018-11-04','2018-12-05')
b
end_time = time.time()
print("\nTiempo de ejecucion fue de", end_time - start_time, "segundos")


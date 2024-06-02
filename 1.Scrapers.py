#By Francisco Cucullu

import schedule
import time
import sys
sys.path.append(r'Y:\Git\Scrapers')
sys.path.append(r'Y:\Git\Funciones')
sys.path.append(r'Y:\Git\Webdrivers')
import scrap_tasa as tasa
import scrap_dolarMEP as dolarMEP
import scrap_dolarMAE as dolarMAE
import scrap_riesgopais as riesgopais
import scrap_dolarIOL as dolarIOL
import Reporte35 as dolarSUPV
import FuncionesFrancisco as FF #Funciones varias
import scrap_competencia_wraper as dolarCOMP

##############################################################################
'''                 Funciones que hará el scheduler                       '''
##############################################################################

def csv():
    try:
        tasa.crea_csv()
        print('CSV de tasa creado.')
    except:
        print('Hubo un problema con el CSV de TASA.')
        
    try:
        dolarMEP.crea_csv_dolarMEP()
        print('CSV de DOLAR MEP creado.')   
    except:
        print('Hubo un problema con el CSV de DOLAR MEP.')
    
    try:
        dolarMAE.crea_csv_dolarMAE()
        print('CSV de DOLAR MAE creado.')  
    except:
        print('Hubo un problema con el CSV de DOLAR MAE.')
        
    try:
        riesgopais.crea_csv_riesgopais()
        print('CSV de RIESGO PAIS creado.')    
    except:
        print('Hubo un problema con el CSV de RIESGO PAIS.')
        
    try:
        dolarIOL.crea_csv_dolarIOL()
        print('CSV de DOLAR IOL creado.')    
    except:
        print('Hubo un problema con el CSV de DOLAR IOL.')
        
    try:
        dolarSUPV.crea_csv_dolarSUPV()
        print('CSV de DOLAR SUPV creado.')    
    except:
        print('Hubo un problema con el CSV de DOLAR SUPV.')
    
    try:
        dolarCOMP.crea_csv()
        print('CSV de DOLAR COMPETENCIA creado.')    
    except:
        print('Hubo un problema con el CSV de DOLAR COMPETENCIA.')
        
        
def mep_5min():
    dolarMEP.escribe_dolarMEP()
    
def tasa_5min():
    tasa.escribe_tasa()
    
def mae_5min():
    dolarMAE.escribe_dolarMAE()
    
def riesgopais_5min():
    riesgopais.escribe_riesgopais()
    
def iol_5min():
    dolarIOL.escribe_dolarIOL()
    
def supv_5min():
    dolarSUPV.escribe_dolarSUPV()
    
def comp_5min():
    dolarCOMP.escribe_dolar()
    
def separador():
    hora = FF.DetectaHorario()
    print('\n----------------------------')
    print('               {}             '.format(hora))
    
    
##############################################################################
'''                 Defino horarios para dispara scripts                   '''
##############################################################################

# CREAR ARCHIVOS PARA TODOS
schedule.every().day.at("11:05").do(csv).tag('files')


#HORARIO DE 1030 a 17
horario1 = []  #Defino horarios para el script que alimentará el archivo
for i in range(30, 60, 5):
    if i == 0 or i == 5:  #Si es minuto de una sola cifra, detectar
        horario1.append(str(10)+':0'+str(i)) #imprime hora y minuto transformado en dos cifras
    else:
        horario1.append(str(10)+':'+str(i)) #imprime hora y minuto
for h in range(11, 17, 1): #Loop para ir hora por hora
    for m in range(00, 60, 5): #Loop para ir minuto por minuto
        if m == 0 or m == 5:  #Si es minuto de una sola cifra, detectar
            horario1.append(str(h)+':0'+str(m)) #imprime hora y minuto transformado en dos cifras
        else:
            horario1.append(str(h)+':'+str(m)) #imprime hora y minuto
horario1.append('17:00') #imprime hora de cierre


#HORARIO DE 11 a 16
horario2 = []  #Defino horarios para el script que alimentará el archivo
for h in range(11, 16, 1): #Loop para ir hora por hora
    for m in range(00, 60, 5): #Loop para ir minuto por minuto
        if m == 0 or m == 5:  #Si es minuto de una sola cifra, detectar
            horario2.append(str(h)+':0'+str(m)) #imprime hora y minuto transformado en dos cifras
        else:
            horario2.append(str(h)+':'+str(m)) #imprime hora y minuto
horario2.append('16:00') #imprime hora de cierre


#HORARIO DE 1030 a 15
horario3 = []  #Defino horarios para el script que alimentará el archivo
for i in range(30, 60, 5):
    if i == 0 or i == 5:  #Si es minuto de una sola cifra, detectar
        horario3.append(str(10)+':0'+str(i)) #imprime hora y minuto transformado en dos cifras
    else:
        horario3.append(str(10)+':'+str(i)) #imprime hora y minuto
for h in range(11, 15, 1): #Loop para ir hora por hora
    for m in range(00, 60, 5): #Loop para ir minuto por minuto
        if m == 0 or m == 5:  #Si es minuto de una sola cifra, detectar
            horario3.append(str(h)+':0'+str(m)) #imprime hora y minuto transformado en dos cifras
        else:
            horario3.append(str(h)+':'+str(m)) #imprime hora y minuto
horario3.append('15:00') #imprime hora de cierre


#HORARIO DE 11 a 17
horario4 = []  #Defino horarios para el script que alimentará el archivo
for h in range(11, 17, 1): #Loop para ir hora por hora
    for m in range(00, 60, 5): #Loop para ir minuto por minuto
        if m == 0 or m == 5:  #Si es minuto de una sola cifra, detectar
            horario4.append(str(h)+':0'+str(m)) #imprime hora y minuto transformado en dos cifras
        else:
            horario4.append(str(h)+':'+str(m)) #imprime hora y minuto
horario4.append('17:00') #imprime hora de cierre



# SEPARADOR
for i in horario1:
    schedule.every().day.at(i).do(separador).tag('scraper')  #Aqui definí intervalos de 5 minutos para el script


# ALIMENTAR ARCHIVO DE DOLAR MEP
for i in horario2:
    schedule.every().day.at(i).do(mep_5min).tag('scraper')  #Aqui definí intervalos de 5 minutos para el script

# ALIMENTAR ARCHIVO DE DOLAR SUPV
for i in horario2:
    schedule.every().day.at(i).do(supv_5min).tag('scraper')  #Aqui definí intervalos de 5 minutos para el script

# ALIMENTAR ARCHIVO DE DOLAR IOL
for i in horario2:
    schedule.every().day.at(i).do(iol_5min).tag('scraper')  #Aqui definí intervalos de 5 minutos para el script

# ALIMENTAR ARCHIVO DE DOLAR MAE
for i in horario3:
    schedule.every().day.at(i).do(mae_5min).tag('scraper')  #Aqui definí intervalos de 5 minutos para el script

# ALIMENTAR ARCHIVO DE RIESGO PAIS
for i in horario1:
    schedule.every().day.at(i).do(riesgopais_5min).tag('scraper')  #Aqui definí intervalos de 5 minutos para el script

# ALIMENTAR ARCHIVO DE TASA
for i in horario2:
    schedule.every().day.at(i).do(tasa_5min).tag('scraper')  #Aqui definí intervalos de 5 minutos para el script

# ALIMENTAR ARCHIVO DE TASA
for i in horario4:
    schedule.every().day.at(i).do(comp_5min).tag('scraper')  #Aqui definí intervalos de 5 minutos para el script



##############################################################################
'''                       Incicio el scheduler                           '''
##############################################################################

horario = FF.DetectaHorario()
while horario != '16:01': #Que corra mientras el horario sea diferente a 16:01 y despues que cierre!
    schedule.run_pending()
    time.sleep(1)
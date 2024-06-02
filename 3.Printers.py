#By Francisco Cucullu

import schedule
import time
import sys
sys.path.append(r'Y:\Git\Funciones')
sys.path.append(r'Y:\Git\Scrapers')
sys.path.append(r'Y:\Git\Webdrivers')
sys.path.append(r'Y:\Git\algotrading\API')
import scrap_tasa as tasa
import Reporte35 as dolarSUPV
import scrap_dolarMEP as dolarMEP
import scrap_dolarMAE as dolarMAE
import scrap_riesgopais as riesgopais
import FuncionesFrancisco as FF #Funciones varias
import pandas as pd
from tabulate import tabulate
import csv
from funcionesAPI import Sandbox
sandbox = Sandbox()


##############################################################################
'''                 Funciones que hará el scheduler                       '''
##############################################################################

def print_5seg():
    
    hora = FF.DetectaHorarioSegundos()
    #Ptasa, Vtasa = tasa.print_tasa()
    PmepC, PmepV, ProfC, ProfV = dolarMEP.print_dolarME2P()
    PsupvC, PsupvV, VsupvC, VsupvV = dolarSUPV.print_dolarSUPV()
    Pmae, Vmae = dolarMAE.print_dolarMAE()
    Prp, Vrp = riesgopais.print_riesgopais()
    portafolio = len(sandbox.portafolio_arg()['activos'])
    saldo = sandbox.saldo_arg_dolares_inmediato_notok()
    
    
    try:
        Gcia_Compra = "%0.2f" % (PmepC-PsupvV,)
    except:
        Gcia_Compra = 'N/D'
       
    try:
        Gcia_Venta = "%0.2f" % (PsupvC-PmepV,)
    except:
        Gcia_Venta = 'N/D'
       
        
    tick = pd.DataFrame({hora: ['Nivel', 'Prof/Var'],
                                 'MEP': [str(PmepC)+' | '+str(PmepV), str(ProfC)+' | '+str(ProfV)],
                                 'SUPV': [str(PsupvC)+' | '+str(PsupvV), str(Gcia_Venta)+' | '+str(Gcia_Compra)],
                                 'MAE': [Pmae, Vmae],
                                 'R.Pais': [Prp, Vrp],
                                 'Port': [portafolio, saldo]})
    print('--------------------------------------------------------------------------')
    print(tabulate(tick[[hora,'MEP','SUPV','MAE','R.Pais','Port']],
                       headers='keys', tablefmt='fancy_grid', showindex=False, stralign="center", numalign="center"))
   
    
    try:
        if (float(Gcia_Venta) > 0):
            almacenar(PmepC, PmepV, PsupvC, PsupvV, ProfC, ProfV, Gcia_Venta, Gcia_Compra)
    except:
        pass
    try:
        if (float(Gcia_Compra) > 0):
            almacenar(PmepC, PmepV, PsupvC, PsupvV, ProfC, ProfV, Gcia_Venta, Gcia_Compra)
    except:
        pass

def crea_csv():

    #Detecto dia
    (DIA, MES, ANO) = FF.DetectaDia()
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_arbitraje.csv"
    
    #Creo el cvs incialcon el nombre de las filas correspondiente a los datos que scrapeo
    with open(path, 'w', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        filewriter.writerow(['Horario','Mep_C','Mep_V','Supv_C','Supv_V','Prof_C','Prof_V','Dif_C','Dif_V'])
 
    csvfile.close()
    print(' ----------------------- ARCHIVO CSV CREADO -----------------------------')
    
def almacenar(PmepC, PmepV, PsupvC, PsupvV, ProfC, ProfV, Gcia_Venta, Gcia_Compra):
    
    #Detecto dia
    (DIA, MES, ANO) = FF.DetectaDia()
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_arbitraje.csv"

    
    csv_input = pd.read_csv(path, sep=';', decimal=',')
    csv_input = csv_input.append({'Horario': FF.DetectaHorario(),
                                  'Mep_C': PmepC,
                                  'Mep_V': PmepV,
                                  'Supv_C': PsupvC,
                                  'Supv_V': PsupvV,
                                  'Prof_C': ProfC,
                                  'Prof_V': ProfV,
                                  'Dif_C': Gcia_Venta,
                                  'Dif_V': Gcia_Compra}, ignore_index=True)
    csv_input.to_csv(path, index=False, sep=';', decimal=',')
    
    try:
        if float(Gcia_Venta) > 0:
            print('¡¡ ARBITRAR !! -> VENDER DOLAR AL SUPV')
    except:
        pass
    try:
        if float(Gcia_Compra) > 0:
            print('¡¡ ARBITRAR !! -> COMPRAR DOLAR AL SUPV')
    except:
       pass
    
##############################################################################
'''                 Defino horarios para dispara scripts                   '''
##############################################################################

schedule.every().day.at("10:50").do(crea_csv).tag('files')

schedule.every(5).seconds.do(print_5seg)  #Aqui definí intervalos de 15 segs para el script

##############################################################################
'''                       Incicio el scheduler                           '''
##############################################################################

horario = FF.DetectaHorario()
#while horario != '11:00':
#    time.sleep(1)
    
while horario != '16:01': #Que corra mientras el horario sea diferente a 16:01 y despues que cierre!
    schedule.run_pending()
    time.sleep(1)
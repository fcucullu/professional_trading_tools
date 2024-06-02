# By Francisco Cucullu

tickers = ['AY24', 'AO20', 'DICA']

import sys
sys.path.append(r'Y:\Git\Funciones')
sys.path.append(r'Y:\Git\algotrading\API')
import FuncionesFrancisco as FF
import csv
import pandas as pd
from funcionesAPI import Requests #APIS 
requests = Requests()
import traceback

##############################################################################
'''                 Funcion para crear archivo CSV                       '''
##############################################################################

def crea_csv_dolarMEP():

    #Detecto dia
    (DIA, MES, ANO) = FF.DetectaDia()
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_MEP.csv"
    
    #Creo el cvs incialcon el nombre de las filas correspondiente a los datos que scrapeo
    with open(path, 'w', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        filewriter.writerow(['Horario','BonoC','Compra','Venta','BonoV'])
 
    csvfile.close()
    
##############################################################################
'''                 Funcion para alimentar archivo CSV                    '''
##############################################################################

def escribe_dolarMEP():
    import sys #Se vuelve a inportar para no confundir con el modulo requests
    sys.path.append(r'Y:\Git\Funciones') #Se vuelve a inportar para no confundir con el modulo requests
    sys.path.append(r'Y:\Git\algotrading\API') #Se vuelve a inportar para no confundir con el modulo requests
    from funcionesAPI import Requests #Se vuelve a inportar para no confundir con el modulo requests
    requests = Requests() #Se vuelve a inportar para no confundir con el modulo requests
    
    #Detecto dia y horario
    (DIA, MES, ANO) = FF.DetectaDia()
    horario = FF.DetectaHorario()
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_MEP.csv"
    
    DM_AlVender = (1 - 0.0001) / (1 + 0.0001)
    DM_AlComprar = (1 + 0.0001) / (1 - 0.0001)
    
    TC_V = pd.DataFrame(columns={'Bono','Venta'})
    TC_C = pd.DataFrame(columns={'Bono','Compra'})
        
    for i in tickers:
        try:
            QC_CI,C_CI,V_CI,QV_CI = requests.puntas(i,'BCBA','T0').values()
        except:
            QC_CI,C_CI,V_CI,QV_CI = 0
        try:
            QC_CID,C_CID,V_CID,QV_CID = requests.puntas(i+"D",'BCBA','T0').values()
        except:
            QC_CID,C_CID,V_CID,QV_CID = 0
            
        if V_CI == 0 or C_CID == 0:
            pass
        else:
            TC_V = TC_V.append({'Bono': i, 'Venta': V_CI/C_CID}, ignore_index=True)
            
        if C_CI == 0 or V_CID == 0:
            pass
        else:
            TC_C = TC_C.append({'Bono': i, 'Compra': C_CI/V_CID}, ignore_index=True)
    
    TC = TC_C.merge(TC_V, on='Bono', suffixes=('_Compra', '_Venta')) #Mergeo las tablas
    TC = TC[['Bono','Compra','Venta']]  #Reordeno las columnas
    #print(TC)
    #print('')
    if len(TC) == 0:
        print('DOLAR MEP sin datos')
        pass
    else:
        
        try:
            csv_input = pd.read_csv(path, sep=';', decimal=',')
        
            indexV = TC['Venta'].idxmin()
            bonoV = TC.iloc[indexV,0]
            precioV = round(float(TC.iloc[indexV,2] * DM_AlComprar),4)
            indexC = TC['Compra'].idxmax()
            bonoC = TC.iloc[indexC,0]
            precioC = round(float(TC.iloc[indexC,1] * DM_AlVender),4)
    
            csv_input = csv_input.append({'Horario': horario,
                                          'BonoC': bonoC,
                                          'Compra': precioC,
                                          'Venta': precioV,
                                          'BonoV': bonoV}, ignore_index=True)
            csv_input.to_csv(path, index=False, sep=';', decimal=',')
            print('DOLAR MEP: {}-{}'.format(precioC, precioV))
        except:
            print('Problema en actualizar DOLAR MEP las {}'.format(horario))
            traceback.print_exc()
            pass
    
    
##############################################################################
'''                           Funcion para printear                        '''
##############################################################################

def print_dolarMEP():
    
    lastC, lastV = check_last()
    
    DM_AlVender = (1 - 0.0001) / (1 + 0.0001)
    DM_AlComprar = (1 + 0.0001) / (1 - 0.0001)
    
    TC_V = pd.DataFrame(columns={'Bono','Venta', 'ProfV'})
    TC_C = pd.DataFrame(columns={'Bono','Compra', 'ProfC'})
        
    for i in tickers:
        try:
            QC_CI,C_CI,V_CI,QV_CI = requests.puntas(i,'BCBA','T0').values()
        except:
            QC_CI,C_CI,V_CI,QV_CI = 0
        try:
            QC_CID,C_CID,V_CID,QV_CID = requests.puntas(i+"D",'BCBA','T0').values()
        except:
            QC_CID,C_CID,V_CID,QV_CID = 0
            
        
        if V_CI == 0 or C_CID == 0:
            pass
        else:
            TC_V = TC_V.append({'Bono': i, 'Venta': V_CI/C_CID, 'ProfV': min(QV_CI,QC_CID)}, ignore_index=True)
            
        if C_CI == 0 or V_CID == 0:
            pass
        else:
            TC_C = TC_C.append({'Bono': i, 'Compra': C_CI/V_CID, 'ProfC': min(QC_CI,QV_CID)}, ignore_index=True)
    
    TC = TC_C.merge(TC_V, on='Bono', suffixes=('_Compra', '_Venta')) #Mergeo las tablas
    TC = TC[['Bono','Compra','Venta','ProfC','ProfV']]  #Reordeno las columnas
    #print(TC)
     
    try:

        indexV = TC['Venta'].idxmin()
        #bonoV = TC.iloc[indexV,0]
        precioV = round(float(TC.iloc[indexV,2] * DM_AlComprar),2)
        profV = str(int(precioV * TC.iloc[indexV,4]/1000))+' K' if precioV * TC.iloc[indexV,4] < 1000000 else str(int(precioV * TC.iloc[indexV,4]/1000000))+' M'
        
        indexC = TC['Compra'].idxmax()
        #bonoC = TC.iloc[indexC,0]
        precioC = round(float(TC.iloc[indexC,1] * DM_AlVender),2)
        profC = str(int(precioC * TC.iloc[indexV,3]/1000))+' K' if precioC * TC.iloc[indexV,3] < 1000000 else str(int(precioC * TC.iloc[indexV,3]/1000000))+' M'       
            
    except:
        precioC = 'N/D'
        precioV = 'N/D'
        profC = 'N/D'
        profV = 'N/D'
                    
    return precioC, precioV, profC, profV


##############################################################################
'''                           Funciones varias                          '''
##############################################################################

def check_last():
    #Veo cual fue el cierre de ayer para el % de variacion diaria
    for i in range(1,15):
        try:
            archivo = FF.DeltaDateHoy(i)[1].replace('-','')+'_MEP.csv'
            path = "Y:\\Git\\Data\\Dolar\\" + archivo
            csv_input = pd.read_csv(path, sep=';', decimal=',')
            lastC = csv_input.iloc[-1,2]
            lastV = csv_input.iloc[-1,3]
            break
        except FileNotFoundError:
            continue
        
    return lastC, lastV

##############################################################################
    

def print_dolarME2P():
    
    lastC, lastV = check_last()
    
    DM_AlVender = (1 - 0.0001) / (1 + 0.0001)
    DM_AlComprar = (1 + 0.0001) / (1 - 0.0001)
    
    TC_V = pd.DataFrame(columns={'Bono','Venta', 'ProfV'})
    TC_C = pd.DataFrame(columns={'Bono','Compra', 'ProfC'})
        
    for i in tickers:
        try:
            QC_CI,C_CI,V_CI,QV_CI = requests.puntas(i,'BCBA','T0').values()
        except:
            QC_CI,C_CI,V_CI,QV_CI = 0,0,0,0
        try:
            QC_CID,C_CID,V_CID,QV_CID = requests.puntas(i+"D",'BCBA','T0').values()
        except:
            QC_CID,C_CID,V_CID,QV_CID = 0,0,0,0
            
        
        if V_CI == 0 or C_CID == 0:
            pass
        else:
            TC_V = TC_V.append({'Bono': i, 'Venta': V_CI/C_CID, 'ProfV': min(QV_CI,QC_CID)*C_CID/100}, ignore_index=True)
            
        if C_CI == 0 or V_CID == 0:
            pass
        else:
            TC_C = TC_C.append({'Bono': i, 'Compra': C_CI/V_CID, 'ProfC': min(QC_CI,QV_CID)*V_CID/100}, ignore_index=True)
    
    TC = TC_C.merge(TC_V, on='Bono', suffixes=('_Compra', '_Venta')) #Mergeo las tablas
    TC = TC[['Bono','Compra','Venta','ProfC','ProfV']]  #Reordeno las columnas
    #print(TC)
     
    try:

        indexV = TC['Venta'].idxmin()
        #bonoV = TC.iloc[indexV,0]
        precioV = round(float(TC.iloc[indexV,2] * DM_AlComprar),4)
        profV = 'U$ '+str(int(TC.iloc[indexV,4]//100*100))
        
        indexC = TC['Compra'].idxmax()
        #bonoC = TC.iloc[indexC,0]
        precioC = round(float(TC.iloc[indexC,1] * DM_AlVender),4)
        profC = 'U$ '+str(int(TC.iloc[indexV,3] //100*100))
            
    except:
        precioC = 'N/D'
        precioV = 'N/D'
        profC = 'N/D'
        profV = 'N/D'
                    
    return precioC, precioV, profC, profV



# By Francisco Cucullu
'''Se crea este archivo para programar un script que cree un CSV y
que guarde la información de los otros scrapers teniendo en cuenta las
excepciones que fueran necesarias '''

import sys
sys.path.append(r'Y:\Git\Funciones')
sys.path.append(r'Y:\Git\Scrapers')
sys.path.append(r'Y:\Git\Webdrivers')
import FuncionesFrancisco as FF
import csv
import scrap_competencia as comp
import scrap_dolarMAE as MAE
import scrap_dolarMEP as dolarMEP
import Reporte35 as dolarSUPV
import pandas as pd

##############################################################################
'''                 Funcion para crear archivo CSV                       '''
##############################################################################

def crea_csv():
    
    #Detecto dia
    (DIA, MES, ANO) = FF.DetectaDia()
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_competencia.csv"
    
    #Creo el cvs incialcon el nombre de las filas correspondiente a los datos que scrapeo
    with open(path, 'w', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';')
        filewriter.writerow(['Horario'])
        filewriter.writerow(['MAE_compra'])
        filewriter.writerow(['MAE_venta'])
        filewriter.writerow(['MAE_spread'])
        filewriter.writerow(['MEP_compra'])
        filewriter.writerow(['MEP_venta'])
        filewriter.writerow(['MEP_spread'])
        filewriter.writerow(['MESA_compra'])
        filewriter.writerow(['MESA_venta'])
        filewriter.writerow(['MESA_spread'])
        filewriter.writerow(['Balanz_compra'])
        filewriter.writerow(['Balanz_venta'])
        filewriter.writerow(['Balanz_spread'])
        filewriter.writerow(['BBVA_compra'])
        filewriter.writerow(['BBVA_venta'])
        filewriter.writerow(['BBVA_spread'])
        filewriter.writerow(['BNA_compra'])
        filewriter.writerow(['BNA_venta'])
        filewriter.writerow(['BNA_spread'])
        filewriter.writerow(['BullMarket_compra'])
        filewriter.writerow(['BullMarket_venta'])
        filewriter.writerow(['BullMarket_spread'])
        filewriter.writerow(['ciudad_compra'])
        filewriter.writerow(['Ciudad_venta'])
        filewriter.writerow(['Ciudad_spread'])
        filewriter.writerow(['GGAL_compra'])
        filewriter.writerow(['GGAL_venta'])
        filewriter.writerow(['GGAL_spread'])
        filewriter.writerow(['ICBC_compra'])
        filewriter.writerow(['ICBC_venta'])
        filewriter.writerow(['ICBC_spread'])
        #filewriter.writerow(['IEB_compra'])
        #filewriter.writerow(['IEB_venta'])
        #filewriter.writerow(['IEB_spread'])
        filewriter.writerow(['IOL_compra'])
        filewriter.writerow(['IOL_venta'])
        filewriter.writerow(['IOL_spread'])
        filewriter.writerow(['PPI_compra'])
        filewriter.writerow(['PPI_venta'])
        filewriter.writerow(['PPI_spread'])
        filewriter.writerow(['Santander_compra'])
        filewriter.writerow(['Santander_venta'])
        filewriter.writerow(['Santander_spread'])
        filewriter.writerow(['TiendaDolar_compra'])
        filewriter.writerow(['TiendaDolar_venta'])
        filewriter.writerow(['TiendaDolar_spread'])
        filewriter.writerow(['BuenDolar_compra'])
        filewriter.writerow(['BuenDolar_venta'])
        filewriter.writerow(['BuenDolar_spread'])
        filewriter.writerow(['Dolaria_compra'])
        filewriter.writerow(['Dolaria_venta'])
        filewriter.writerow(['Dolaria_spread'])
        filewriter.writerow(['NaranjaX_compra'])
        filewriter.writerow(['NaranjaX_venta'])
        filewriter.writerow(['NaranjaX_spread'])
        filewriter.writerow(['Brubank_compra'])
        filewriter.writerow(['Brubank_venta'])
        filewriter.writerow(['Brubank_spread'])
        
    csvfile.close()
    
    
def escribe_dolar():

    #Detecto dia y horario
    (DIA, MES, ANO) = FF.DetectaDia()
    horario = FF.DetectaHorario()
    #Ruta del CSV
    path = "Y:\\Git\\Data\\Dolar\\"+ANO+MES+DIA+"_competencia.csv"
    
    try:
        bull_compra, bull_venta = comp.bullmarket()
        bull_spread = bull_venta-bull_compra
        
        bna_compra, bna_venta = comp.bna()
        bna_spread = bna_venta-bna_compra
        
        ggal_compra, ggal_venta =  comp.ggal()
        ggal_spread = ggal_venta-ggal_compra
        
        tiendadolar_compra, tiendadolar_venta = comp.tiendadolar()
        tiendadolar_spread = tiendadolar_venta - tiendadolar_compra
        
        icbc_compra, icbc_venta = comp.icbc()
        icbc_spread = icbc_venta - icbc_compra
        
        bbva_compra, bbva_venta =  comp.bbva()
        bbva_spread = bbva_venta - bbva_compra
        
        ciudad_compra, ciudad_venta = comp.ciudad()
        ciudad_spread = ciudad_venta - ciudad_compra
        
        santander_compra, santander_venta = comp.santander()
        santander_spread = santander_venta - santander_compra
        
        #ieb_compra, ieb_venta = comp.ieb()
        #ieb_spread = ieb_venta - ieb_compra
        
        iol_compra, iol_venta = comp.iol()
        iol_spread = iol_venta - iol_compra
        
        ppi_compra, ppi_venta = comp.ppi()
        ppi_spread = ppi_venta - ppi_compra 
        
        balanz_compra, balanz_venta = comp.balanz()
        balanz_spread = balanz_venta - balanz_compra
        
        buendolar_compra, buendolar_venta = comp.buendolar()
        buendolar_spread = buendolar_venta - buendolar_compra
        
        dolaria_compra, dolaria_venta = comp.dolaria()
        dolaria_spread = dolaria_venta - dolaria_compra
        
        naranjax_compra, naranjax_venta = comp.naranjax()
        naranjax_spread = naranjax_venta - naranjax_compra
                
        brubank_compra, brubank_venta = comp.brubank()
        brubank_spread = brubank_venta - brubank_compra

        
        mep_compra, mep_venta, a, b  = dolarMEP.print_dolarME2P()
        if mep_compra == 'N/D':
            mep_compra = 0
        if mep_venta == 'N/D':
            mep_venta = 0
        mep_compra, mep_venta = round(mep_compra,2), round(mep_venta,2)
        mep_spread = mep_venta - mep_compra
        
        mesa_compra, mesa_venta, a, b = dolarSUPV.print_dolarSUPV()
        mesa_spread = mesa_venta - mesa_compra
        
        mae_compra, mae_venta, mae_last = MAE.reuters_mae()
        mae_spread = round(mae_venta,4) - round(mae_compra,4)

        
        #########################################################
        
        tick = pd.DataFrame({horario:
        [mae_compra,mae_venta,mae_spread,
        mep_compra,mep_venta,mep_spread,
        mesa_compra,mesa_venta,mesa_spread,
        balanz_compra,balanz_venta,balanz_spread,
        bbva_compra,bbva_venta,bbva_spread,
        bna_compra,bna_venta,bna_spread,
        bull_compra,bull_venta,bull_spread,
        ciudad_compra,ciudad_venta,ciudad_spread,
        ggal_compra,ggal_venta,ggal_spread,
        icbc_compra,icbc_venta,icbc_spread,
        #ieb_compra,ieb_venta,ieb_spread,
        iol_compra,iol_venta,iol_spread,
        ppi_compra,ppi_venta,ppi_spread,
        santander_compra,santander_venta,santander_spread,
        tiendadolar_compra,tiendadolar_venta,tiendadolar_spread,
        buendolar_compra, buendolar_venta, buendolar_spread,
        dolaria_compra, dolaria_venta, dolaria_spread,
        naranjax_compra, naranjax_venta, naranjax_spread,
        brubank_compra, brubank_venta, brubank_spread]})
        
        tick = tick.astype(float) #Para que todos los datos sean numeros

        
        
        
        #Levanto info del CSV y le agrego la info nueva
        csv_input = pd.read_csv(path, sep=';', decimal=',')
        csv_input = csv_input.join(tick)
        csv_input.to_csv(path, index=False, sep=';', decimal=',')
        print('Se guardo con exito el Dolar_Competencia')
        
    except:
        print('Hubo un problema en Dolar_Competencia')
        pass
    

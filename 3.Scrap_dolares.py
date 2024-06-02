# By Francisco Cucullu
import sys
sys.path.append(r'Y:\Git\Funciones')
sys.path.append(r'Y:\Git\Scrapers')
sys.path.append(r'Y:\Git\Webdrivers')
sys.path.append(r'Y:\Git\algotrading\API')
sys.path.append(r'Y:\Git\Python-website')
sys.path.append(r'Y:\Git\Python-website\templates')

import requests as rq
import FuncionesFrancisco as FF #Funciones varias
import pandas as pd
from tabulate import tabulate
import Reporte35 as dolarSUPV
import scrap_dolarMEP as dolarMEP
import scrap_competencia as comp
import scrap_dolarMAE as MAE
import datetime
import json
import time
import multiprocessing #modulo para disparar varios scripts al mismo tiempoo
import traceback
import index as web
from flask import Flask, render_template
from flask.logging import default_handler #Para evitar que se printeen IPs en la consola
from waitress import serve # Para correr el server en produccion sin que se trabe

#Me loggeo para obtener cookies
session = rq.Session()

def tabla(cotizaciones, cotizaciones2):
    ''' ###################### '''
    mae_compra, mae_venta, mae_last = MAE.reuters_mae()
    mae_spread = round(mae_venta,4) - round(mae_compra,4)
    body = {'precioCompra': mae_compra,
         'precioVenta': mae_venta,
         'precioUltimaCotizacion': mae_last}
    req = session.post('http://10.0.0.143:1234/CotizacionDolarMAE/Post', data=body)
    if req.status_code != 200:
        intentos = 0
        if intentos > 0 and intentos%10 == 0:
            print(req.json()['message'])
            intentos += 1
            time.sleep(1)
        
    ''' ###################### '''
    
    bull_compra, bull_venta = comp.bullmarket()
    bull_spread = bull_venta-bull_compra
    comprador_bull = mae_compra - bull_compra
    vendedor_bull = bull_venta - mae_venta
    
    bna_compra, bna_venta = comp.bna()
    bna_spread = bna_venta-bna_compra
    comprador_bna = mae_compra - bna_compra
    vendedor_bna = bna_venta - mae_venta
    
    ggal_compra, ggal_venta =  comp.ggal()
    ggal_spread = ggal_venta-ggal_compra
    comprador_ggal = mae_compra - ggal_compra
    vendedor_ggal = ggal_venta - mae_venta
    
    tiendadolar_compra, tiendadolar_venta = comp.tiendadolar()
    tiendadolar_spread = tiendadolar_venta - tiendadolar_compra
    comprador_tiendadolar = mae_compra - tiendadolar_compra
    vendedor_tiendadolar = tiendadolar_venta - mae_venta
    
    icbc_compra, icbc_venta = comp.icbc()
    icbc_spread = icbc_venta - icbc_compra
    comprador_icbc = mae_compra - icbc_compra
    vendedor_icbc = icbc_venta - mae_venta

    bbva_compra, bbva_venta =  comp.bbva()
    bbva_spread = bbva_venta - bbva_compra
    comprador_bbva = mae_compra - bbva_compra
    vendedor_bbva = bbva_venta - mae_venta

    ciudad_compra, ciudad_venta = comp.ciudad()
    ciudad_spread = ciudad_venta - ciudad_compra
    comprador_ciudad = mae_compra - ciudad_compra
    vendedor_ciudad = ciudad_venta - mae_venta
    
    santander_compra, santander_venta = comp.santander()
    santander_spread = santander_venta - santander_compra
    comprador_santander = mae_compra - santander_compra
    vendedor_santander = santander_venta - mae_venta
    
    #ieb_compra, ieb_venta = comp.ieb()
    #ieb_spread = ieb_venta - ieb_compra
    #comprador_ieb = mae_compra - ieb_compra
    #vendedor_ieb = ieb_venta - mae_venta
    
    iol_compra, iol_venta = comp.iol()
    iol_spread = iol_venta - iol_compra
    comprador_iol = mae_compra - iol_compra
    vendedor_iol = iol_venta - mae_venta
    
    ppi_compra, ppi_venta = comp.ppi()
    ppi_spread = ppi_venta - ppi_compra 
    comprador_ppi = mae_compra - ppi_compra
    vendedor_ppi = ppi_venta - mae_venta
    
    balanz_compra, balanz_venta = comp.balanz()
    balanz_spread = balanz_venta - balanz_compra
    comprador_balanz = mae_compra - balanz_compra
    vendedor_balanz = balanz_venta - mae_venta
    
    supv_compra, supv_venta = comp.supv()
    supv_spread = supv_venta - supv_compra
    comprador_supv = mae_compra - supv_compra
    vendedor_supv = supv_venta - mae_venta
    
    buendolar_compra, buendolar_venta = comp.buendolar()
    buendolar_spread = buendolar_venta - buendolar_compra
    comprador_buendolar = mae_compra - buendolar_compra
    vendedor_buendolar = buendolar_venta - mae_venta
    
    dolaria_compra, dolaria_venta = comp.dolaria()
    dolaria_spread = dolaria_venta - dolaria_compra
    comprador_dolaria = mae_compra - dolaria_compra
    vendedor_dolaria = dolaria_venta - mae_venta
    
    naranjax_compra, naranjax_venta = comp.naranjax()
    naranjax_spread = naranjax_venta - naranjax_compra
    comprador_naranjax = mae_compra - naranjax_compra
    vendedor_naranjax = naranjax_venta - mae_venta

    brubank_compra, brubank_venta = comp.brubank()
    brubank_spread = brubank_venta - brubank_compra
    comprador_brubank = mae_compra - brubank_compra
    vendedor_brubank = naranjax_venta - mae_venta

    
    mep_compra, mep_venta, a, b  = dolarMEP.print_dolarME2P()
    if mep_compra == 'N/D':
        mep_compra = 0
    if mep_venta == 'N/D':
        mep_venta = 0
    mep_compra, mep_venta = round(mep_compra,2), round(mep_venta,2)
    mep_spread = round(mep_venta - mep_compra, 2)
    comprador_mep = mae_compra - mep_compra
    vendedor_mep = mep_venta - mae_venta
    
    mesa_compra, mesa_venta, a, b = dolarSUPV.print_dolarSUPV()
    mesa_spread = mesa_venta - mesa_compra
    comprador_mesa = mae_compra - mesa_compra
    vendedor_mesa = mesa_venta - mae_venta
    
    
    hora = FF.DetectaHorarioSegundos()
    tabla_compra = pd.DataFrame({hora: [   'BullMarket','Bco_Nacion','Bco_Galicia','TiendaDolar',      'Bco_ICBC',   'Bco_BBVA',    'Bco_Ciudad',   'Bco_Santder',       '--> Dolariol.com <--',     'PPI',      'Balanz',    'Bco_Supervielle',    'BuenDolar(c/comision)',   'Dolaria',     'NaranjaX',      "BruBank",      'MEP',      'MESA',      'MAE'],
                                 'COMPRA': [bull_compra, bna_compra, ggal_compra, tiendadolar_compra,  icbc_compra,  bbva_compra,   ciudad_compra, santander_compra,         iol_compra,       ppi_compra,  balanz_compra,    supv_compra,     buendolar_compra,           dolaria_compra, naranjax_compra, brubank_compra,  mep_compra, mesa_compra, mae_compra]})
    tabla_compra = tabla_compra[tabla_compra['COMPRA'] != 0].sort_values('COMPRA',ascending=False).reset_index(drop=True)

    tabla_venta = pd.DataFrame({'Broker.': ['BullMarket','Bco_Nacion','Bco_Galicia','TiendaDolar',      'Bco_ICBC',   'Bco_BBVA',    'Bco_Ciudad',   'Bco_Santder',       '--> Dolariol.com <--',     'PPI',      'Balanz', 'Bco_Supervielle','BuenDolar(c/comision)',  'Dolaria',   'NaranjaX',      "BruBank",    'MEP',      'MESA',     'MAE'],
                                'VENTA':  [bull_venta,  bna_venta,  ggal_venta,  tiendadolar_venta,      icbc_venta,  bbva_venta,     ciudad_venta,  santander_venta,          iol_venta,          ppi_venta,  balanz_venta,   supv_venta,   buendolar_venta,         dolaria_venta, naranjax_venta, brubank_venta, mep_venta,  mesa_venta,  mae_venta]})
    tabla_venta = tabla_venta[tabla_venta['VENTA'] != 0].sort_values('VENTA',ascending=True).reset_index(drop=True)
        
    tabla_spread = pd.DataFrame({'.Broker': ['BullMarket','Bco_Nacion','Bco_Galicia','TiendaDolar',      'Bco_ICBC',   'Bco_BBVA',    'Bco_Ciudad',   'Bco_Santder',         '--> Dolariol.com <--',     'PPI',      'Balanz',     'Bco_Supervielle',     'BuenDolar(c/comision)', 'Dolaria',   'NaranjaX',       'BruBank',     'MEP',      'MESA',     'MAE'],
                                 'SPREAD': [bull_spread, bna_spread, ggal_spread, tiendadolar_spread,   icbc_spread,   bbva_spread,    ciudad_spread, santander_spread,         iol_spread,         ppi_spread, balanz_spread,    supv_spread,     buendolar_spread,        dolaria_spread,  naranjax_spread, brubank_spread, mep_spread, mesa_spread, mae_spread]})
    tabla_spread = tabla_spread[tabla_spread['SPREAD'] != 0].sort_values('SPREAD',ascending=True).reset_index(drop=True)

    tabla_comprador = pd.DataFrame({'Broker':       ['BullMarket',     'Bco_Nacion','Bco_Galicia',      'TiendaDolar',      'Bco_ICBC',      'Bco_BBVA',    'Bco_Ciudad',         'Bco_Santder',    '--> Dolariol.com <--',     'PPI',         'Balanz',      'Bco_Supervielle',     'BuenDolar(c/comision)',   'Dolaria',        "NaranjaX",        'BruBank',          'MEP',         'MESA'],
                                 'Sesgo_Comprador': [comprador_bull, comprador_bna, comprador_ggal, comprador_tiendadolar, comprador_icbc, comprador_bbva, comprador_ciudad, comprador_santander,       comprador_iol,     comprador_ppi, comprador_balanz,  comprador_supv,        comprador_buendolar,     comprador_dolaria, comprador_naranjax, comprador_brubank, comprador_mep, comprador_mesa]})
    tabla_comprador = tabla_comprador[tabla_comprador['Sesgo_Comprador'] > -0.2].sort_values('Sesgo_Comprador',ascending=True).reset_index(drop=True)

    tabla_vendedor = pd.DataFrame({'Broker': [        'BullMarket','Bco_Nacion','Bco_Galicia',      'TiendaDolar',      'Bco_ICBC',   'Bco_BBVA',    'Bco_Ciudad',   'Bco_Santder',       '--> Dolariol.com <--',     'PPI',        'Balanz',     'Bco_Supervielle',     'BuenDolar(c/comision)', 'Dolaria',       "NaranjaX",         'BruBank',        'MEP',      'MESA'],
                                 'Sesgo_Vendedor': [vendedor_bull, vendedor_bna, vendedor_ggal, vendedor_tiendadolar, vendedor_icbc, vendedor_bbva, vendedor_ciudad, vendedor_santander,    vendedor_iol,        vendedor_ppi, vendedor_balanz,  vendedor_supv,           vendedor_buendolar, vendedor_dolaria,  vendedor_naranjax, vendedor_brubank, vendedor_mep, vendedor_mesa]})
    tabla_vendedor = tabla_vendedor[tabla_vendedor['Sesgo_Vendedor'] > -0.2].sort_values('Sesgo_Vendedor',ascending=True).reset_index(drop=True)

    tabla = pd.concat([tabla_compra, tabla_venta, tabla_spread], axis=1, ignore_index=False, sort =False)
    tabla_total = pd.concat([tabla_compra, tabla_venta, tabla_spread, tabla_comprador, tabla_vendedor], axis=1, ignore_index=False, sort =False)

    
    tabla_pepe = pd.DataFrame({hora: [     'BullMarket','Bco_Nacion','Bco_Galicia','TiendaDolar',       'Bco_ICBC',  'Bco_BBVA',  'Bco_Ciudad',  'Bco_Santder',    '--> Dolariol.com <--', 'PPI',      'Balanz',       'Bco_Supervielle', 'BuenDolar(c/comision)', 'Dolaria',      "NaranjaX",       'BruBank',     'MEP',      'MESA',      'MAE'],
                                 'COMPRA': [bull_compra, bna_compra,  ggal_compra,  tiendadolar_compra, icbc_compra, bbva_compra, ciudad_compra, santander_compra, iol_compra,             ppi_compra, balanz_compra,  supv_compra,        buendolar_compra,       dolaria_compra,  naranjax_compra, brubank_compra, mep_compra, mesa_compra, mae_compra],
                                 'VENTA':  [bull_venta,  bna_venta,   ggal_venta,   tiendadolar_venta,  icbc_venta,  bbva_venta,  ciudad_venta,  santander_venta,  iol_venta,              ppi_venta,  balanz_venta,   supv_venta,         buendolar_venta,        dolaria_venta,   naranjax_venta,  brubank_venta,  mep_venta,  mesa_venta,  mae_venta],
                                 'SPREAD': [bull_spread, bna_spread,  ggal_spread,  tiendadolar_spread, icbc_spread, bbva_spread, ciudad_spread, santander_spread, iol_spread,             ppi_spread, balanz_spread,  supv_spread,        buendolar_spread,       dolaria_spread,  naranjax_spread, brubank_spread, mep_spread, mesa_spread, mae_spread]})
    tabla_pepe = tabla_pepe[tabla_pepe['VENTA'] != 0].sort_values(['VENTA','SPREAD'],ascending=[True,True]).reset_index(drop=True)  
    '''
    print(tabulate(tabla_pepe[[hora,'COMPRA','VENTA','SPREAD']],
                       headers='keys', tablefmt='fancy_grid', showindex=False, stralign="center", numalign="center"))
    print('--------------------------------------------------------------------------')
    

    print(tabulate(tabla[[hora,'COMPRA','Broker.','VENTA','.Broker','SPREAD']],
                       headers='keys', tablefmt='fancy_grid', showindex=False, stralign="center", numalign="center"))
    '''
    
    print('Cotizaciones actualizadas a las '+hora)
    cotizaciones.value = tabla_pepe
    cotizaciones2.value = tabla_total
    return


def correr_tabla(cotizaciones, cotizaciones2, hora_stop):
    now = datetime.datetime.now()
    while now.hour < hora_stop:
        try:
            tabla(cotizaciones, cotizaciones2)
        except Exception:
            traceback.print_exc()
            continue
        now = datetime.datetime.now()
    return
        
def correr_web(cotizaciones, cotizaciones2):
    web.web(cotizaciones, cotizaciones2)
    return

##############################################################################
'''                       Funcion GLOBAL                               '''
##############################################################################
def Global(): 
    if __name__ == "__main__":    
        now = datetime.datetime.now() #Hora en la que comienza la funcion        
        
        hora_stop = 18
        
        m = multiprocessing.Manager() #Declaro el Manager de multiprocessing
        cotizaciones = m.Value('d', 1) #Tabla de cotizaciones
        cotizaciones2 = m.Value('d', 1) #Tabla de cotizaciones
        p = multiprocessing.Pool(processes=50) #Declaro pool de workers
          
        app = Flask(__name__, template_folder='Y:\\Git\\Python-website\\templates')
        app.logger.removeHandler(default_handler) #Para quitar los IPs de la consola
        @app.route('/') # Asi indico que es la pagina principal
        def home():
            return render_template('home.html',  tables=[cotizaciones.value.to_html(classes='data', index=False)], titles=cotizaciones.value.columns.values)
        @app.route('/sesgos') # Creo una pagina de about en mi web
        def about():
            return render_template('sesgos.html',  tables=[cotizaciones2.value.to_html(classes='data', index=False)], titles=cotizaciones2.value.columns.values)

        try:
            p.starmap_async(correr_tabla, [(cotizaciones, cotizaciones2, hora_stop)])
            #app.run(host='192.168.0.202', debug=True, use_reloader=False) #Server de testing
            serve(app, host='192.168.0.202', port=5000) #Server de produccion - no se traba random
            
        except:
            traceback.print_exc()
        
        #Espero a que sean las 16hrs para liquidar parets and childs
        while now.hour < hora_stop:
            time.sleep(1)
            now = datetime.datetime.now()
        
        time.sleep(200) #Le doy un tiempo para que todos los workers hagan su ultima vuelta
        p.terminate() #Liquido pool de procesos
        p.join() #Joineo memoria del pool al main
      
    return


##############################################################################
'''                               MAIN                                 '''
##############################################################################
 

if __name__ == '__main__':
    now = datetime.datetime.now()
    Global()









'''
bbva = session.get('http://10.0.0.143:1234/CotizacionDolarMAE/Get')
bbva = json.loads(bbva.content)
bbva

bbva = session.get('http://10.0.0.143:1234/CotizacionDolarMAE/EstadoOperatoriaAutomatica')
bbva = json.loads(bbva.content)
bbva

'''








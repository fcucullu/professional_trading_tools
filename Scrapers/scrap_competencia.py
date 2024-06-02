#By Francisco Cucullu

import requests as rq
from bs4 import BeautifulSoup as bs
import json

#Me loggeo para obtener cookies
session = rq.Session()


''' BULL MARKET'''
def bullmarket():
    try:
        BullMarket = session.get('http://dolarhoy.bullmarketbrokers.com/')
        BullMarket = bs(BullMarket.content, 'xml')
        bull_compra = float(BullMarket.find_all('h4')[2].text[-5:].replace(',','.'))
        bull_venta = float(BullMarket.find_all('h4')[3].text[-5:].replace(',','.'))
    except:
        bull_compra = 0
        bull_venta = 0
    return bull_compra, bull_venta

'''BNA '''
def bna():
    try:
        BNA = session.get('http://www.bna.com.ar/Personas')
        BNA = bs(BNA.content, 'lxml')
        BNA_compra = float(BNA.find_all('td')[1].text.replace(',','.'))
        BNA_venta = float(BNA.find_all('td')[2].text.replace(',','.'))
    except:
        BNA_compra = 0
        BNA_venta = 0
    return BNA_compra, BNA_venta

''' GGAL '''
def ggal():
    try:
        ggal = session.get('https://www.bancogalicia.com/cotizacion/cotizar?currencyId=02&quoteType=SU&quoteId=999')
        ggal = json.loads(ggal.content)
        ggal_compra = float(ggal['buy'].replace(',','.'))
        ggal_venta = float(ggal['sell'].replace(',','.'))
    except:
        ggal_compra = 0
        ggal_venta = 0
    return ggal_compra, ggal_venta

''' TIENDA DOLAR '''
def tiendadolar():
    try:
        tiendadolar = session.get('https://tiendadolar.com.ar/api/v2/price/get_base_price')
        tiendadolar = json.loads(tiendadolar.content)
        tiendadolar_compra = tiendadolar['compra']
        tiendadolar_venta = tiendadolar['venta']
    except:
        tiendadolar_compra = 0
        tiendadolar_venta = 0 
    return tiendadolar_compra, tiendadolar_venta

''' ICBC'''
def icbc():
    try:
        icbc = session.get('https://www.icbc.com.ar/ICBC_CotizacionMonedaWEB/cotizacion/dolar')
        icbc = json.loads(icbc.content)
        icbc_compra = float(icbc['valorCompra'].replace(',','.'))
        icbc_venta = float(icbc['valorVenta'].replace(',','.'))
    except:
        icbc_compra = 0
        icbc_venta = 0
    return icbc_compra, icbc_venta

''' BBVA'''
def bbva():
    try:
        bbva = session.get('https://hb.bbv.com.ar/fnet/mod/inversiones/NL-dolareuro.jsp')
        bbva = bs(bbva.content, 'xml')
        bbva_compra = float(bbva.find_all('td')[1].text.replace(',','.'))
        bbva_venta = float(bbva.find_all('td')[2].text.replace(',','.'))
    except:
        bbva_compra = 0
        bbva_venta = 0
    return bbva_compra, bbva_venta

''' CIUDAD '''
def ciudad():
    try:
        ciudad = session.get('https://www.bancociudad.com.ar/institucional/herramientas/getCotizaciones', timeout=10)
        ciudad = json.loads(ciudad.content)
        ciudad_compra = float(ciudad['data']['dolar']['compra'][-6:].replace(',','.'))
        ciudad_venta = float(ciudad['data']['dolar']['venta'][-6:].replace(',','.'))
    except:
        ciudad_compra = 0
        ciudad_venta = 0
    return ciudad_compra, ciudad_venta

''' SANTANDER '''
def santander():
    try:
        santander = session.get('https://banco.santanderrio.com.ar/exec/cotizacion/index.jsp')
        santander = bs(santander.content, 'xml')
        santander_compra = float(santander.find_all('td')[1].text[-6:].replace(',','.'))
        santander_venta = float(santander.find_all('td')[2].text[-6:].replace(',','.'))
    except:
        santander_compra = 0
        santander_venta = 0       
    return santander_compra, santander_venta

''' INVERTIR EN BOLSA '''
def ieb():
    try:
        ieb = session.get('https://invertirenbolsa.com.ar/inversion-dolares')
        ieb = bs(ieb.content, 'xml')
        ieb_compra = float(ieb.find_all('td')[1].text[-6:].replace(',','.'))
        ieb_venta = float(ieb.find_all('td')[2].text[-6:].replace(',','.'))
    except:
        ieb_compra = 0
        ieb_venta = 0
    return ieb_compra, ieb_venta

''' IOL '''
def iol():
    try:
        iol = session.get('https://dolar.invertironline.com/')
        iol = bs(iol.content, 'xml')
        iol_compra = float(iol.find(class_="precio-compra").text.replace(',','.'))
        iol_venta = float(iol.find(class_="precio-venta").text.replace(',','.'))
    except:
        iol_compra = 0
        iol_venta = 0
    return iol_compra, iol_venta

''' PORTFOLIO PERSONAL '''    
def ppi(): 
    try:
        data = {
        'AuthorizedClient': '321321321',
        'ClientKey': 'pp123456',
        'Referer': 'https://api.portfoliopersonal.com/Content/html/proxy.html'}
        ppi = session.get('https://api.portfoliopersonal.com/api/Cotizaciones/CotizacionActualDolarPPI', headers=data)
        ppi = json.loads(ppi.content)
        ppi_compra = float(ppi['payload']['bids'][0]['precio'])
        ppi_venta = float(ppi['payload']['offers'][0]['precio'])
    except:
        ppi_compra = 0
        ppi_venta = 0
    return ppi_compra, ppi_venta

''' BALANZ '''
def balanz():
    try:    
        data = {'authority': 'dolarbalanz.com',
                'method': 'GET',
                'path': '/api/dolarBalanz',
                'scheme': 'https',
                'accept': 'application/json'}
        balanz = session.get('https://dolarbalanz.com/api/dolarBalanz', headers=data, cookies=dict(session.cookies.items()))
        balanz = json.loads(balanz.content)
        balanz_compra = balanz['precioCompraVenta'][0]['preciocompra']
        balanz_venta = balanz['precioCompraVenta'][0]['precioventa']
    except:
        balanz_compra = 0
        balanz_venta = 0
    return balanz_compra, balanz_venta

''' SUPV '''
def supv():
    try:
        supv = session.get('https://personas.supervielle.com.ar/Pages/QuotesPanel/Quotes.aspx')
        supv = bs(supv.content, 'lxml')
        supv = supv.find_all('td')[1]
        supv_compra = float(supv.find_all('td')[1].text.replace(',','.'))
        supv_venta = float(supv.find_all('td')[2].text.replace(',','.'))
    except:
        supv_compra = 0
        supv_venta = 0
    return supv_compra, supv_venta

''' BUENDOLAR '''
def buendolar():
    try:
        buendolar = session.get('https://be.buendolar.com/api/market/ticker/?format=json')
        buendolar = json.loads(buendolar.content)
        buendolar_compra = round(float(buendolar['object']['purchase_price']) ,2)
        buendolar_compra_cometa = round(float(buendolar_compra*0.005) ,2)
        buendolar_compra = round( buendolar_compra - (buendolar_compra_cometa*1.21) ,2)

        buendolar_venta = round(float(buendolar['object']['selling_price']) ,2)
        buendolar_venta_cometa = round(float(buendolar_venta*0.005 ),2)
        buendolar_venta = round( buendolar_venta + (buendolar_venta_cometa*1.21) ,2)
    except:
        buendolar_compra = 0
        buendolar_venta = 0
    return buendolar_compra, buendolar_venta

''' DOLARIA '''
def dolaria():
    try:
        dolaria = session.get('https://www.dolaria.com.ar/Api/Data/0/GetCotizaciones')
        dolaria = json.loads(dolaria.content)
        dolaria_compra = round(dolaria['Cotizaciones'][0]['PrecioCompra'] ,2)
        dolaria_venta = round(dolaria['Cotizaciones'][0]['PrecioVenta'] ,2)
    except:
        dolaria_compra = 0
        dolaria_venta = 0
    return dolaria_compra, dolaria_venta

''' NaranjaX '''
def naranjax():
    path = r"Y:\Git\APKs\NaranjaX\informe.txt"
    f= open(path,"r")
    contenido = f.read()
    try:
        last = contenido.split('\n')[-2]
        naranjax_venta = float(last.split(' - ')[2])
        naranjax_compra = float(last.split(' - ')[1])
    except:
        naranjax_compra, naranjax_venta = 0, 0
    f.close()
    return naranjax_compra, naranjax_venta

''' BRUBANK ''' 
def brubank():
    brubank = session.get('https://drdolar.com/')
    brubank = bs(brubank.content, 'lxml')
    i = 0
    brubank_compra = 0
    brubank_venta = 0
    while i < 50:
        data = brubank.find_all('tr')[i].text
        if 'Brubank' in data:
            data = data.split('$')
            brubank_compra = float(data[1][:5].replace(',','.'))
            brubank_venta = float(data[2][:5].replace(',','.'))
            break
        i += 1
    
    return brubank_compra, brubank_venta




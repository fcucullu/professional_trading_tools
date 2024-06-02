import requests

from Quote import Quote
from token_iol import Token

class Requests:
    def __init__(self):
        self.base_url = 'https://api.invertironline.com/'
        self.token = None
        self.logged = False

    def get_token(self):
        payload = {'username': 'cprueba', 'password': 'testeo123', 'grant_type': 'password'}
        request = requests.post(self.base_url + 'token', data=payload)
        #print("Request enviada, HTTP STATUS CODE {}".format(request.status_code))

        self.token = Token(response=request.json())
        self.logged = self.token.is_valid()

    def refresh_token(self):
        payload = {'refresh_token': self.token.refresh, 'grant_type': 'refresh_token'}
        request = requests.post(self.base_url + 'token', data=payload)
        #print("Refresh enviado, HTTP STATUS CODE {}".format(request.status_code))
        self.token = Token(response=request.json())

    def get_header(self):
        if not self.logged:
            self.get_token()

        if not self.token.is_valid():
            self.refresh_token()

        return {'Authorization': 'Bearer ' + self.token.access}
       
    def cotizacion(self, simbolo: str, mercado: str, plazo: str):
        req = requests.get(self.base_url + 'api/{}/Titulos/{}/Cotizacion'.format(mercado, simbolo), headers=self.get_header())
        #print("Obteniendo cotizacion de {}, HTTP STATUS CODE {}".format(simbolo, req.status_code))
        req.raise_for_status()
        response = req.json()
        return response
    
    def ultimoPrecio(self, simbolo: str, mercado: str, plazo: str):
        req = requests.get(self.base_url + 'api/{}/Titulos/{}/cotizacion?plazo={}'.format(mercado, simbolo, plazo), headers=self.get_header())
        #print("Obteniendo cotizacion de {}, HTTP STATUS CODE {}".format(simbolo, req.status_code))
        req.raise_for_status()
        response = req.json()
        return response['ultimoPrecio']
    
    def puntas(self, simbolo: str, mercado: str, plazo: str):
        req = requests.get(self.base_url + 'api/{}/Titulos/{}/cotizacion?plazo={}'.format(mercado, simbolo, plazo), headers=self.get_header())
        #print("Obteniendo cotizacion de {}, HTTP STATUS CODE {}".format(simbolo, req.status_code))
        req.raise_for_status()
        response = req.json()
        try:
            respuesta = response['puntas'][0] #Suma las cantidades con mismo precio
        except:
            respuesta = {'cantidadCompra': 0.0, 
                         'precioCompra': 0.0,
                         'precioVenta': 0.0,
                         'cantidadVenta': 0.0}
        return respuesta
    
    def serie_diaria(self, simbolo: str, fechaDesde: str, fechaHasta: str):
        req = requests.get(self.base_url + 'api/bcba/titulos/{}/cotizacion/seriehistorica/{}/{}/ajustada'.format(simbolo, fechaDesde, fechaHasta), headers=self.get_header())
        #print("Obteniendo serie histórica de {}, HTTP STATUS CODE {}".format(simbolo, req.status_code))
        req.raise_for_status()
        response = req.json()
        precios = []
        for i in range(len(response)):
            precios.append(response[i]['ultimoPrecio'])
        return response
    
    def serie_intradiaria(self, simbolo: str, fechaDesde: str, fechaHasta: str):
        req = requests.get(self.base_url + 'api/bcba/titulos/{}/cotizacion/seriehistorica/{}/{}/sinAjustar'.format(simbolo, fechaDesde, fechaHasta), headers=self.get_header())
        #print("Obteniendo serie histórica de {}, HTTP STATUS CODE {}".format(simbolo, req.status_code))
        req.raise_for_status()
        response = req.json()
        precios = []
        for i in range(len(response)):
            precios.append(response[i]['ultimoPrecio'])
        return precios
        


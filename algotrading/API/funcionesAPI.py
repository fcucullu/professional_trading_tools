import requests

from Quote import Quote
from token_iol import Token

class Requests:
    def __init__(self):
        self.base_url = 'https://api.invertironline.com/'
        #self.get_token()
        self.token = None
        self.logged = False

    def get_token(self):
        payload = {'username': 'algotrading', 'password': 'fcucullu1', 'grant_type': 'password'}
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
        req = requests.get(self.base_url + 'api/v2/bcba/titulos/{}/cotizacion/seriehistorica/{}/{}/ajustada'.format(simbolo, fechaDesde, fechaHasta), headers=self.get_header())
        #print("Obteniendo serie histórica de {}, HTTP STATUS CODE {}".format(simbolo, req.status_code))
        req.raise_for_status()
        response = req.json()
        precios = []
        for i in range(len(response)):
            precios.append([response[i]['fechaHora'], response[i]['ultimoPrecio']])
        return precios
    
    def serie_intradiaria(self, simbolo: str, fechaDesde: str, fechaHasta: str):
        req = requests.get(self.base_url + 'api/bcba/titulos/{}/cotizacion/seriehistorica/{}/{}/sinAjustar'.format(simbolo, fechaDesde, fechaHasta), headers=self.get_header())
        #print("Obteniendo serie histórica de {}, HTTP STATUS CODE {}".format(simbolo, req.status_code))
        req.raise_for_status()
        response = req.json()
        precios = []
        for i in range(len(response)):
            precios.append([response[i]['fechaHora'], response[i]['ultimoPrecio']])
        return precios
        
    
    
##############################################################################
'''                  POSTS       -  ¡¡¡AHORA EN PRODUCCION!!!!             '''
##############################################################################

class Sandbox:
    def __init__(self):
        #◙self.base_url = 'http://testing-api.invertironline.com/'
        self.base_url = 'https://api.invertironline.com/'
        #self.get_token()
        self.token = None
        self.logged = False

    def get_token(self):
        #payload = {'username': 'algotrading997', 'password': 'testeo123', 'grant_type': 'password'}
        payload = {'username': 'algotrading', 'password': 'fcucullu1', 'grant_type': 'password'}
        request = requests.post(self.base_url + 'token', data=payload)
        #print("Request enviada, HTTP STATUS CODE {}".format(request.status_code))

        self.token = Token(response=request.json())
        self.logged = self.token.is_valid()
        
        return self.token.access

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
    
    def get_header_operate(self):
        if not self.logged:
            self.get_token()
            print('SE OBTIENE TOKEN POR NO ESTAR LOGEADO')

        if not self.token.is_valid():
            self.refresh_token()
            print('SE REFRESCA TOKEN POR EXPIRACION')

        return {'Authorization': 'Bearer ' + self.token.access, 'Content-Type': 'application/x-www-form-urlencoded'}
    
    #####################################
    '''            OPERAR             '''    
    #####################################
    
    def saldo_arg_pesos_inmediato(self, token):
        headers = {'Authorization': 'Bearer ' + token.value}
        req = requests.get(self.base_url + 'api/v2/estadocuenta', headers=headers)
        return req.json()['cuentas'][0]['saldos'][0]['disponibleOperar']
        #Info de cuentas -> Cuenta de Argentina en Pesos -> Seccion de saldos -> Seccion Inmediato ->Disponible para operar
    
    def saldo_arg_pesos_inmediato_notok(self):
        req = requests.get(self.base_url + 'api/v2/estadocuenta', headers=self.get_header())
        return req.json()['cuentas'][0]['saldos'][0]['disponibleOperar']
        #Info de cuentas -> Cuenta de Argentina en Pesos -> Seccion de saldos -> Seccion Inmediato ->Disponible para operar
    
    def saldo_arg_dolares_inmediato(self, token):
        headers = {'Authorization': 'Bearer ' + token.value}
        req = requests.get(self.base_url + 'api/v2/estadocuenta', headers=headers)
        return req.json()['cuentas'][1]['saldos'][0]['disponibleOperar']
        #Info de cuentas -> Cuenta de Argentina en Pesos -> Seccion de saldos -> Seccion Inmediato ->Disponible para operar
    
    def saldo_arg_dolares_inmediato_notok(self):
        req = requests.get(self.base_url + 'api/v2/estadocuenta', headers=self.get_header())
        return req.json()['cuentas'][1]['saldos'][0]['disponibleOperar']
        #Info de cuentas -> Cuenta de Argentina en Pesos -> Seccion de saldos -> Seccion Inmediato ->Disponible para operar
    
    def portafolio_arg(self):
        req = requests.get(self.base_url + 'api/v2/portafolio/argentina', headers=self.get_header())
        return req.json()
    
    def comprar(self, simbolo:str, cantidad: float, precio: float, plazo: str, hoy, token):
        headers = {'Authorization': 'Bearer ' + token.value,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        
        body = {'mercado': 'BCBA',
                'simbolo': simbolo,
                'cantidad': cantidad,
                'precio': precio,
                'plazo': plazo,
                'validez': hoy}
        req = requests.post(self.base_url + 'api/v2/operar/Comprar', headers=headers, data=body)
        req.raise_for_status()  
        
        if req.status_code != 201:
            print("\nError en la COMPRA de "+simbolo +" "+str(cantidad)+" @ "+str(precio))
            print(req.json())
            return req.json()
        
        return req.json()['numeroOperacion']
    
    def vender(self, simbolo:str, cantidad: float, precio: float, plazo: str, hoy, token):
        headers = {'Authorization': 'Bearer ' + token.value,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        
        body = {'mercado': 'BCBA',
                'simbolo': simbolo,
                'cantidad': cantidad,
                'precio': precio,
                'plazo': plazo,
                'validez': hoy}
        req = requests.post(self.base_url + 'api/v2/operar/Vender', headers=headers, data=body)
        req.raise_for_status()  
        
        if req.status_code != 201:
            print("\nERROR en la VENTA de "+simbolo +" "+str(cantidad)+" @ "+str(precio))
            print(req.json())
            return req.json()
        
        return req.json()['numeroOperacion']
    
    
    def tr_check(self, tr: int, token):
        import traceback
        
        headers= {'Authorization': 'Bearer ' + token.value}
        
        req = requests.get(self.base_url + 'api/v2/operaciones/{}'.format(tr), headers=headers)
        req.raise_for_status()
        
        precios = []
        cantidades = []
        try:
            rango = range(len(req.json()['operaciones'])) #Se fija cuantas operaciones tuvo
            for i in rango:
                precios.append(req.json()['operaciones'][i]['precio']) #Arma una lista de todos los precios operados
                cantidades.append(req.json()['operaciones'][i]['cantidad']) #Arma una lista de todas las cantidades operadas
            
            cantidad = sum(cantidades)
            suma = 0
            #Ahora calculo el precio ponderado de la operacion
            if cantidad > 0: #Filtro por que en ese caso no se puede dividir por cero.
                for i in rango: suma += (precios[i]*cantidades[i]) #calculo el denominador de la sumaproducto
                precio = suma/cantidad #Precio calculado por sumapruducto = Precio ponderado
            else:
                precio = 0 #sin cantidad operada, seteo el precio = 0
                
            return req.json()['estadoActual'], [cantidad, precio]
        
        except Exception:
            print(' --- HUBO UN ERROR EN EL FUNCION CHECK PARA LA TR {} --- '.format(tr))
            traceback.print_exc()
        
 
    def tr_delete(self, tr: int, token):
        import time
        
        headers= {'Authorization': 'Bearer ' + token.value}
        try:
            req = requests.delete(self.base_url + 'api/v2/operaciones/{}'.format(tr), headers=headers)
            req.raise_for_status()
        except:
            pass
        
        intentos = 0
        while self.tr_check(tr, token)[0] != 'terminada' and self.tr_check(tr, token)[0] != 'cancelada': #Contingencia si la tr no esta en estado 4 o 5
            if intentos > 0 and intentos%3 == 0:
                print("\n¡¡¡ URGENTE !!!: CANCELAR TR {} DEL CC 127".format(tr)) #Mensaje de urgencia cuando la tr esta mas de 10 segundos pendiente de cancelacion
            intentos += 1
            time.sleep(1)
            
        return self.tr_check(tr, token) #Devuelve estado + cantidad y monto  
    
    
    def tr_controlar(self, tr: int):
        
        req = requests.get(self.base_url + 'api/v2/operaciones/{}'.format(tr), headers=self.get_header())
        req.raise_for_status()
                    
        return req.json()['estados']
    
    
    def vender_dolar(self, moneda: str, monto: float, token):
        headers = {'Authorization': 'Bearer ' + token.value,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        
        body = {'MonedaMonto': moneda, #peso_Argentino o Dolar_Estadounidense
                'Monto': monto}
        
        req = requests.post(self.base_url + 'api/v2/Dolar/Vender', headers=headers, data=body)
        req.raise_for_status()  
        
        if req.status_code != 200:
            print("\nERROR en la VENTA de DOLARES")
            print(req.json())
            return req.json()
        
        return req.json()['nroOperacion']
    
    
    def comprar_dolar(self, moneda: str, monto: float, token):
        headers = {'Authorization': 'Bearer ' + token.value,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        
        body = {'MonedaMonto': moneda, #peso_Argentino o Dolar_Estadounidense
                'Monto': monto}
        
        req = requests.post(self.base_url + 'api/v2/Dolar/Comprar', headers=headers, data=body)
        req.raise_for_status()  
        
        if req.status_code != 200:
            print("\nERROR en la COMPRA de DOLARES")
            print(req.json())
            return req.json()
        
        return req.json()['nroOperacion']


  
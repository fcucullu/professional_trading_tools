from datetime import datetime

class Quote:
    def __init__(self, response):
        self.open = response['apertura']
        self.high = response['maximo']
        self.low = response['minimo']
        self.close = response['ultimoPrecio']
        self.fecha = datetime.strptime(response['fechaHora'], '%a, %d %b %Y %H:%M:%S %Z')

'''

import dateutil.parser
yourdate = dateutil.parser.parse(datestring)'''
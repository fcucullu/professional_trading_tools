#By Francisco Cucullu


''' QUEDA INUTILIZADO POR QUE AHORA SE CORRE DESDE SCRAP_DOLARES.PY '''
from flask import Flask, render_template
import sys
sys.path.append(r'Y:\Git\Python-website\templates')


def web():
    app = Flask(__name__, template_folder='Y:\\Git\\Python-website\\templates')
    
    df = cotizaciones.value
    
    @app.route('/') # Asi indico que es la pagina principal
    def home():
        return render_template('home.html',  tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)
    
    @app.route('/about') # Creo una pagina de about en mi web
    def about():
        return render_template('about.html')
    
    #if __name__ == '__main__':
    app.run(host='192.168.0.202', debug=True, use_reloader=False)

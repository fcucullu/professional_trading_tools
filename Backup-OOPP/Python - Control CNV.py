# By Francisco Cucullu

#Importo funciones propias
import sys
sys.path.append(r'Y:\Git\Funciones')
import FuncionesFrancisco as FF
import time

#Detecto username
user = FF.ReconocerUsuario()

#Detecto dia
(DIA, MES, AÑO) = FF.DetectaDia()

#Descargo el archivo de CNV correspondiente al día de la fecha
FF.DescargarCNV(AÑO,MES,DIA)

#le pido a python que espere, ya que no todas las PCs tienen alta velocidad
time.sleep(15)

#Muevo el archivo desde descargas a la ruta correspondiente al dia de la fecha
RutaOrigen = "C:\\Users\\"+user+"\\Downloads\\"+AÑO+MES+DIA+"AG151.xls"
RutaDestino = "Y:\\1- IOL Sociedad de Bolsa SA\\Controles\\Control de boletos\\Archivos Control de boletos\\"+AÑO+MES+"\\"+AÑO+MES+DIA+"\\"+AÑO+MES+DIA+"AG151.xls"
FF.MoverArchivos(RutaOrigen, RutaDestino)

#Abro el archivo
Ruta = r'Y:\1- IOL Sociedad de Bolsa SA\Controles\Control de boletos\Control CNV.xlsm'
FF.AbrirArchivo(Ruta)

#le pido a python que espere, ya que no todas las PCs tienen alta velocidad
time.sleep(15)

#Correr macros
FF.EjecutarMacroYAABIERTO(Ruta,"LimpiarArchivo")
FF.EjecutarMacroYAABIERTO(Ruta,"Traer_info")
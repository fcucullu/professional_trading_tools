# By Francisco Cucullu

from tkinter import Tk, ttk, Label, Entry, messagebox, Button
import sys
path = r'Y:\Git\algotrading\API'
path2 = r'Y:\Git\Funciones'
sys.path.append(path)
sys.path.append(path2)
from funcionesAPI import Sandbox
sandbox = Sandbox()
import FuncionesFrancisco as FF
dia, mes, ano = FF.DetectaDia()
hoy = str(ano+"-"+mes+"-"+dia) 
import numpy as np
import pandas as pd
import time

##############################################################################
'''                     Ventana de la aplicacion                           '''
##############################################################################

def ventana(cotizaciones, inputs_compra, inputs_venta, semaforo, lock):
    #Parametros de la ventana 
    window = Tk()
    window.title("Ejecutar Dolar MEP") #Titulo de la ventana
    window.geometry('450x150') #Para establecer el tamaño de la ventana
    window.configure(background='black')
     
    #Parametros de las labels
    lbl1 = Label(window, text="Bono", font=("Arial Bold", 20), bg="black", fg="white") #Label fija
    lbl1.grid(column=0, row=0, sticky='W') #Siempre es necesario establecer la posicion de la label
    lbl2 = Label(window, text="Dolares", font=("Arial Bold", 20), bg="black", fg="white") #Label fija
    lbl2.grid(column=0, row=1, sticky='W') 
    lbl3 = Label(window, text="Side", font=("Arial Bold", 20), bg="black", fg="white") #Label fija
    lbl3.grid(column=0, row=2, sticky='W') 
    
    txt = Entry(window,width=10, font=("Arial Bold", 20)) #Cuadro te texto para ingresar data
    txt.grid(column=1, row=1, columnspan=2)
    txt.focus()
    
    combo = ttk.Combobox(window, width=10, font=("Arial Bold", 20))
    combo['values']= ("AY24", "DICA", "AO20")
    combo.current(0) #set the selected item
    combo.grid(column=1, row=0, columnspan=2)
    
    #Codigos de especie
    lista = pd.read_csv('Y:\\Git\\algotrading\\Dolar\\tickers_MEP.csv', sep=';', decimal=',')
    
    #Funciones
    def clicked_compra():
        if txt.get() == "":
            messagebox.showwarning('Operación NO enviada',"¡Debe cargar la cantidad de dolares que quiere operar!")
        elif semaforo.value != 0:
            messagebox.showwarning('Operación NO enviada',"Hay operaciones en curso!")            
        else:
            ticker = combo.get() #Detecto que ticker selecciono operar
            codigoP = int(lista.loc[lista.iloc[:,0] == ticker, 'ID'].item())
            #codigoD = float(lista.loc[lista.iloc[:,0] == ticker, 'par dolar'].item())
            row = np.where(cotizaciones.value[:,0] == np.array(codigoP).item()) #Detecto la fila dentro de la tabla de coti.
            precioP = cotizaciones.value[row,5].item()
            precioD = cotizaciones.value[row,9].item()
            dolares = int( txt.get() )
            cantidad = int((dolares / precioD) * 100)
            
            lock.acquire()
            inputs_compra.value = [ticker, cantidad, precioP, hoy]
            time.sleep(2)
            inputs_venta.value = [ticker+"D", cantidad, precioD, hoy]
            semaforo.value = 1
            lock.release()
            
            res = ["Compra de " + str(cantidad) + " " + str(ticker) + " a $" + str(precioP),
                   "Venta de " + str(cantidad) + " " + str(ticker) + "D" + " a U$D" + str(precioD)]
            messagebox.showinfo('Operación enviada', "\n".join(res))
            txt.delete(0, 100) #Para limpiar el campo desde el caracter 0 hasta el 100
    
    def clicked_venta():
        if txt.get() == "":
            messagebox.showwarning('Operación NO enviada',"¡Debe cargar la cantidad de dolares que quiere operar!")
        elif semaforo.value != 0:
            messagebox.showwarning('Operación NO enviada',"Hay operaciones en curso!")            
        else:
            ticker = combo.get() #Detecto que ticker selecciono operar
            codigoP = int(lista.loc[lista.iloc[:,0] == ticker, 'ID'].item())
            #codigoD = float(lista.loc[lista.iloc[:,0] == ticker, 'par dolar'].item())
            row = np.where(cotizaciones.value[:,0] == np.array(codigoP).item()) #Detecto la fila dentro de la tabla de coti.
            precioP = cotizaciones.value[row,3].item()
            precioD = cotizaciones.value[row,11].item()
            dolares = int( txt.get() )
            cantidad = int((dolares / precioD) * 100)
            
            lock.acquire()
            inputs_compra.value = [ticker+"D", cantidad, precioD, hoy]
            time.sleep(2)
            inputs_venta.value = [ticker, cantidad, precioP, hoy]
            semaforo.value = 1
            lock.release()
            
            res = ["Venta de " + str(cantidad) + " " + str(ticker) + " a $" + str(precioP),
                   "Compra de " + str(cantidad) + " " + str(ticker) + "D" + " a U$D" + str(precioD)]
            messagebox.showinfo('Operación enviada', "\n".join(res))
            txt.delete(0, 100) #Para limpiar el campo desde el caracter 0 hasta el 100
    
    
    #Botones
    btn_comprar = Button(window, width=9, text="COMPRAR", command=clicked_compra, bg="green", fg="black", font=("Arial Bold", 20))
    btn_comprar.grid(column=2, row=2)
    btn_vender = Button(window, width=9, text="VENDER", command=clicked_venta, bg="red", fg="black", font=("Arial Bold", 20))
    btn_vender.grid(column=1, row=2)
    
    window.mainloop() #Con esto hago que aparezca la ventana hasta que la cierre manualmente

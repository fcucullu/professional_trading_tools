from appium import webdriver #importo el WebDriver para que maneje todo automaticamente
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import traceback
import time
from datetime import datetime
now = datetime.now()
path = r"Y:\Git\APKs\NaranjaX\informe.txt"

#Declaro las Desired Capabilities
desired_cap = {
            "platformName": "Android",
            "deviceName": "Emulador1",
            "udid": "emulator-5554",
            "appPackage": "com.tarjetanaranja.ncuenta",
            "appActivity": "com.naranja.ncuenta.app.ui.StartupActivity",
            #"app": "Y:\\Git\\APKs\\NaranjaX\\base.apk",
            "newCommandTimeout": 3000
}

#Invoco el driver.
#el primer parámetro lo saco de appium y le agrego al final "/wb/hub"
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
driver.implicitly_wait(60) # Busca por 30 segundos entre cada accion
wait = WebDriverWait(driver, 30)

try:
    # Clickea en el boton de siguiente
    wait.until(EC.element_to_be_clickable((By.ID, "com.tarjetanaranja.ncuenta:id/walkthrough_buttn_slide"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "com.tarjetanaranja.ncuenta:id/walkthrough_buttn_slide"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "com.tarjetanaranja.ncuenta:id/walkthrough_buttn_slide"))).click()
    
    # Clickea en el boton de aceptar los terminos y condiciones
    wait.until(EC.element_to_be_clickable((By.ID, 'com.tarjetanaranja.ncuenta:id/walkthrough_buttn_tyc'))).click()
    
    #Completo los datos del formulario
    wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.EditText[@resource-id='dni']"))).send_keys("quantdevelopings@gmail.com")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.EditText[@resource-id='password']"))).send_keys("2802")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.Button[@text='Ingresar']"))).click()
       
    #Voy a la solapa de Dolares
    wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='DÓLARES']")))
    time.sleep(10) #Si no pongo este wait no se clickea!
    wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='DÓLARES']"))).click()

    #Lo abro y lo cierro para dejarlo en blanco. el "w+" es para crearlo en caso que no exista
    if now.hour < 11:
        f= open(path,"w+")
        f.close()
except:
    traceback.print_exc()



while now.hour < 17:
    
    hora = datetime.now().strftime("%H:%M")
    
    #Extraigo los datos de compra y de venta
    venta = wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.tarjetanaranja.ncuenta:id/menu_item_text'])[2]"))).text
    venta = float(venta.split("$")[1].replace(',','.'))
    compra = wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.tarjetanaranja.ncuenta:id/menu_item_text'])[3]"))).text
    compra = float(compra.split("$")[1].replace(',','.'))

    #Abro el archivo en modo append y guardo la data nueva
    f= open(path,"a+")
    f.write(hora + " - " + str(compra) + " - " + str(venta) +"\n")
    f.close()
    
    time.sleep(60)
    now = datetime.now()
    
    

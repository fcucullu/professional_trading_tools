# By Francisco Cucullu
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
            "deviceName": "Emulador2",
            "udid": "emulator-5556",
            "appPackage": "com.brubank",
            "appActivity": "com.brubank.android.ui.activities.LandingActivity",
            "newCommandTimeout": 3000
}

#Invoco el driver.
#el primer parámetro lo saco de appium y le agrego al final "/wb/hub"
driver = webdriver.Remote("http://localhost:4724/wd/hub", desired_cap)
driver.implicitly_wait(60) # Busca por 30 segundos entre cada accion
wait = WebDriverWait(driver, 30)

'''try:'''
# Clickea en el boton de iniciar sesion
wait.until(EC.element_to_be_clickable((By.ID, "com.brubank:id/login_button"))).click()

#Completo los datos del formulario
wait.until(EC.element_to_be_clickable((By.ID, "com.brubank:id/login_email_field"))).send_keys("quantdevelopings@gmail.com")
wait.until(EC.element_to_be_clickable((By.ID, "com.brubank:id/login_email_continue_button"))).click()
   
#Ingresa clave
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[9]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[6]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[5]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[2]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[8]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[5]"))).click()

# Confirmo el nuevo dispositivo
wait.until(EC.element_to_be_clickable((By.ID, "com.brubank:id/information_primary_button"))).click()
wait.until(EC.element_to_be_clickable((By.ID, "com.brubank:id/information_primary_button"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Updates']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.view.View[contains(@content-desc,'Link para ingresar a Brubank')])[1]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.view.View[@text='INGRESÁ'])[1]"))).click()

#Ingresa clave
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[9]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[6]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[5]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[2]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[8]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "(//android.widget.TextView[@resource-id='com.brubank:id/pin_title'])[5]"))).click()






    #Lo abro y lo cierro para dejarlo en blanco. el "w+" es para crearlo en caso que no exista
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
    
    
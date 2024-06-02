using NUnit.Framework;
using OpenQA.Selenium;
using OpenQA.Selenium.Appium;
using OpenQA.Selenium.Appium.Android;
using OpenQA.Selenium.Appium.Enums;
using OpenQA.Selenium.Support.UI;
using System;
using System.IO;
using System.Threading;

namespace Tests
{
    public class Tests
    {
        private WebDriverWait wait;
        private AppiumDriver<AndroidElement> driver;
        public string apkDir, textDir;

        [SetUp]
        public void SetUp()
        {
            apkDir = Path.Combine(Directory.GetParent(Directory.GetCurrentDirectory()).Parent.Parent.Parent.FullName, @"APK\base.apk");
            textDir = Path.Combine(Directory.GetParent(Directory.GetCurrentDirectory()).Parent.Parent.Parent.FullName, @"APK\informe.txt");

            AppiumOptions cap = new AppiumOptions();
            cap.AddAdditionalCapability(MobileCapabilityType.PlatformName, "android");
            cap.AddAdditionalCapability(MobileCapabilityType.PlatformVersion, "9");
            cap.AddAdditionalCapability(MobileCapabilityType.DeviceName, "emulator-5554");
            cap.AddAdditionalCapability(MobileCapabilityType.App, apkDir);
            cap.AddAdditionalCapability("appActivity", "com.naranja.ncuenta.app.ui.StartupActivity");
            cap.AddAdditionalCapability("appPackage", "com.tarjetanaranja.ncuenta");
            driver = new AndroidDriver<AndroidElement>(new Uri("http://127.0.0.1:4723/wd/hub"), cap, TimeSpan.FromSeconds(90));

            wait = new WebDriverWait(driver, TimeSpan.FromSeconds(30));

            //driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(15);

            //driver.InstallApp(apkDir);
        }

        [Test]
        public void Test1()
        {
            wait.Until(d => d.FindElement(By.XPath("//android.widget.TextView[@text='Siguiente']"))).Click();
            wait.Until(d => d.FindElement(By.XPath("//android.widget.TextView[@text='Siguiente']"))).Click();
            wait.Until(d => d.FindElement(By.XPath("//android.widget.TextView[@text='Siguiente']"))).Click();

            Thread.Sleep(1000);

            wait.Until(d => d.FindElement(By.XPath("//android.widget.TextView[@text='Aceptar']"))).Click();

            Thread.Sleep(1000);

            wait.Until(d => d.FindElement(By.XPath("//android.widget.EditText[@resource-id='dni']"))).SendKeys("thetesting24@gmail.com");
            wait.Until(d => d.FindElement(By.XPath("//android.widget.EditText[@resource-id='password']"))).SendKeys("8426");
            wait.Until(d => d.FindElement(By.XPath("//android.widget.Button[@text='Ingresar']"))).Click();

            Thread.Sleep(1000);

            wait.Until(d => d.FindElement(By.XPath("//android.widget.ImageView[@resource-id='com.tarjetanaranja.ncuenta:id/icon_cancel']"))).Click();

            wait.Until(d => d.FindElement(By.XPath("//android.widget.TextView[@text='DÓLARES']"))).Click();

            //var fecha = DateTime.Now.ToString("dd/MM/yyyy");
            //var hora = DateTime.Now.ToString("HH:mm");

            //string linea;
            //var compra = wait.Until(d => d.FindElement(By.XPath(
            //        "(//android.widget.TextView[@resource-id='com.tarjetanaranja.ncuenta:id/menu_item_text'])[1]"))).Text;
            //var venta = wait.Until(d => d.FindElement(By.XPath(
            //       "(//android.widget.TextView[@resource-id='com.tarjetanaranja.ncuenta:id/menu_item_text'])[2]"))).Text;

            //linea = fecha + "\t" + hora + ": \t" + compra;
            //File.AppendAllText(textDir, linea + Environment.NewLine);

            //linea = fecha + "\t" + hora + ": \t" + venta;
            //File.AppendAllText(textDir, linea + Environment.NewLine + Environment.NewLine);

            //Thread.Sleep(TimeSpan.FromSeconds(60));

            Thread.Sleep(1000);

            while (true)
            {
                //var localCompra = wait.Until(d => d.FindElement(By.XPath(
                //    "(//android.widget.TextView[@resource-id='com.tarjetanaranja.ncuenta:id/menu_item_text'])[1]"))).Text;
                //var localVenta = wait.Until(d => d.FindElement(By.XPath(
                //       "(//android.widget.TextView[@resource-id='com.tarjetanaranja.ncuenta:id/menu_item_text'])[2]"))).Text;

                var localCompra = driver.FindElement(By.XPath(
                    "(//android.widget.TextView[@resource-id='com.tarjetanaranja.ncuenta:id/menu_item_text'])[1]")).Text;
                var localVenta = driver.FindElement(By.XPath(
                       "(//android.widget.TextView[@resource-id='com.tarjetanaranja.ncuenta:id/menu_item_text'])[2]")).Text;

                //if (compra != localCompra || venta != localVenta)
                //{
                var fecha = DateTime.Now.ToString("dd/MM/yyyy");
                var hora = DateTime.Now.ToString("HH:mm");

                string[] compra = localCompra.Split("$");
                string[] venta = localVenta.Split("$");

                string linea = fecha + "," + hora + "," + compra[0].Trim() + "," + compra[1].Replace(",", ".") + "," + venta[0].Trim() + "," + venta[1].Replace(",", ".");

                File.AppendAllText(textDir, linea + Environment.NewLine);

                Thread.Sleep(TimeSpan.FromSeconds(15));
                localCompra = driver.FindElement(By.XPath(
                    "(//android.widget.TextView[@resource-id='com.tarjetanaranja.ncuenta:id/menu_item_text'])[1]")).Text;
                Thread.Sleep(TimeSpan.FromSeconds(15));
                localCompra = driver.FindElement(By.XPath(
                    "(//android.widget.TextView[@resource-id='com.tarjetanaranja.ncuenta:id/menu_item_text'])[1]")).Text;
                Thread.Sleep(TimeSpan.FromSeconds(15));
                localCompra = driver.FindElement(By.XPath(
                    "(//android.widget.TextView[@resource-id='com.tarjetanaranja.ncuenta:id/menu_item_text'])[1]")).Text;
                Thread.Sleep(TimeSpan.FromSeconds(15));
            }
        }

        [TearDown]
        public void TearDown()
        {
            driver.RemoveApp("com.tarjetanaranja.ncuenta");
            driver.Dispose();
        }

    }
}
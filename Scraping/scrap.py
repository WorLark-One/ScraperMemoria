from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.common.by import By
#from datatime import date
import time
import sys 

ubicacionD = "C:/Users/WorLark/PycharmProjects/Scraping/chromedriver.exe" 
driver = webdriver.Chrome(ubicacionD)
home_link = "https://comunidadc.cl"
search_link = '/vitrina/?_p=1&rows=&nombre=&idEmp=&catego=idReg%3B7&_o='
driver.get(home_link + search_link)

post = 'http://localhost:8000/api/public/postProducto'

#wait = WebDriverWait(driver, 10)
#original_window = driver.current_window_handle

page = BeautifulSoup(driver.page_source, 'html.parser')
#print(page)
pg_amount = 1

for i in range(0, pg_amount):
    contador = 0
    for bloque in page.findAll('div', attrs={'class': 'vab-prod-ficha-mini'}):
        tituloFinal = None
        precioFinal = None
        imagenFinal = None
        detallesFinal = None
        ubicacionFinal = None
        linkFinal = None
        marketPlaceFinal = "ComunidadC"
        #print(bloque);

        """href = bloque['href']
        #href = '/ecommerce/restServAdminAction.do?_accion=verProducto&idProducto=1589474926101695'
        idAux = href.split('Producto=')
        id = idAux[1]
        product_id.append(id)
        driver2 = webdriver.Chrome(ubicacion)
        driver2.get(home_link + href)
        page2 = BeautifulSoup(driver2.page_source, 'html.parser')"""
        titulo = bloque.find('strong').text
        if titulo:
            #product_title.append(titulo)
            tituloFinal = titulo
        else:
            titulo = 'No titulo'
            tituloFinal = titulo
            #product_title.append(titulo)
        precioAux = bloque.find('h2', attrs={'align': 'center'})
        precio = precioAux.find('strong').text
        if precio:
            aux = list(precio)
            precioString = ""
            flag = True
            for j in aux:
                if j != "$" and j != ".":
                    if flag:
                        precioString = j
                        flag = False
                    else:
                        precioString = precioString+j

            precioInt = int(precioString)
            precioFinal = precioInt
            #product_price.append(precio)
        else:
            precio = 0
            precioFinal = precio
            #product_price.append(precio)
        imagen = bloque.find('div', attrs={'class': 'vab-img-prod'})
        if imagen:
            imagenAux = imagen['style']
            imagenList = list(imagenAux)
            max = len(imagenList);
            flag = True
            imagenString = ""
            for j in range(0, max):
                fin = max - 3
                if j > 22 and j < fin:
                    if flag:
                        imagenString = imagenList[j]
                        flag = False
                    else:
                        imagenString = imagenString+imagenList[j]
            imagenFinal = imagenString
            #product_image.append(imagen['src'])
        else:
            imagen = 'No imagen'
            imagenFinal = imagen
            #product_image.append(imagen)
        detalles = bloque.find('p').text
        if detalles:
            # product_title.append(titulo))
            detallesFinal = detalles
        else:
            detalles = 'No detalles'
            detallesFinal = detalles
            # product_title.append(titulo)
        ubicacion = bloque.find('div', attrs={'class': 'vab-prod-det-region'}).text
        if ubicacion:
            # product_title.append(titulo)
            ubicacionAux = ubicacion.split("/")
            ubicacionLimpia = ubicacionAux[1].strip()
            ubicacionFinal = ubicacionLimpia
        else:
            ubicacion = 'No ubicacion'
            ubicacionFinal = ubicacion
            # product_title.append(titulo)
        link = bloque.find('a', attrs={'class': 'vab-prod-ficha-mini-boton vab-prod-ficha-mini-boton-ver-det'})
        if link:
            linkLimpio = link['href']
            linkFinal = linkLimpio
        else:
            link = 'No link'
            linkFinal = link
        data = {
            "titulo": tituloFinal,
            "descripcion": detallesFinal,
            "precio": precioFinal,
            "imagen": imagenFinal,
            "ubicacion": ubicacionFinal,
            "link": linkFinal,
            "marketplace": marketPlaceFinal
        }
        time.sleep(1)
        resp = requests.post(post, json=data)
        print(resp.json())
        """
        otros = page2.findAll('div', attrs={'class': 'card-body'})
        if otros:
            detalles3 = otros[0].text + otros[1].text
            detalles2 = detalles3.rstrip('\n')
            detalles1 = detalles2.split()
            detalles = " ".join(detalles1)
            #print(detalles)
            ubicacion2 = otros[2].find('span', attrs={'style': ' float: right;'}).text
            auxUbi = ubicacion2.split(',')
            ubicacionProduct3 = auxUbi[1]
            ubicacionProduct2 = ubicacionProduct3.rstrip('\n')
            ubicacionProduct1 = ubicacionProduct2.split()
            ubicacionProduct = " ".join(ubicacionProduct1)
            #print(ubicacionProduct)
            product_details.append(detalles)
            product_location.append(ubicacionProduct)
        else:
            detalles = 'No detalles'
            ubicacionProduct = 'No ubicación'
            product_details.append(detalles)
            product_location.append(ubicacionProduct)
        product_link.append(home_link + href)
        driver2.close()"""
    #next_btn = driver.find_element_by_id('bot-siguiente')
    #next_btn.click()
    #time.sleep(5)
    #element = driver.find_element_by_xpath("//a[@class='page-link' and @id='bot-siguiente']")
    #driver.execute_script("arguments[0].click();", element)
    #page = BeautifulSoup(driver.page_source, 'html.parser')
    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='page-link' and @id='bot-siguiente']"))).click()

driver.close()
"""product_list = pd.DataFrame({
    'ID': product_id,
    'Titulo': product_title,
    'Precio': product_price,
    'Imagen': product_image,
    'Detalles': product_details,
    'Ubicación': product_location,
    'Link': product_link
})"""
sys.exit()
#print(product_list)
#product_list.to_csv(r'lista_prueba.csv', index=False, header=True, encoding='utf-8-sig')

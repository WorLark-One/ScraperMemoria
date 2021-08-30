from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests

ubicacionD = "C:/Users/WorLark/PycharmProjects/Scraping/chromedriver.exe"  # Ruta del driver
driver = webdriver.Chrome(ubicacionD)
home_link = "https://www.mercadolibre.cl/"
seccion = "c/"
maule = "Maule/"
categorias = ['celulares-y-telefonia', 'computacion', 'electronica-audio-y-video', 'consolas-y-videojuegos', 'accesorios-para-vehiculos', 'electrodomesticos', 'hogar-y-muebles', 'belleza-y-cuidado-personal', 'vestuario-y-calzado', 'deportes-y-fitness', 'herramientas', 'construccion', 'salud-y-equipamiento-medico', 'industrias-y-oficinas', 'agro', 'alimentos-y-bebidas', 'animales-y-mascotas', 'arte-libreria-y-cordoneria', 'antiguedades-y-colecciones', 'bebes', 'camaras-y-accesorios']
search_link = ['celulares-y-telefonia']
marketPlaceFinal = "MercadoLibre"
post = 'http://localhost:8000/api/public/postProducto'
driver2 = webdriver.Chrome(ubicacionD)
driver3 = webdriver.Chrome(ubicacionD)
for cat in categorias:
    driver.get(home_link + seccion + cat)
    page = BeautifulSoup(driver.page_source, 'html.parser')
    for subcat in page.findAll('div', attrs={'class': 'desktop__view-child'}):
        linkSubCat = subcat.find('a', attrs={'target': '_self'})
        linkSubCatSplit = linkSubCat['href'].split('#')
        auxLinkSubCat = linkSubCatSplit[0]+maule
        #print(auxLinkSubCat)
        driver2.get(auxLinkSubCat)
        page2 = BeautifulSoup(driver2.page_source, 'html.parser')
        productos = page2.findAll('a', attrs={'class': 'ui-search-item__group__element ui-search-link'})
        if productos:
            for p in productos:
                tituloFinal = None
                descripcionFinal = None
                precioFinal = None
                imagenFinal = None
                ubicacionFinal = None
                linkFinal = None
                linkProducto = p['href']
                driver3.get(linkProducto)
                page3 = BeautifulSoup(driver3.page_source, 'html.parser')
                verificarU = page3.find('p', attrs={'class': 'ui-seller-info__status-info__title'})
                verificarL = driver3.current_url.split('JM#')
                verificarL2 = driver3.current_url.split('JM?')
                if verificarU:
                    if verificarU.text == "Ubicación" and (len(verificarL) > 1 or len(verificarL2) > 1):
                        titulo = page3.find('h1', attrs={'class': 'ui-pdp-title'})
                        if titulo:
                            tituloFinal = titulo.text
                        else:
                            titulo = 'No titulo'
                            tituloFinal = titulo
                        descripcion = page3.find('p', attrs={'class': 'ui-pdp-description__content'})
                        if descripcion:
                            descripcionAux = ''
                            for d in descripcion.contents:
                                descripcionAux = descripcionAux+str(d)
                            descripcionFinal = descripcionAux
                        else:
                            descripcion = 'No descripcion'
                            descripcionFinal = descripcion
                        precio = page3.find('meta', attrs={'itemprop': 'price'})
                        if precio:
                            precioAux = precio['content'].strip('.')
                            precioFinal = int(precioAux)
                        else:
                            precio = 0
                            precioFinal = precio
                        imagen = page3.find('img', attrs={'class': 'ui-pdp-image ui-pdp-gallery__figure__image'})
                        if imagen:
                            imagenFinal = imagen['src']
                        else:
                            imagen = 'No imagen'
                            imagenFinal = imagen
                        ubicacion = page3.find('p', attrs={'class': 'ui-seller-info__status-info__subtitle'})
                        if ubicacion:
                            ubicacionAux = ubicacion.text.split(",")
                            ubicacionLimpia = ubicacionAux[0]
                            ubicacionFinal = ubicacionLimpia
                        else:
                            ubicacion = 'No ubicacion'
                            ubicacionFinal = ubicacion
                        link = driver3.current_url
                        if link:
                            linkAux1 = link.split('JM#')
                            linkAux2 = link.split('JM?')
                            if len(linkAux1) > 1:
                                linkFinal = linkAux1[0]+"JM"
                            else:
                                if len(linkAux2) > 1:
                                    linkFinal = linkAux2[0]+"JM"
                        else:
                            link = 'No link'
                            linkFinal = link
                        data = {
                            "titulo": tituloFinal,
                            "descripcion": descripcionFinal,
                            "precio": precioFinal,
                            "imagen": imagenFinal,
                            "ubicacion": ubicacionFinal,
                            "link": linkFinal,
                            "marketplace": marketPlaceFinal
                        }
                        #print(data)
                        time.sleep(1)
                        resp = requests.post(post, json=data)
                        print(resp.json())

                time.sleep(1)
        else:
            print("no productos")
        time.sleep(1)
    time.sleep(1)
driver3.close()
driver2.close()
driver.close()

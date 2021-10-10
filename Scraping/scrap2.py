from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
import time

ubicacionD = "D:/NewEscritorio/memoria/ScraperMemoria/Scraping/chromedriver.exe"  # Ruta del driver
driver = webdriver.Chrome(ubicacionD)
home_link = "https://www.marketmaule.cl/"
home_link2 = "https://www.marketmaule.cl"
marketPlaceFinal = "marketmaule"
search_link = 'alimentos-y-bebidas'
categorias = ['agro', 'alimentos-y-bebidas', 'celulares-y-telefonia', 'computacion', 'electronica-audio-y-video', 'camaras-y-accesorios', 'electrodomesticos', 'artesania', 'autos-motos-y-otros', 'consolas-y-videojuegos', 'juegos-y-juguetes', 'libros-revistas-y-comics', 'hogar-y-muebles', 'herramientas-y-construccion', 'animales-y-mascotas', 'belleza-y-cuidado-personal', 'deportes-y-fitness', 'vestuario-y-calzado', 'relojes-y-joyas', 'arte-libreria-y-cordoneria', 'antiguedades-y-colecciones', 'bebes', 'bebidas/vinos-y-espumantes', 'bebidas/bebidas-blancas-y-licores', 'bebidas/cervezas']
post = 'http://localhost:8000/api/public/postProducto'
inicio = time.time()
for cat in categorias:
    driver.get(home_link + cat)
    """previous_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            break
        previous_height = new_height
    time.sleep(1)"""
    page = BeautifulSoup(driver.page_source, 'html.parser')
    page1 = page.find('div', attrs={'data-react-class': 'views/products/ProductsIndex'})
    obj = page1['data-react-props']
    jsonFormated = json.loads(obj)
    for p in jsonFormated["products"]:
        titulo = p["name"]
        if titulo:
            titulo1 = " ".join(titulo.split())
            tituloFinal = titulo1
        else:
            titulo = 'No titulo'
            tituloFinal = titulo
        descripcion = p["large_description"]

        if descripcion:
            descripcion2 = " ".join(descripcion.split())
            descripcionFinal = descripcion2
        else:
            descripcion = 'No descripcion'
            descripcionFinal = descripcion
        precio = p["price"]
        if precio:
            descuento = p["active_discount"]
            if descuento:
              precio = p["discount_price"]
            precioFinal = precio
        else:
            precio = 0
            precioFinal = precio
        imagen = p["avatar_url"]
        if imagen:
            imagenFinal = home_link2+imagen
        else:
            imagen = 'No imagen'
            imagenFinal = imagen
        ubicacion = p["store"]["district"]["name"]
        if ubicacion:
            ubicacionFinal = ubicacion
        else:
            ubicacion = 'No ubicacion'
            ubicacionFinal = ubicacion
        link = p["slug"]
        if link:
            linkFinal = home_link+"products/"+link
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
        #print(data);
        time.sleep(0.5)
        resp = requests.post(post, json=data)
        print(resp.json())
driver.close()
fin = time.time()
print((fin-inicio)/60)

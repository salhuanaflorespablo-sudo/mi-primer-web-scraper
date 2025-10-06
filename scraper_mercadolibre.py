import requests
from bs4 import BeautifulSoup
import pandas as pd

# Función principal
def scrape_mercadolibre(producto):
    # URL de búsqueda en Mercado Libre Perú (ej: celulares)
    url = f"https://listado.mercadolibre.com.pe/{producto}"
    
    # Descargar la página
    headers = {'User-Agent': 'Mozilla/5.0'}  # Para que no te bloqueen
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Buscar productos
    productos = []
    items = soup.find_all('div', {'class': 'ui-search-result__content'})
    
    for item in items[:10]:  # Solo los primeros 10 para que sea rápido
        try:
            nombre = item.find('h2').text.strip()
            precio = item.find('span', {'class': 'andes-money-amount__fraction'}).text
            link = item.find('a')['href']
            
            productos.append({
                'Nombre': nombre,
                'Precio': precio,
                'Link': link
            })
        except:
            pass  # Ignora errores
    
    # Guardar en un Excel
    df = pd.DataFrame(productos)
    df.to_excel(f'{producto}_precios.xlsx', index=False)
    print(f"¡Listo! {len(productos)} productos guardados en {producto}_precios.xlsx")

# Usar el scraper
scrape_mercadolibre('celulares')  # Cambia por lo que quieras: 'zapatillas', 'laptops', etc.
import requests
from bs4 import BeautifulSoup

def get_chapter_links(url):
    # Realizar la solicitud GET a la página
    response = requests.get(url)

    # Verificar que la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar la tabla wiki con la clase 'wikitable'
        table = soup.find('table', {'class': 'wikitable'})

        # Verificar si se encontró la tabla
        if table:
            # Inicializar la lista de enlaces
            chapter_links = []

            # Iterar sobre las filas de la tabla
            for row in table.find_all('tr')[1:]:
                # Obtener las celdas de la fila
                cells = row.find_all(['td', 'th'])

                # Obtener el enlace si la celda es un td y contiene un enlace
                if len(cells) == 3 and cells[1].find('a'):
                    link = cells[1].find('a')
                    href = link.get('href')
                    full_url = f"https://wiki.itcsoluciones.com{href}"
                    chapter_links.append(full_url)

            return chapter_links

        else:
            print("No se encontró la tabla 'wikitable'.")
            return None
    else:
        print(f"Error al realizar la solicitud. Código de estado: {response.status_code}")
        return None

# Ejemplo de uso
url = "https://wiki.itcsoluciones.com/index.php/CIE-10"
links = get_chapter_links(url)
print(links)

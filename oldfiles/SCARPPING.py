
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


URL = "https://wiki.itcsoluciones.com/index.php/CIE-10"

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

            if len(chapter_links) == 0:
                print("No se encontraron enlaces.")
            else:
                chapter_links.pop()

            return chapter_links

        else:
            print("No se encontró la tabla 'wikitable'.")
            return None
    else:
        print(f"Error al realizar la solicitud. Código de estado: {response.status_code}")
        return None


def scrape_data(url):
    # Realizar la solicitud GET a la página
    response = requests.get(url)

    # Verificar que la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar el elemento con id 'mw-content-text'
        mw_content_text = soup.find('div', {'id': 'mw-content-text'})

        # Verificar si se encontró el elemento
        if mw_content_text:
            # Buscar la etiqueta 'pre' dentro del elemento
            pre_tag = mw_content_text.find('pre')

            # Verificar si se encontró la etiqueta 'pre'
            if pre_tag:
                # Obtener el texto dentro de 'pre'
                codes_text = pre_tag.text.strip()

                # Imprimir el texto
                lines = codes_text.strip().split('\n')
                data = [re.split(r'\s+', line, maxsplit=1) for line in lines]

                # Crear un DataFrame
                df = pd.DataFrame(data, columns=['code', 'name'])
                print('dataframe de link:', url, '\n\n', df.head())
                return df
                # Imprimir el DataFrame
               # print(df)
            else:
                print("No se encontró la etiqueta 'pre' dentro del elemento 'mw-content-text'.")
        else:
            print("No se encontró el elemento 'mw-content-text'.")
    else:
        print(f"Error al realizar la solicitud. Código de estado: {response.status_code}")

def get_super_dataframe(links):
    # Inicializar una lista para almacenar los DataFrames
    dataframes = []

    # Iterar sobre los enlaces y aplicar scrape_data
    for link in links:
        df = scrape_data(link)
        if df is not None:
            dataframes.append(df)

    # Verificar si hay DataFrames para concatenar
    if len(dataframes) == 0:
        print("No hay DataFrames para concatenar. Descartando y continuando...")
        return None

    # Concatenar los DataFrames en uno solo
    super_dataframe = pd.concat(dataframes, ignore_index=True)

    return super_dataframe



links = get_chapter_links(URL)

# Call the function with the updated links list
super_dataframe = get_super_dataframe(links)

# Export the dataframe to an Excel file named "cie_data.xlsx"
super_dataframe.to_excel("cie_data.xlsx", index=False)
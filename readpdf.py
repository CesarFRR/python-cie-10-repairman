import PyPDF2
import pandas as pd
import re
from ast import literal_eval
# Abrir el archivo PDF
pdf_file = open('./muertes.pdf', 'rb')

pdf_reader = PyPDF2.PdfReader(pdf_file)

num_pages = len(pdf_reader.pages)

page_text = []

for page in range(num_pages):
    page_obj = pdf_reader.pages[page]
    text = page_obj.extract_text()
    page_text.append(text)
#print(page_text[3])


# Inicializar un DataFrame vacío para almacenar los datos extraídos
data = pd.DataFrame(columns=['id', 'name', 'code'])

# Definir el patrón de las líneas que queremos extraer
pattern = r"(\S+)  (.*?)   (.*)"

# Para cada página en el texto del PDF
data_list = []

for page in page_text:
    # Encontrar todas las coincidencias del patrón en la página
    matches = re.findall(pattern, page)
    
    # Para cada coincidencia, extraer el ID, el nombre y los códigos
    for match in matches:
        id = match[0]
        name = match[1]
        codes = match[2].split('  ')  # Dividir los códigos en una lista
        
        # Añadir los datos extraídos a la lista
        data_list.append({'id': id, 'name': name, 'code': codes})




# Concatenar los datos de la lista en un DataFrame
data = pd.concat([data, pd.DataFrame(data_list)], ignore_index=True)
df = data
df.to_excel('muertesv0.xlsx')
def clean_dataframe(file_path):
    # Leer el archivo Excel en un DataFrame
    df = pd.read_excel(file_path)

    # Eliminar los espacios en blanco al principio y al final de cada valor en la columna 'name'
    df['name'] = df['name'].apply(lambda name: name.strip())
    # Eliminar los números al principio de cada valor en la columna 'name'
    df['name'] = df['name'].apply(lambda name: re.sub(r'^\d+\s*', '', name.strip()))

    # Convertir la columna 'code' a listas
    df['code'] = df['code'].apply(literal_eval)

    # Filtrar los elementos de la lista en la columna 'code'
    df['code'] = df['code'].apply(lambda codes: [code for code in codes if 'excepto' not in code and code.strip() != '' and code.count('.') <= 1])

    # Eliminar las filas que contienen 'resto' en la columna 'code'
    df = df[~df['code'].apply(lambda codes: any('resto' in code.lower() for code in codes))]

    # Eliminar las filas donde la lista en la columna 'code' está vacía
    df = df[df['code'].apply(lambda codes: len(codes) > 0)]
    df['code'] = df['code'].apply(lambda codes: [re.sub(r'\s-\s', '-', code) for code in codes])
    df.to_excel('muertesfixeddeuna3.xlsx')
    return df

excel_nuevo = clean_dataframe('muertesv0.xlsx')
import pandas as pd
from ast import literal_eval
import re
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
    df.to_excel('muertes17.xlsx')
    return df
    


excel_nuevo = clean_dataframe('muertes2.xlsx')


import pandas as pd
from fuzzywuzzy import process

def agregar_columna_code_corregida(df_a, df_b):
    # Añadir columnas 'name_fixed' y 'code' a A
    df_a['name_fixed'] = ''
    df_a['code'] = ''
    # Crear una lista de opciones para la búsqueda
    opciones_b = df_b['name'].tolist()

    # Iterar sobre las filas de A
    for index_a, row_a in df_a.iterrows():
        # Obtener el nombre de la fila actual en A
        name_a = row_a['name']

        # Encontrar la mejor correspondencia en B
        mejor_correspondencia, _ = process.extractOne(name_a, opciones_b)

        # Si la correspondencia es suficientemente buena, copiar el 'code' de B a A
        if process.extractOne(name_a, [mejor_correspondencia])[1] > 80:  # Puedes ajustar el umbral según sea necesario
            df_a.at[index_a, 'name_fixed'] = mejor_correspondencia
            df_a.at[index_a, 'code'] = df_b[df_b['name'] == mejor_correspondencia]['code'].values[0]
        else:
            df_a.at[index_a, 'name_fixed'] = name_a
    return df_a

# Ejemplo de uso
df_a = pd.DataFrame({'name': ['HIPOXIA FETAKL', 'Alice', 'Bob']})
df_b = pd.DataFrame({'name': ['HIPOXIA FETAL', 'Bob', 'Eve'], 'code': [101, 102, 103]})

df_a_actualizado = agregar_columna_code_corregida(df_a, df_b)

# Imprimir el resultado
print(df_a_actualizado)




# def encontrar_mejor_correspondencia(texto_a, opciones_b):
#     # Función para encontrar la mejor correspondencia entre un texto y una lista de opciones
#     mejor_correspondencia, _ = process.extractOne(texto_a, opciones_b)
#     return mejor_correspondencia
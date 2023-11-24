from fuzzywuzzy import fuzz
from collections import defaultdict
import threading
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from tqdm import tqdm
class Repairman:
    def __init__(self, df_a, df_b, df_d=None):
        self.df_a = df_a
        self.df_b = df_b
        self.df_d = df_d
        if self.df_d is None:
            self.df_d = pd.read_excel('./deaths_cie_10.xlsx')
        self.hashing_words={}
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))

        self.classifier = LinearSVC()
    def agregar_columna_code_corregida(self):
        print(f"\Corrigiendo un poco el dataframe A...\n")
        self.prepare_df_a()
        # print(f"\nGenerando mapa de hasing para corrección de palabras...\n")
        # self.create_hash_map()
        # print(f"\nMapa de hasing generado con exito\n")
        print(f"\nIniciando reparacion\n")
        # Añadir columnas 'name_fixed' y 'code' a A
        self.df_a['name_fixed'] = ''
        self.df_a['code'] = ''
         # # Obtener la longitud de df_a
        df_a_length = len(self.df_a)
        # Iterar sobre las filas de A
        new_df_a=self.predict_codes(df_a=self.df_a)
        self.df_a=new_df_a
        print(f"\nReparación completada! puede exportar el archivo a excel\n")
        # for index_a, row_a in self.df_a.iterrows():
        #     # Obtener el nombre de la fila actual en A
        #     name_a = row_a['name']

        #     # Tomar la primera palabra del nombre
        #     first_word = name_a.split()[0]

        #     # Filtrar df_b para que solo contenga filas cuyos nombres comienzan con first_word
        #     df_b_filtered = self.df_b[self.df_b['name'].str.startswith(first_word)]

        #     # Crear una lista de opciones para la búsqueda
        #     opciones_b = df_b_filtered['name'].tolist()

        #     # Encontrar la mejor correspondencia en B
        #     mejor_correspondencia = max(opciones_b, key=lambda x: fuzz.ratio(name_a, x)) if opciones_b else ''

        #     # Si la correspondencia es suficientemente buena, copiar el 'code' de B a A
        #     if mejor_correspondencia and fuzz.ratio(name_a, mejor_correspondencia) > 60:  # Puedes ajustar el umbral según sea necesario
        #         self.df_a.at[index_a, 'name_fixed'] = mejor_correspondencia
        #         self.df_a.at[index_a, 'code'] = df_b_filtered[df_b_filtered['name'] == mejor_correspondencia]['code'].values[0]
        #     else:
        #         self.df_a.at[index_a, 'name_fixed'] = name_a
        #         self.df_a.at[index_a, 'code'] = 'No encontrado'
        #     #Imprimir el progreso
        #     print(f"reparando {index_a+1}/{df_a_length} registros | {((index_a+1)/df_a_length)*100:.1f}%")
        return self.df_a
    def train(self):
        # Convertir todos los valores de 'name' a mayúsculas y sin tildes
        self.df_a['name'] = self.df_a['name'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        self.df_b['name'] = self.df_b['name'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

        # Entrenar el vectorizador con las formas de decir las enfermedades en df_b
        print(f"\nEntrenando el vectorizador...\n")
        print('datos: ', 'len de df_a: ', len(self.df_a['name']), 'len de df_b: ', len(self.df_b['name']))
        X_train = self.vectorizer.fit_transform(self.df_b['name'])
        print(f"\nEntrenamiento completo\nAhora puede reparar el archivo de excel en poco tiempo\n")

        # Entrenar el clasificador con los vectores de las formas de decir las enfermedades y sus correspondientes códigos
        y_train = self.df_b['code']
        self.classifier.fit(X_train, y_train)
    def prepare_df_a(self):
        change = {'HIPERTENSION ARTERIAL': 'ENFERMEDAD CARDIOVASCULAR'}
        
        # Aplicar el cambio en la columna 'name'
        self.df_a['name'] = self.df_a['name'].replace(change, regex=True)

    def predict_codes(self, df_a):
        # Para cada forma de decir una enfermedad en df_a, predecir su código
        X_test = self.vectorizer.transform(df_a['name'])
        df_a['code'] = self.classifier.predict(X_test)

        # Crear un mapeo inverso de los códigos a los nombres en df_b
        code_to_name = self.df_b.set_index('code')['name'].to_dict()

        # Asignar el nombre correspondiente a la columna 'name_fixed' en df_a
        df_a['name_fixed'] = df_a['code'].map(code_to_name)

        # Si no se predice nada, establecer 'name_fixed' igual a 'name' y 'code' igual a 'No encontrado'
        df_a.loc[df_a['code'].isna(), 'name_fixed'] = df_a.loc[df_a['code'].isna(), 'name']
        df_a.loc[df_a['code'].isna(), 'code'] = 'No encontrado'

        return df_a
    def Docreate_hash_map(self):
        load_thread = threading.Thread(target=self.create_hash_map)
        # Iniciar el hilo
        load_thread.start()
    
    def create_hash_map(self):
        # Crear un diccionario para almacenar las palabras y sus frecuencias
        word_freq = defaultdict(list)  # Cambiar 'int' por 'list'
        lista = self.df_a['name'].tolist() #+ self.df_b['name'].tolist()
        total_l= len(lista)
        print('Total de registros: ', total_l)
        # Iterar sobre las palabras en df_a y df_b

        for name in lista:
            print(f"Procesando {len(word_freq)}/{total_l} registros | {((len(word_freq))/total_l)*100:.1f}%")
            # Dividir el nombre en palabras
            for word in name.split():
                # Calcular el valor hash de la palabra
                word_hash = hash(word)

                # Agregar la palabra al diccionario
                word_freq[word_hash].append(word)

        # Para cada conjunto de palabras que tengan el mismo valor hash
        for word_hash, words in word_freq.items():
            # Encontrar la palabra que se repite más veces
            most_common_word = max(words, key=words.count)

            # Guardar la palabra más común en self.hashing_words
            self.hashing_words[word_hash] = most_common_word
        print('Hashing completado')

    def repair_name(self, name):
        # Dividir el nombre en palabras
        words = name.split()

        # Para cada palabra en el nombre
        for i in range(len(words)):
            # Calcular el valor hash de la palabra
            word_hash = hash(words[i])

            # Si el valor hash está en self.hashing_words
            if word_hash in self.hashing_words:
                # Reemplazar la palabra por la palabra más común
                words[i] = self.hashing_words[word_hash]

        # Unir las palabras corregidas en un nombre y devolverlo
        return ' '.join(words)

# # Ejemplo de uso
# df_a = pd.DataFrame({'name': ['HIPOXIA FETAKL', 'Alice', 'Bob']})
# df_b = pd.DataFrame({'name': ['HIPOXIA FETAL', 'Bob', 'Eve'], 'code': [101, 102, 103]})

# reparador = Reparador(df_a, df_b)
# df_a_actualizado = reparador.agregar_columna_code_corregida()

# # Imprimir el resultado
# print(df_a_actualizado)

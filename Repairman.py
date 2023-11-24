from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

class Repairman:
    def __init__(self, df_a, df_b):
        self.df_a = df_a
        self.df_b = df_b
        self.hashing_words={}
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))

        self.classifier = LinearSVC()
    def agregar_columna_code_corregida(self):
        print(f"\Corrigiendo un poco el dataframe A...\n")
        self.prepare_df_a()
        print(f"\nIniciando reparacion\n")
        self.df_a['name_fixed'] = ''
        self.df_a['code'] = ''
        df_a_length = len(self.df_a)

        new_df_a=self.predict_codes(df_a=self.df_a)

        self.df_a=new_df_a
        self.revert_prepare_df_a()
        print(f"\nReparación completada! puede exportar el archivo a excel\n")
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
    def revert_prepare_df_a(self):
        change = {'ENFERMEDAD CARDIOVASCULAR': 'HIPERTENSION ARTERIAL'}
        
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

import pandas as pd
from CIE_10_Loader import CIE_10_Loader

class CIE_APP:
    def __init__(self):
        self.loader = CIE_10_Loader()
        self.links = None

    def load_cie_10_data(self):
        links = self.loader.get_chapter_links()
        return self.scrape_data(links)

    def scrape_data(self, links):
        self.links = links
        # Inicializar una lista para almacenar los DataFrames
        dataframes = []

        # Iterar sobre los enlaces y aplicar scrape_data
        for index, link in enumerate(self.links):
            df = self.loader.scrape_data(url=link)

            if df is not None:
                dataframes.append(df)
                print('\n\nCategoria N°: ',index+1, '\nEnlace: ',link, '\nDatos:\n', df.head(n=3).to_string(index=False))
        # Verificar si hay DataFrames para concatenar
        if len(dataframes) == 0:
            print("No hay DataFrames para concatenar. Descartando y continuando...")
            return None

        # Concatenar los DataFrames en uno solo
        super_dataframe = pd.concat(dataframes, ignore_index=True)

        return super_dataframe

    def export_to_excel(self, filename):
        # Call the function to scrape data
        super_dataframe = self.scrape_data()

        if super_dataframe is not None:
            # Export the dataframe to an Excel file with the given filename
            super_dataframe.to_excel(filename, index=False)
            print(f"Data exported to {filename} successfully.")

# # Create an instance of CIE_APP with the updated links list
# loader = CIE_10_Loader()
# links = loader.get_chapter_links()
# cie_app = CIE_APP(links)

# # Call the export_to_excel method with the desired filename
# cie_app.export_to_excel("cie_data.xlsx")

import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys
import csv
import plotly
import plotly.express as px
import pycountry

class covid19Scraper():

    def __init__(self):
        self.url ="https://www.worldometers.info"
        self.subdomain="/coronavirus/"
        # Paises cargados a partir de los argumentos 
        self.country_list =[]

    def __loaddata(self):
        page = requests.get(self.url+self.subdomain)
        self.soup = BeautifulSoup(page.content,'html.parser')

    def __get_data_columns(self):
        self.soup.find_all('tr')[0].get_text().split('\n')

        self.soup.find_all('tr')[0].get_text()
        self.columnas = self.soup.find_all('tr')[0].get_text().split('\n')

        # Elimina el primer y ultimo elemento
        self.columnas.pop(0)
        self.columnas.pop(-1)
        self.columnas.pop(-2)
        self.columnas.pop(-2)

        self.columnas[0] = 'Country/Other'
        self.columnas[8] = 'Tot Cases/1M pop' 
        self.columnas[11] = "Tests/1M pop"
    
    def __load_country_list(self):
        for i in range(len(sys.argv)):
            if i>0:
                self.country_list.append(sys.argv[i])

    
    def __get_countries(self):
        
        i=0
        paises = []
        for pais in self.soup.find_all('tr'):
            total = self.soup.find_all('tr')[i].get_text().split('\n')
            
            paises.append(total[1])
            i+=1

            self.paises_clean = list(set(paises))
        
        if len(self.country_list) != 0:
            self.paises_clean=self.country_list


    def __get_country_data(self):
        
        self.lista_info = []
        i,j,k = 0,0,0
        for num in range(9,len(self.paises_clean)+9):
            #    print(num)
            info = self.soup.find_all('tr')[num].get_text().split('\n')

            info.pop(0)
            info.pop(-1)
        
            self.lista_info.append(info)

        # Tomamos todos los primeros elementos de las listas y lo guardamos 
        # en una lista - paises y lo mismo con el ultimo elemento y lo guardamos 
        # como continent
        self.lista_paises = [lista[0] for lista in self.lista_info] 
        self.lista_continentes = [lista[-1] for lista in self.lista_info] 

        # lista_info -- La recorremos y quitamos la posicion de los paises y los 
        # continentes, dejammos unicamente valores numericos
        for lista in self.lista_info:
            lista.pop(0)
            lista.pop(-1)
                
    def __clean_data(self):
        # 3. Limpieza de datos
        # 3.1 Elimina los espacios en blanco y sustituye por 0
        for lista in self.lista_info:
            i=0
            #print(lista)
            for elem in lista:
                if elem == '':
                    lista[i] = "0"
                
                if elem == ' ':
                    lista[i] = "0"
                
                if elem == 'N/A': 
                    lista[i] = "0"    
                i+= 1
        # 3.2 Elimina el simbolo + de los numeros
        for lista in self.lista_info:
            j,k=0,0
            for elem in lista:

                if elem[0] == '+': #si el elemento comienza con +
                    lista[j]= elem.replace('+','')
                
                lista[k]=float(elem.replace(',','')) # Quita la coma para indicar mil
                #lista_test.append(lista[k])
                j+=1
                k+=1

        # Convierte las cadenas en float
        for lista in self.lista_info:
            j=0
            for elem in lista:
                if (lista.index(elem))==0:
                    continue
                if (lista.index(elem)+1)==len(lista):
                    continue
                float(elem)
                
        # Como separamos las listas de continente y pais modificamos columnas
        self.columnas_def = self.columnas[1:-1]


        print("Comprobando longitud de listas.....\n")
        print('Longitud lista paises: ',len(self.paises_clean))
        print('longitud lista informacion: ',len(self.lista_info))
        print("\nComprobando numero de columnas....\n")
        print('Longitud lista columnas: ',len(self.columnas_def))
        print('Lontigud sublistas info: ',len(self.lista_info[0]))


    def __build_dataframe(self):
        # 4. DataFrame        
        
        dframe=pd.DataFrame(self.lista_info,columns=self.columnas_def)

        dframe[self.columnas[0]] = self.lista_paises
        dframe[self.columnas[-1]] = self.lista_continentes

        self.covid19_data = dframe[self.columnas] # Cambia Country/Other a la posicion 1


    def save_to_csv(self):
        # 5. Anadimos a nuestro DataFrame la fecha de la ultima actualizacion y lo 
        # guardamos en la ubicación deseada con el nombre deseado
        # obtenemos el path desde la pagina web
        fecha_path = self.soup.find('div',
        {'style':'font-size:13px; color:#999; margin-top:5px; text-align:center'})

        print('\n\nLa fecha se encuentra en la siguiente linea: \n',fecha_path)

        fecha = fecha_path.text[14:-4].split(',')

        hora = int(fecha[2].split(' ')[1].split(':')[0])
        minutos = int(fecha[2].split(' ')[1].split(':')[1])
        anyo = int(fecha[1].split(' ')[1])
        dia = int(fecha[0].split(' ')[1])
        mes = fecha[0].split(' ')[0]

        # 5.2 Guardar DataFrame en csv
        # Creamos un nombre de archivo lo haremos de la siguiente forma
        # Corona_10-03-2020_T1550

        nombre = 'Corona_{}-{}-{}_T{}{}'.format(dia,mes,anyo,hora,minutos)

        # Guarda el DataFrame actual en la carpeta deseada con el nombre en formato 
        # Corona_dd-mm-aaaa_Thhmm
        self.covid19_data.to_csv(r'{}.csv'.format(nombre), index = False)
        print('\n\nArchivo guardado como {}.csv'.format(nombre))

    # def export_to_csv(self, filename):
    #     # Overwrite to the specified file.
	# 	# Create it if it does not exist.
    #     file = open("/csv/" + filename, "w+")

	# 	# Dump all the data with CSV format
    #     for i in range(len(self.covid19_data)):
    #         for j in range(len(self.covid19_data[i])):
    #             file.write(self.covid19_data[i][j] + ";")
    #         file.write("\n")

    def __get_alph_3(self,location):
        try:
            return pycountry.countries.get(name=location).alpha_3
        except:
            return None



    def __visualize_data (self):


        # from list(pycountry.countries)
        self.covid19_data['Country/Other'][0] = 'United States'
        self.covid19_data['Country/Other'][5] = 'United Kingdom'
        self.covid19_data['Country/Other'][6] = 'Iran, Islamic Republic of'
        self.covid19_data['Country/Other'][13] = 'Russian Federation'
        self.covid19_data['Country/Other'][18] = 'Korea, Republic of'
        self.covid19_data['Country/Other'][37] = 'United Arab Emirates'
        self.covid19_data['Country/Other'][56] = 'Moldova, Republic of'
        self.covid19_data['Country/Other'][87] = 'Côte d\'Ivoire'
        self.covid19_data['Country/Other'][96] = 'Taiwan, Province of China'
        self.covid19_data['Country/Other'][101] = 'Bolivia, Plurinational State of'
        self.covid19_data['Country/Other'][105] = 'Palestine, State of'
        self.covid19_data['Country/Other'][108] = 'Viet Nam'
        self.covid19_data['Country/Other'][110] = 'Congo, The Democratic Republic of the'
        self.covid19_data['Country/Other'][116] = 'Faroe Islands'
        self.covid19_data['Country/Other'][117] = 'Venezuela, Bolivarian Republic of'
        self.covid19_data['Country/Other'][123] = 'Brunei Darussalam'
        self.covid19_data['Country/Other'][147] = 'Tanzania, United Republic of'
        self.covid19_data['Country/Other'][156] = 'Saint Martin (French part)'
        self.covid19_data['Country/Other'][158] = 'Syrian Arab Republic'
        self.covid19_data['Country/Other'][183] = 'Saint Vincent and the Grenadines'
        self.covid19_data['Country/Other'][184] = 'Central African Republic'
        self.covid19_data['Country/Other'][194] = 'Turks and Caicos Islands'
        self.covid19_data['Country/Other'][195] = 'Holy See (Vatican City State)'
        self.covid19_data['Country/Other'][197] = 'Saint Barthélemy'
        self.covid19_data['Country/Other'][201] = 'Falkland Islands (Malvinas)'
        self.covid19_data['Country/Other'][206] = 'Virgin Islands, British'
        self.covid19_data['Country/Other'][209] = 'Saint Pierre and Miquelon'

        # Anadimos el codigo alph al data frame
        self.covid19_data['Code'] = self.covid19_data['Country/Other'].apply(lambda x: self.__get_alph_3(x))

        # columnas nuevo orden
        col_new = [self.covid19_data.columns[-1]]+[self.covid19_data.columns[0]]+[self.covid19_data.columns[-2]]+list(self.covid19_data.columns[1:-2])

        df_def=self.covid19_data[col_new]

        # Confirmed
        fig_c = px.choropleth(df_def, locations='Country/Other', locationmode='country names', 
                            color="TotalCases", hover_name="Country/Other", hover_data=['TotalCases'],
                            color_continuous_scale=px.colors.sequential.Plasma)
        fig_c.update_layout(
            title_text = 'Casos Totales Coronavirus')
        fig_c.show()
        # Deaths

        fig_d = px.choropleth(df_def, locations='Country/Other', locationmode='country names',
                            color="TotalDeaths", hover_name="Country/Other", hover_data=['TotalDeaths'],
                            color_continuous_scale=px.colors.sequential.Plasma)

        fig_d.update_layout(
            title_text = 'Muertes Totales Coronavirus')
        fig_d.show()

    
    
    def scraper (self):
        # Cargamos los datos de la web
        self.__loaddata()

        # Cargamos las columnas de datos
        self.__get_data_columns()

        #Cargamos los paises pasados por parametros 
        self.__load_country_list()

        #Cargamos los paises
        self.__get_countries()

        #Cargamos los datos de cada pais
        self.__get_country_data()

        # Formateamos los datos
        self.__clean_data()

        # Creamos nuestro dataset
        self.__build_dataframe()

        # Guardamos el resultado en csv
        self.save_to_csv()

        # visualizamos los datos
        self.__visualize_data()

        # Exportamos el resultado a csv
        # self.export_to_csv("covid_by_country.csv")
        
        
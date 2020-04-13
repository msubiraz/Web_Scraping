import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys

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

    def __get_countries(self):
        
        i=0
        paises = []
        for pais in self.soup.find_all('tr'):
            total = self.soup.find_all('tr')[i].get_text().split('\n')
            
            paises.append(total[1])
            i+=1

            self.paises_clean = list(set(paises))

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


    def build_dataframe(self):
        # 4. DataFrame
        self.df=pd.DataFrame(self.lista_info,columns=self.columnas_def)

        self.df[self.columnas[0]] = self.lista_paises
        self.df[self.columnas[-1]] = self.lista_continentes

        self.df = self.df[self.columnas] # Cambia Country,Other a la posicion 1


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
        self.df.to_csv(r'{}.csv'.format(nombre), index = False)
        print('\n\nArchivo guardado como {}.csv'.format(nombre))


    

    def __load_country_list(self):
        for i in range(len(sys.argv)):
            if i>0:
                self.country_list.append(sys.argv[i])
    
    def scraper (self):
        # Cargamos los datos de la web
        self.__loaddata()

        # Cargamos las columnas de datos
        self.__get_data_columns()

        #Cargamos los paises
        self.__get_countries()

        #Cargamos los datos de cada pais
        self.__get_country_data

        # Formateamos los datos
        self.__clean_data

        # Guardamos el resultado en csv
        self.save_to_csv
        
        #Cargamos los paises pasados por parametros 
        self.__load_country_list()
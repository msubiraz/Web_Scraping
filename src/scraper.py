import requests
import pandas as pd
from bs4 import BeautifulSoup

class covid19Scraper():

    def __init__(self, pais):
        self.url ="https://www.worldometers.info"
        self.subdomain="/coronavirus/"
        self.data = []


    
    def __loaddata(self):
        page = requests.get(self.url+self.subdomain)

        return page
    
    def __get_covid19_links(self, page):
        pass 
    
    
    
    def scraper (self)
    
        #load data
        page =self.__loaddata()
    
    def __varis (self):

        
        

        soup = BeautifulSoup(page.content,'html.parser')

        #print(soup.prettify())
        soup.find_all('tr')[0].get_text()
        columnas = soup.find_all('tr')[0].get_text().split('\n')

        # Elimina el primer y ultimo elemento
        columnas.pop(0)
        columnas.pop(-1)

        columnas[8] = 'Tot Cases/1M pop'
        columnas

        # crea lista con los paises
        i=0
        paises = []
        for pais in soup.find_all('tr'):
            total = soup.find_all('tr')[i].get_text().split('\n')
            
            paises.append(total[1])
            i+=1

        paises.pop(0)
        paises.pop(-1)

        paises_clean = paises[:183]

        print('longitud lista paises: ',len(paises_clean))

        # crear una lista con la informacion de cada pais

        lista_info = []
        i,j,k = 0,0,0
        for num in range(len(paises_clean)):
        #    print(num)
            info = soup.find_all('tr')[num+1].get_text().split('\n')

            info.pop(0)
            info.pop(0)
            info.pop(-1)
            
            lista_info.append(info)
            
        print('longitud lista paises: ',len(paises_clean))
        print('longitud lista_info: ',len(lista_info))

        # Sustituye los espacios en blanco por 0
        for lista in lista_info:
            i=0
            #print(lista)
            for elem in lista:
                if elem == '':
                    lista[i] = "0"
                
                if elem == ' ':
                    lista[i] = "0"
                    
                i+= 1

        #lista_info

        # Elimina el simbolo + de los numeros
        for lista in lista_info:
            j,k=0,0
            for elem in lista:
                
                if elem[0] == '+': #si el elemento comienza con +
                    #print(elem[0])
                    lista[j]= elem.replace('+','')
                    
                lista[k]=float(elem.replace(',','')) # Quita la coma para indicar mil
                    
                
                j+=1
                k+=1


        # Convierte las cadenas en int
        for lista in lista_info:
            j=0
            for elem in lista:
                float(elem)


        # comprobar listas
        print('Longitud lista paises: ',len(paises_clean))
        print('longitud lista informacion: ',len(lista_info))

        # Dataframe
        df=pd.DataFrame(lista_info,columns=columnas[1:])

        df[columnas[0]] = paises_clean
        print('Agregamos la columna: ',columnas[0])

        # Cambia Country,Other a la posicion 1
        df = df[columnas]
        df.head()

        # Añadimos fecha

        import datetime
        # obtenemos el path desde la pagina web
        fecha_path = soup.find('div',{'style':'font-size:13px; color:#999; text-align:center'})

        print('La fecha se encuentra en la siguiente linea: \n\n',fecha_path)

        fecha = fecha_path.text[14:-4].split(',')

        hora = int(fecha[2].split(' ')[1].split(':')[0])
        minutos = int(fecha[2].split(' ')[1].split(':')[1])
        anyo = int(fecha[1].split(' ')[1])
        dia = int(fecha[0].split(' ')[1])
        mes = fecha[0].split(' ')[0]

        # Necesitamos obtener el numero del mes
        lista_meses = [datetime.date(2008, i, 1).strftime('%B') for i in range(1,13)] # crea lista de meses

        mes_num = lista_meses.index(mes)+1 # busca en la lista la posicion del mes del scraping

        # creamos un timestamp con la fecha de la ultima actualizacion
        time = pd.Timestamp(year=anyo, month=mes_num, day=dia, hour=hora, minute=minutos) 

        # crea una columna con el timestamp
        df['Time'] = [time for i in range(len(df[columnas[0]]))]

        df.set_index('Time', inplace=True) # convierte la columna Time en indice

        # Guardar dataframe en csv
        # Creamos un nombre de archivo
        # lo haremos de la siguiente forma
        # Corona_10-03-2020_T1550

        nombre = 'Corona_{}-{}-{}_T{}{}'.format(dia,mes,anyo,hora,minutos)
        nombre

        # Guarda el DataFrame actual en la carpeta deseada con el nombre en formato Corona_dd-mm-aaaa_Thhmm
        df.to_csv(r'PEC_1_Web_Scraping/{}.csv'.format(nombre), index = False)


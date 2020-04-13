import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import datetime

page = requests.get("https://www.worldometers.info/coronavirus/")

soup = BeautifulSoup(page.content,'html.parser')
# 2. Agrupamos la informacion en listas
# 2.1 Lista de los nombres de las columnas
soup.find_all('tr')[0].get_text().split('\n')

soup.find_all('tr')[0].get_text()
columnas = soup.find_all('tr')[0].get_text().split('\n')

# Elimina el primer y ultimo elemento
columnas.pop(0)
columnas.pop(-1)
columnas.pop(-2)
columnas.pop(-2)

columnas[0] = 'Country/Other'
columnas[8] = 'Tot Cases/1M pop' 
columnas[11] = "Tests/1M pop" 

# 2.2 Lista de los nombres de los paises
i=0
paises = []
for pais in soup.find_all('tr'):
    total = soup.find_all('tr')[i].get_text().split('\n')
    
    paises.append(total[1])
    i+=1

paises_clean = paises[paises.index("USA"):paises.index('China')+1]

print('longitud lista paises: ',len(paises_clean))

# 2.3 Lista de la informacion de cada pais
lista_info = []
i,j,k = 0,0,0
for num in range(9,len(paises_clean)+9):
#    print(num)
    info = soup.find_all('tr')[num].get_text().split('\n')

    info.pop(0)
    info.pop(-1)
    
    lista_info.append(info)

print('longitud lista paises: ',len(paises_clean))
print('longitud lista_info: ',len(lista_info))

# Tomamos todos los primeros elementos de las listas y lo guardamos 
# en una lista - paises y lo mismo con el ultimo elemento y lo guardamos 
# como continent
lista_paises = [lista[0] for lista in lista_info] 
lista_continentes = [lista[-1] for lista in lista_info] 

# lista_info -- La recorremos y quitamos la posicion de los paises y los 
# continentes, dejammos unicamente valores numericos
for lista in lista_info:
    lista.pop(0)
    lista.pop(-1)
    
# 3. Limpieza de datos
# 3.1 Elimina los espacios en blanco y sustituye por 0
for lista in lista_info:
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
for lista in lista_info:
    j,k=0,0
    for elem in lista:

        if elem[0] == '+': #si el elemento comienza con +
            lista[j]= elem.replace('+','')
        
        lista[k]=float(elem.replace(',','')) # Quita la coma para indicar mil
        #lista_test.append(lista[k])
        j+=1
        k+=1

# Convierte las cadenas en float
for lista in lista_info:
    j=0
    for elem in lista:
        if (lista.index(elem))==0:
            continue
        if (lista.index(elem)+1)==len(lista):
            continue
        float(elem)
        
# Como separamos las listas de continente y pais modificamos columnas
columnas_def = columnas[1:-1]
columnas_def

print("Comprobando longitud de listas.....\n")
print('Longitud lista paises: ',len(paises_clean))
print('longitud lista informacion: ',len(lista_info))
print("\nComprobando numero de columnas....\n")
print('Longitud lista columnas: ',len(columnas_def))
print('Lontigud sublistas info: ',len(lista_info[0]))

# 4. DataFrame
df=pd.DataFrame(lista_info,columns=columnas_def)

df[columnas[0]] = lista_paises
df[columnas[-1]] = lista_continentes

df = df[columnas] # Cambia Country,Other a la posicion 1

# 5. Anadimos a nuestro DataFrame la fecha de la ultima actualizacion y lo 
# guardamos en la ubicación deseada con el nombre deseado
# obtenemos el path desde la pagina web
fecha_path = soup.find('div',
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
df.to_csv(r'{}.csv'.format(nombre), index = False)
print('\n\nArchivo guardado como {}.csv'.format(nombre))
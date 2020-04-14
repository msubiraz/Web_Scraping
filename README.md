# Práctica 1: Web scraping

## Descripción

Repositorio creado para la práctica1 de la asignatura _Tipología y ciclo de vida de los datos_, del Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. 

La práctica gira entorno al Web Scraping y a la creación de repositorios para proyectos colaborativos.

## Miembros del equipo

La actividad ha sido realizada de manera conjunta por **Hugo Gomez** y **Marc Subirà**.

## Ficheros del código fuente

* **src/main.py**: punto de entrada al programa. Inicia el proceso de scraping.
* **src/scraper.py**: contiene la implementación de la clase _covid19Scraper_ para extraer información de la página https://www.worldometers.info/coronavirus/.
* **export.py**: Contiene la implementación de la classe export para la exportación de información --DEPRECATED

## Programa

Para la ejecución del programa es necesario disponer las siguientes librerias: 
* requests
* pandas 
* bs4.BeautifulSoup
* sys
* csv
* plotly
* plotly.express 
* pycountry

La ejecución del programa se realiza con el fichero main.py. El programa se puede ejecutar con argumentos de paises (en inglés) para los cuales se quiere extraer la informació. Si no se pasan argumentos, el programa extraerá la información de todos los paises.
```
python main.py {pais1} {pais2} {paisn}
```

El programa tiene como outputs
* fichero .csv con los datos de covid por país
* Visualizaciones abiertas en ventanas del navegador con los casos de covid y muertes, en mapa, por país 

## Recursos

1. Subirats, L., Calvo, M. (2019). Web Scraping. Editorial UOC.
2. Tutorial de Github https://guides.github.com/activities/hello-world.

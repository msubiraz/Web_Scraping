#from scraper import covid19Scraper

import sys

if __name__ == "__main__":
    pais =  sys.argv[1]
    paisos =[]
#    scraper=covid19Scraper()

    for i in range(len(sys.argv)):
        if i>0:
            paisos.append(sys.argv[i])

    print(paisos)



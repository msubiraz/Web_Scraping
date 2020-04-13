from scraper import covid19Scraper

import sys


if __name__ == "__main__":
    #countries=load_country_list()
    covid=covid19Scraper()
    covid.scraper()
    


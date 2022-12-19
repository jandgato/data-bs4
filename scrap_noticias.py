import csv
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

def scrape_el_pais(url):
    # create regular expressions to match URLs
    formed_link_ok = re.compile(r'^https?://.+/.+$')
    root_path_ok = re.compile(r'^/.+$')

    # send GET request to website and store response
    elpaismx = requests.get(url)

    # parse HTML of response and create BeautifulSoup object
    soup = BeautifulSoup(elpaismx.text, 'lxml')

    # find all headlines on website
    titulares = soup.find_all('h2', attrs={'class':'c_t'})

    # store links and text of headlines in separate lists
    links_titulares = [titular.a.get('href') for titular in titulares]
    texto_titulares = [titular.a.get_text() for titular in titulares]

    # create dictionaries for headlines and links
    titulares_dicc = {'titulares': texto_titulares}
    enlaces_dicc = {'enlaces': links_titulares}

    # combine dictionaries into single dictionary
    titulares_dicc.update(enlaces_dicc)

    # create DataFrame from dictionary
    df = pd.DataFrame(titulares_dicc, columns = ['titulares', 'enlaces'])

    # export DataFrame to CSV file
    with open('noticias_ElPais_MX.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=df.columns)
        writer.writeheader()
        for index, row in df.iterrows():
            writer.writerow(row.to_dict())

if __name__ == '__main__':
    try:
        # set URL of website to scrape
        url = 'https://elpais.com/mexico/'

        # scrape website
        scrape_el_pais(url)
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        # add delay to reduce load on server
        time.sleep(5)

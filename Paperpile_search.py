import requests
from bs4 import BeautifulSoup as Bs

from style import log, warning, error

"""
The purpose of this script is to look up the abbreviation of the journal name in the paperpile.com.
"""


def search(j_name):
    url = 'https://paperpile.com/guides/journal-abbreviations-list'
    response = requests.post(url)
    context = response.text
    soup = Bs(context, 'lxml')
    abb_urls = soup.find_all('a')
    for abb_url in abb_urls:
        if abb_url.get_text().upper() == j_name.upper():
            url = 'https://paperpile.com/' + abb_url.get('href')
            return get_Abbreviation(url)
    warning(f'The journal does not exist in the list. {j_name}')
    return None


def get_Abbreviation(url):
    response = requests.get(url)
    context = response.text
    soup = Bs(context, 'lxml')
    try:
        figure = soup.find('figure', {'class': 'infotable striped'})
        trs = figure.find_all('tr')
        for tr in trs:
            name = tr.find('th')
            value = tr.find('td')
            if name is None or value is None:
                continue
            if name.get_text() == 'Abbreviation':
                return value.get_text()
    except:
        error('There is an error in the journal details page.')
        error(url)
    return None

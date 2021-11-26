import re
import requests
from bs4 import BeautifulSoup as Bs

from style import warning, error


def search(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Journal abbreviation
    """
    url = 'https://cassi.cas.org/searching.jsp'
    body = {
        'searchIn': 'titles',
        'searchFor': j_name,
        'exactMatch': 'on',
        'c': 'WIy460-R_DY',
    }
    response = requests.post(url, body)

    if response.url == 'https://cassi.cas.org/no-result.jsp':
        warning(f'No result. {j_name}')
        return None
    elif response.url.find('results.jsp') > 0:
        warning(f'Multi choice. {j_name}')
        return multiple_choice(response.text, j_name)
    elif response.url.find('publication.jsp') > 0:
        return get_table_value(response.text)
    else:
        error(f'Unknown error. {j_name}')
        return None


def get_table_value(response):
    """
    :param response: {str} Content of a http requests
    :return: {str} Journal abbreviated
    """
    soup = Bs(response, 'lxml')

    table = soup.find('table', id='publication')

    for tr in table.find_all('tr'):
        if len(tr.contents) < 2:
            continue
        name = tr.find('td', {'class': 'name'})
        value = tr.find('td', {'class': 'value'})
        if name is None or value is None:
            continue
        if name.get_text() == 'Abbreviated Title':
            return value.get_text()
    return None


def disambiguation(string):
    """
    :param string: {str} The name contains certain symbols or '&'
    :return: {list} Clear the string of special symbols
    """
    punc = '\n'
    string = re.sub(r"[%s]+" % punc, "", string)

    string = string.upper().replace('&amp;', '&')
    string_and = string.replace('&', 'AND')
    return string, string_and


def multiple_choice(response, j_name):
    """
    :param response: {str} Content of a http requests
    :param j_name:  {str} Journal name
    :return: {str} Journal abbreviated
    """
    soup = Bs(response, 'lxml')

    table = soup.find('table', id='publication')

    for tr in table.find_all('tr'):
        name = tr.find('td', {'class': 'name'})
        value = tr.find('td', {'class': 'value'})
        if name is None or value is None:
            continue
        value_name = value.get_text().upper()
        if name.get_text() == 'Publication Title' and j_name.upper() in disambiguation(value_name):
            url = 'https://cassi.cas.org/' + value.find('a').get('href')
            warning(f'Choose the first.')
            return get_table_value(requests.get(url).text)

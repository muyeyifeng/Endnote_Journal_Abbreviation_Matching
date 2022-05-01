import re
import requests
from bs4 import BeautifulSoup as Bs

from style import log, warning, error

"""
The purpose of this script is to look up the abbreviation of the journal name in the Berkeley database.
"""


def check_page(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Page name
    """
    _ascii = ord(j_name.lower()[0])
    if _ascii == 97 or _ascii == 98:
        page = 'a-b'
    elif 99 <= _ascii <= 103:
        page = 'c-g'
    elif 104 <= _ascii <= 106:
        page = 'h-j'
    elif 107 <= _ascii <= 113:
        page = 'k-q'
    elif 114 <= _ascii <= 122:
        page = 'h-j'
    else:
        return None
    return page


def match(j_name, trs):
    """
    :param j_name: {str} Journal name
    :param trs: {object} Table's element
    :return: {str} Journal abbreviation
    """
    for tr in trs:
        tds = tr.find_all('td')
        if tds is not None and len(tds) == 2:
            name = tds[0].get_text()
            value = tds[1].get_text()
            if name == j_name:
                return value
    warning(f'The journal does not exist in the list. {j_name}')
    return None


def search(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Journal abbreviation
    """
    divs = get_page_content(j_name)
    if divs is not None:
        for div in divs:
            table = div.find('table')
            if table is not None:
                trs = table.find_all('tr')
                return match(j_name, trs)
    warning(f'The journal does not exist in the list. {j_name}')
    return None


def reverse_lookup_match(j_name, trs):
    """
    :param j_name: {str} Non-stander journal name
    :param trs: {object} Table's element
    :return: {str} Full journal name
    """
    for tr in trs:
        tds = tr.find_all('td')
        if tds is not None and len(tds) == 2:
            name = tds[0].get_text()
            value = tds[1].get_text()
            punc = '~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}'
            value = re.sub(r"[%s]+" % punc, "", value)
            if value == j_name:
                return name
    return None


def reverse_lookup(j_name):
    """
    :param j_name: {str} Non-stander journal name
    :return: {str} Full journal name
    """
    divs = get_page_content(j_name)
    if divs is None:
        return None
    for div in divs:
        table = div.find('table')
        if table is not None:
            trs = table.find_all('tr')
            return reverse_lookup_match(j_name, trs)
    return None


def get_page_content(j_name):
    """
    :param j_name: {str} Journal name
    :return: {object} Html page element
    """
    page = check_page(j_name)
    if page is None:
        return None
    url = f'https://guides.lib.berkeley.edu/bioscience-journal-abbreviations/{page}'
    response = requests.post(url)
    content = response.text
    soup = Bs(content, 'lxml')
    divs = soup.find_all('div', {'class': 'clearfix'})
    return divs

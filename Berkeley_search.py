import requests, re, string
from style import log, warning, error
from bs4 import BeautifulSoup as Bs

"""
a-b
c-g
h-j
k-q
r-z
"""


def check_page(j_name):
    asii = ord(j_name.lower()[0])
    if asii == 97 or asii == 98:
        page = 'a-b'
    elif 99 <= asii <= 103:
        page = 'c-g'
    elif 104 <= asii <= 106:
        page = 'h-j'
    elif 107 <= asii <= 113:
        page = 'k-q'
    elif 114 <= asii <= 122:
        page = 'h-j'
    else:
        return None
    return page


def match(j_name, trs):
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
    page = check_page(j_name)
    if page is None:
        return None
    url = f'https://guides.lib.berkeley.edu/bioscience-journal-abbreviations/{page}'
    response = requests.post(url)
    context = response.text
    soup = Bs(context, 'lxml')
    divs = soup.find_all('div', {'class': 'clearfix'})
    for div in divs:
        table = div.find('table')
        if table is not None:
            trs = table.find_all('tr')
            return match(j_name, trs)
    warning(f'The journal does not exist in the list. {j_name}')
    return None


def reverse_lookup_match(j_name, trs):
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
    page = check_page(j_name)
    if page is None:
        return None
    url = f'https://guides.lib.berkeley.edu/bioscience-journal-abbreviations/{page}'
    response = requests.post(url)
    context = response.text
    soup = Bs(context, 'lxml')
    divs = soup.find_all('div', {'class': 'clearfix'})
    for div in divs:
        table = div.find('table')
        if table is not None:
            trs = table.find_all('tr')
            return reverse_lookup_match(j_name, trs)
    return None

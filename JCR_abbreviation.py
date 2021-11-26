import requests


"""
The function of this script is to find the full name of the journal 
in the web of knowledge database according to the JCR abbreviation
"""


def JCR_abbreviation_search(j_name):
    """
    :param j_name:  {str} Journal name
    :return: {str} Journal abbreviated
    """
    alphabet = j_name.upper()[0]
    if ord(alphabet) < 65:
        alphabet = '0-9'
    url = f'https://images.webofknowledge.com/images/help/WOS/{alphabet}_abrvjt.html'
    content = requests.get(url).text

    start = content.find('<DL>') + len('<DL>')
    end = content.find('</DL>')
    content = content[start:end]

    index = 0
    while content.find('<DT>', index) >= 0:
        start_dt = content.find('<DT>', index) + len('<DT>')
        end_dt = content.find('<B>', index)

        start_dd = content.find('<DD>', index) + len('<DD>')
        end_dd = content.find('</B>', index)

        dt = content[start_dt:end_dt].strip()
        dd = content[start_dd:end_dd].strip()

        if dd == j_name.upper():
            return dt

        index = end_dd + 1

    return None

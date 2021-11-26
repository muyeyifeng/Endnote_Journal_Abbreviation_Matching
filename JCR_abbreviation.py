import requests


"""
The function of this script is to find the full name of the journal 
in the webofknowledge database according to the JCR abbreviation
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
    context = requests.get(url).text

    start = context.find('<DL>') + len('<DL>')
    end = context.find('</DL>')
    context = context[start:end]

    index = 0
    while context.find('<DT>', index) >= 0:
        start_dt = context.find('<DT>', index) + len('<DT>')
        end_dt = context.find('<B>', index)

        start_dd = context.find('<DD>', index) + len('<DD>')
        end_dd = context.find('</B>', index)

        dt = context[start_dt:end_dt].strip()
        dd = context[start_dd:end_dd].strip()

        if dd == j_name.upper():
            return dt

        index = end_dd + 1

    return None

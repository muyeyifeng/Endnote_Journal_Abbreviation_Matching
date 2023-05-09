import os

import yaml

from other_func.style import log
from data_from_website import CASSI_search as Cas, Berkeley_search as Ber

local_journal_abbreviation = {}


def find_abbreviation_match(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Journal_abbreviation
    """
    global local_journal_abbreviation

    log('Use Local')
    load_local_database()
    local_result = local_database_comparison(j_name)
    if local_result is not None:
        return local_result

    log('Use Berkeley')
    ber_result = Ber.search(j_name)
    if ber_result is not None:
        local_journal_abbreviation[j_name] = ber_result
        return ber_result

    log('Use CASSI')
    cas_result = Cas.search(j_name)
    if cas_result is not None:
        local_journal_abbreviation[j_name] = cas_result
        return cas_result
    return None


def load_local_database():
    """
    :return: null
    """
    global local_journal_abbreviation

    if not os.path.exists('local_database/Journal_abbreviation.yml'):
        open('local_database/Journal_abbreviation.yml', 'w', encoding='utf-8')
    with open('local_database/Journal_abbreviation.yml', 'r', encoding='utf-8') as f:
        local_journal_abbreviation = yaml.load(f, Loader=yaml.FullLoader)


def local_database_comparison(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Journal_abbreviation from local_database
    """
    if j_name in local_journal_abbreviation:
        return local_journal_abbreviation[j_name]
    return None
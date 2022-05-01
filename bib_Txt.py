import os
from style import log, warning, error

"""
The purpose of this script is to read the list of journals exported by Endnote
"""


def read_bib_txt(path):
    """
    :param path: {str} Path of journals lists exported by endnote x20
    :return: {list} A list of journals' name
    """
    if os.path.exists(path):
        lst = []
        with open(path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
            for line in lines:
                lst.append(line.split('\t')[0].replace('\n', ''))
        return lst
    error('File does not exist.')
    error(path)
    return None

"""
The purpose of this script is to read the list of journals exported by Endnote
"""


def read_bib_Txt(path):
    """
    :param path: {str} Path of journals list exported by endnote x20
    :return: {list} A list of journals' name
    """
    lst = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        for line in lines:
            lst.append(line.split('\t')[0].replace('\n', ''))
    return lst

import os

import yaml
from style import log, warning, error

'''
The function of this script is to write the yaml document and organize the content of the yaml document.
'''


def clear(yaml_path):
    """
    :param yaml_path: {str} Yaml path
    :return:
    """
    dict1 = {}
    if os.path.exists(yaml_path):
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(dict1, f)


def write_yaml_dict(yaml_path, dict1):
    """
    :param yaml_path:
    :param dict1:
    :return:
    """
    if os.path.exists(yaml_path):
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(dict1, f)


def update_yaml_from_text(new_journal_abbrev_path, old_yaml_path):
    """
    :param new_journal_abbrev_path: {str} Journal abbreviation file from other project, especially the format is
    <journal name>;<abbrev>
    :param old_yaml_path: {str} Journal_abbreviation.yml in this project. :return: null
    """
    if os.path.exists(new_journal_abbrev_path) and os.path.exists(old_yaml_path):
        with open(old_yaml_path, "r", encoding="utf-8") as f:
            data = f.read()
            dict1 = yaml.safe_load(data)

        with open(new_journal_abbrev_path, 'r', encoding='utf-8') as f:
            content_rows = f.readlines()
            for row in content_rows:
                row = row.replace('\n', '')
                row = row.replace('\t', '')
                if row.count(';') == 1:
                    key = row.split(';')[0]
                    value = row.split(';')[1]
                elif row.count(';') > 1:
                    log(row)
                    index = row.rfind(';')
                    key = row[0:index]
                    value = row[index + 1:-1]
                else:
                    log(row)
                    warning(f'Content format error.')
                    continue
                if key not in dict1.keys():
                    dict1[key] = value

        if dict1 is not None:
            with open(old_yaml_path, "w", encoding="utf-8") as f:
                yaml.dump(dict1, f)
    else:
        error(f'File does not exist.\n{new_journal_abbrev_path} \nand\n{old_yaml_path}')


def write_result_txt(bib_path, dict1):
    """
    :param dict1: {dict} Dictionary of journals' name from bib_text and their abbreviation
    :return: null
    """
    if type(dict1) is not dict or dict1 is None:
        return None
    bib_name = bib_path[0:bib_path.rfind('.')]
    path = f'{bib_name}_result.txt'
    write_yaml_dict(path, dict1)


def convert2txt(yaml_path, text_path):
    """
    :param yaml_path:
    :param text_path:
    :return:
    """
    if os.path.exists(yaml_path):
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = f.read()
            dict1 = yaml.safe_load(data)
        with open(text_path, 'w', encoding='utf-8') as f:
            for key in dict1.keys():
                name = key
                value = dict1[key]
                f.write(name + '\t' + str(value) + '\n')

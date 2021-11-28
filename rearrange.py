import yaml
from style import log, warning, error

'''
The function of this script is to write the yaml document and organize the content of the yaml document.
'''


def _rearrange(yaml_path):
    """
    :param yaml_path: {str} Yaml path
    :return: null
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = f.read()
        dic = yaml.safe_load(data)
    if dic is None:
        dic = {}
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(dic, f)


def write_yaml(yaml_path, key, value):
    """
    :param yaml_path: {str} Yaml path
    :param key: {str} Journal name
    :param value: {str} Journal abbreviation
    :return: null
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = f.read()
        dic = yaml.safe_load(data)
    if dic is None:
        dic = {}
    dic[key] = value
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(dic, f)


def rearrange():
    """
    :return: null
    """
    yaml_paths = ['Journal_abbreviation.yml',
                  'Equivalent_journal_name.yml',
                  'Unmatched_journals.yml']
    for yaml_path in yaml_paths:
        _rearrange(yaml_path)
    rewrite_journal_abbreviation()


def rewrite_journal_abbreviation():
    """
    :return: null
    """
    yaml_path = 'Journal_abbreviation.yml'
    text_path = 'Journal_abbreviation.txt'
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = f.read()
        dic = yaml.safe_load(data)

    with open(text_path, "w", encoding="utf-8") as f:
        for key in dic.keys():
            f.write(key + '\t' + dic[key] + '\n')


def update_yaml_from_text(new_journal_abbrev_path, old_yaml_path):
    """
    :param new_journal_abbrev_path: {str} Journal abbreviation file from other project, especially the format is
    <journal name>;<abbrev>
    :param old_yaml_path: {str} Journal_abbreviation.yml in this project. :return: null
    """
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
                dict1[key] = value
            elif row.count(';') > 1:
                log(row)
                index = row.rfind(';')
                key = row[0:index]
                value = row[index + 1:-1]
                dict1[key] = value
            else:
                log(row)
                warning(f'Content format error.')

    if dict1 is not None:
        with open(old_yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(dict1, f)

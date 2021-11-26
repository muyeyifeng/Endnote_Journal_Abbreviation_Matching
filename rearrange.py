import yaml

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

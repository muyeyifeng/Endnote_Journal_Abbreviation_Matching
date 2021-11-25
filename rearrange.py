import yaml

'''
The function of this script is to write the yaml document and organize the content of the yaml document.
'''


def _rearrange(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = f.read()
        dic = yaml.safe_load(data)
    if dic is None:
        dic = {}
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(dic, f)


def write_yaml(yaml_path, key, value):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = f.read()
        dic = yaml.safe_load(data)
    if dic is None:
        dic = {}
    dic[key] = value
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(dic, f)


def rearrange():
    yaml_paths = ['Journal_abbreviation.yml',
                  'Equivalent_journal_name.yml',
                  'Unmatched_journals.yml']
    for yaml_path in yaml_paths:
        _rearrange(yaml_path)

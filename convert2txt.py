import yaml


def convert2txt():
    yaml_path = 'Journal_abbreviation.yml'
    text_path = 'Journal_abbreviation.txt'
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = f.read()
        dic = yaml.safe_load(data)

    with open(text_path, "w", encoding="utf-8") as f:
        for key in dic.keys():
            f.write(key + '\t' + dic[key] + '\n')

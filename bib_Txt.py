def read_bib_Txt(path):
    dic = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        for line in lines:
            dic.append(line.split('\t')[0].replace('\n', ''))
    return dic

import yaml
import Auxiliary_method as Am
import Berkeley_search as Ber
import bib_Txt as Bt
import CASSI_search as Cas
import Paperpile_search as Pap
from JCR_abbreviation import JCR_abbreviation_search as Jcr
from style import log, warning, error
import rearrange


local_journal_abbreviation = None
local_equivalent_journal_name = None


def find_matches(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Journal_abbreviation
    """
    yaml_path = 'Journal_abbreviation.yml'
    log('Use Local')
    local_result = local_database_comparison(j_name)
    if local_result is not None:
        return local_result

    log('Use Berkeley')
    ber_result = Ber.search(j_name)
    if ber_result is not None:
        rearrange.write_yaml(yaml_path, j_name, ber_result)
        return ber_result

    log('Use Paperpile')
    pap_result = Pap.search(j_name)
    if pap_result is not None:
        rearrange.write_yaml(yaml_path, j_name, pap_result)
        return pap_result

    log('Use CASSI')
    cas_result = Cas.search(j_name)
    if cas_result is not None:
        rearrange.write_yaml(yaml_path, j_name, cas_result)
        return cas_result
    return None


def local_database_comparison(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Journal_abbreviation from local_database
    """
    if j_name in local_journal_abbreviation:
        return local_journal_abbreviation[j_name]
    return None


def equivalent_journal_name_local(j_name):
    """
    :param j_name: {str} Non-stander journal name
    :return: {str} Journal full name from local database
    """
    if j_name in local_equivalent_journal_name:
        return local_equivalent_journal_name[j_name]
    return None


def equivalent_journal_name(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Journal full name
    """
    data = equivalent_journal_name_local(j_name)
    if data is not None and j_name in data:
        return data[j_name]
    else:
        return reverse_Lookup(j_name)


def reverse_Lookup(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Journal full name from JCR or Berkeley
    """
    jcr_result = Jcr(j_name)
    if jcr_result is not None:
        return jcr_result
    ber_result = Ber.reverse_lookup(j_name)
    if ber_result is not None:
        return ber_result
    return None


def main_func(bib_text):
    """
    :param bib_text: {str} Endnote export journal list path
    :return: {dict} Dictionary of journals' name from bib_text and their abbreviation
    """
    j_names = Bt.read_bib_Txt(bib_text)
    dict1 = {}
    for j_name in j_names:
        log('Check journal name.')
        if Am.is_contain_chinese(j_name):
            warning('Chinese Journal.')
            continue

        ejn = equivalent_journal_name_local(j_name)
        if ejn is not None and ejn != j_name:
            log(f'{j_name} may not be the full name of the journal, the full name is {ejn}')
            abbreviation = find_matches(ejn)
        else:
            abbreviation = find_matches(j_name)

        if abbreviation is not None:
            dict1[j_name] = abbreviation
            print(j_name, '=>', abbreviation)
            continue
        else:
            warning(f'{j_name} may be a non-standard journal name.')
            warning('Try to find the full name of the journal.')
            ejn = equivalent_journal_name(j_name)
            if ejn is not None:
                log(f'Find the full name of the journal. {ejn}')
                yaml_path = 'Equivalent_journal_name.yml'
                rearrange.write_yaml(yaml_path, j_name, ejn)

                abbreviation = find_matches(ejn)
                if abbreviation is not None:
                    dict1[j_name] = abbreviation
                    print(j_name, '=>', abbreviation)
                    continue
            else:
                warning('Unable to find the full name of the journal.')

        rearrange.write_yaml('Unmatched_journals.yml', j_name, None)
        error(f"No match. {j_name}")
    return dict1


def write_txt(dict1):
    """
    :param dict1: {dict} Dictionary of journals' name from bib_text and their abbreviation
    :return: null
    """
    if type(dict1) is not dict or dict1 is None:
        return None
    with open('The_result_of_this_run.txt', 'w', encoding='utf-8') as f:
        for key in dict1.keys():
            name = key
            value = dict1[key]
            f.write(name + '\t' + value + '\n')


def load_local_database():
    global local_journal_abbreviation, local_equivalent_journal_name
    with open('Journal_abbreviation.yml', 'r', encoding='utf-8') as f:
        local_journal_abbreviation = yaml.load(f, Loader=yaml.FullLoader)
    with open('Equivalent_journal_name.yml', 'r', encoding='utf-8') as f:
        local_equivalent_journal_name = yaml.load(f, Loader=yaml.FullLoader)
    if local_equivalent_journal_name is None or local_journal_abbreviation is None:
        error('Loading local database error.')


if __name__ == '__main__':
    load_local_database()
    bib_texts = [r'Journal_list.txt']
    for _bib_text in bib_texts:
        _dict1 = main_func(_bib_text)
        write_txt(_dict1)

    rearrange.rearrange()

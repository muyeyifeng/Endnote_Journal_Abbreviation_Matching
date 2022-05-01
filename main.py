import yaml
import os
import Auxiliary_method as Am
import Berkeley_search as Ber
import bib_Txt as Bt
import CASSI_search as Cas
import Paperpile_search as Pap
from JCR_abbreviation import JCR_abbreviation_search as Jcr
from style import log, warning, error, emphasize
import rearrange


local_journal_abbreviation = {}
local_equivalent_journal_name = {}
local_unmatched_journals = {}


def find_matches(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Journal_abbreviation
    """
    global local_journal_abbreviation
    log('Use Local')
    local_result = local_database_comparison(j_name)
    if local_result is not None:
        return local_result

    log('Use Berkeley')
    ber_result = Ber.search(j_name)
    if ber_result is not None:
        local_journal_abbreviation[j_name] = ber_result
        return ber_result

    log('Use Paperpile')
    pap_result = Pap.search(j_name)
    if pap_result is not None:
        local_journal_abbreviation[j_name] = pap_result
        return pap_result

    log('Use CASSI')
    cas_result = Cas.search(j_name)
    if cas_result is not None:
        local_journal_abbreviation[j_name] = cas_result
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
        return reverse_lookup(j_name)


def reverse_lookup(j_name):
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
    if j_names is None:
        return None
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
                local_equivalent_journal_name[j_name] = ejn

                abbreviation = find_matches(ejn)
                if abbreviation is not None:
                    dict1[j_name] = abbreviation
                    print(j_name, '=>', abbreviation)
                    continue
            else:
                warning('Unable to find the full name of the journal.')
        local_unmatched_journals[j_name] = None
        error(f'No match. {j_name}')
    return dict1


def load_local_database():
    global local_journal_abbreviation, local_equivalent_journal_name, local_unmatched_journals

    if not os.path.exists('Journal_abbreviation.yml'):
        open('Journal_abbreviation.yml', 'w', encoding='utf-8')
    with open('Journal_abbreviation.yml', 'r', encoding='utf-8') as f:
        local_journal_abbreviation = yaml.load(f, Loader=yaml.FullLoader)

    if not os.path.exists('Equivalent_journal_name.yml'):
        open('Equivalent_journal_name.yml', 'w', encoding='utf-8')
    with open('Equivalent_journal_name.yml', 'r', encoding='utf-8') as f:
        local_equivalent_journal_name = yaml.load(f, Loader=yaml.FullLoader)

    if not os.path.exists('Unmatched_journals.yml'):
        open('Unmatched_journals.yml', 'w', encoding='utf-8')
    with open('Unmatched_journals.yml', 'r', encoding='utf-8') as f:
        local_unmatched_journals = yaml.load(f, Loader=yaml.FullLoader)

    if local_equivalent_journal_name is None or local_journal_abbreviation is None or local_unmatched_journals is None:
        error('Loading local database error.')
    else:
        rearrange.clear('Unmatched_journals.yml')


def completed():
    global local_journal_abbreviation, local_equivalent_journal_name, local_unmatched_journals

    emphasize(f'Writing Equivalent_journal_name.yml')
    rearrange.write_yaml_dict('Equivalent_journal_name.yml', local_equivalent_journal_name)
    emphasize('Completed.')
    emphasize(f'Writing Journal_abbreviation.yml')
    rearrange.write_yaml_dict('Journal_abbreviation.yml', local_journal_abbreviation)
    emphasize('Completed.')
    emphasize(f'Writing Unmatched_journals.yml')
    rearrange.write_yaml_dict('Unmatched_journals.yml', local_unmatched_journals)
    emphasize('Completed.')

    emphasize(f'Convert Unmatched_journals.yml => Unmatched_journals.txt')
    rearrange.convert2txt('Unmatched_journals.yml', 'Unmatched_journals.txt')
    emphasize('Completed.')
    emphasize(f'Convert Journal_abbreviation.yml => Journal_abbreviation.txt')
    rearrange.convert2txt('Journal_abbreviation.yml', 'Journal_abbreviation.txt')
    emphasize('Completed.')


if __name__ == '__main__':
    load_local_database()
    bib_text_paths = []
    while True:
        log('Input bib_text path. (eg. ./Journal_list.txt or D://Journal_list.txt)')
        log('Has default: ./Journal_list.txt')
        log('Input 0 or empty to complete.')
        bit_text_tmp = input('Path:\t')
        if bit_text_tmp == '0' or bit_text_tmp == 0 or bit_text_tmp == '' or bit_text_tmp is None:
            if len(bib_text_paths) == 0:
                bib_text_paths.append(r'./Journal_list.txt')
            break

        if os.path.isdir(bit_text_tmp):
            warning('Input a directory path.')
            warning('Expect the input path to point to a file.')
        elif os.path.exists(bit_text_tmp):
            emphasize('File does exists.')
            bib_text_paths.append(bit_text_tmp)
        else:
            warning('The entered directory does not exist.')

    emphasize(str(bib_text_paths))
    for bib_text_path in bib_text_paths:
        result_dict1 = main_func(bib_text_path)
        if result_dict1 is not None:
            emphasize(f'Writing result for {bib_text_path}.')
            rearrange.write_result_txt(bib_text_path, result_dict1)

    completed()
    input('Press any key to close the window.')

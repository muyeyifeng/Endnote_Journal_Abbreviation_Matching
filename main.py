import yaml
import os
import time
from data_from_website import Berkeley_search as Ber, CASSI_search as Cas
from other_func.requires import install_requires
from search_func.Journal_abbreviation import find_abbreviation_match as fabb
from other_func.Auxiliary_method import is_contain_chinese as is_chinese
from other_func import rearrange, bib_Txt as Bt
from other_func.style import log, warning, error, emphasize

local_journal_abbreviation = {}
local_journal_full_name = {}
local_unmatched_full_name = {}
local_unmatched_abbreviation = {}


def load_journal_abbreviation():
    """
    :return:
    """
    global local_journal_abbreviation
    if not os.path.exists('local_database/Journal_abbreviation.yml'):
        open('local_database/Journal_abbreviation.yml', 'w', encoding='utf-8')
    with open('local_database/Journal_abbreviation.yml', 'r', encoding='utf-8') as f:
        local_journal_abbreviation = yaml.load(f, Loader=yaml.FullLoader)


def load_journal_full_name():
    """
    :return:
    """
    global local_journal_full_name
    if not os.path.exists('local_database/Journal_full_name.yml'):
        open('local_database/Journal_full_name.yml', 'w', encoding='utf-8')
    with open('local_database/Journal_full_name.yml', 'r', encoding='utf-8') as f:
        local_journal_full_name = yaml.load(f, Loader=yaml.FullLoader)


def load_unmatched_full_name():
    """
    :return:
    """
    if not os.path.exists('local_database/Unmatched_full_name.yml'):
        open('local_database/Unmatched_full_name.yml', 'w', encoding='utf-8')


def load_unmatched_abbreviation():
    """
    :return:
    """
    if not os.path.exists('local_database/Unmatched_abbreviation.yml'):
        open('local_database/Unmatched_abbreviation.yml', 'w', encoding='utf-8')


def load_local_database():
    """
    :return: null
    """
    load_unmatched_abbreviation()
    load_unmatched_full_name()
    load_journal_abbreviation()
    load_journal_full_name()
    if local_journal_full_name is None or local_journal_abbreviation is None:
        error('Loading local database error.')
    else:
        rearrange.clear('local_database/Unmatched_full_name.yml')
        rearrange.clear('local_database/Unmatched_abbreviation.yml')


def input_journal_list_path():
    """
    :return: input_journal_list_path
    """
    paths = []
    while True:
        log('Input bib_text path. (eg. ./Journal_list.txt or D://Journal_list.txt)')
        log('Default: ./input_journal_list/Journal_list.txt')
        log('Input 0 or empty to complete.')
        bit_text_tmp = input('Path:\t')
        if bit_text_tmp == '0' or bit_text_tmp == 0 or bit_text_tmp == '' or bit_text_tmp is None:
            if len(paths) == 0:
                paths.append(r'./input_journal_list/Journal_list.txt')
            break

        if os.path.isdir(bit_text_tmp):
            warning('Input a directory path.')
            warning('Expect the input path to point to a file.')
        elif os.path.exists(bit_text_tmp):
            emphasize('File does exists.')
            paths.append(bit_text_tmp)
        else:
            warning('The entered directory does not exist.')
    return paths


def journal_full_name_local(j_name):
    """
    :param j_name: {str} Non-stander journal name
    :return: {str} Journal full name from local database
    """
    global local_journal_full_name

    if j_name in local_journal_full_name:
        return local_journal_full_name[j_name]
    return None


def find_journal_full_name(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Journal full name
    """
    full_name = journal_full_name_local(j_name)
    if full_name is not None:
        return full_name
    else:
        return reverse_lookup(j_name)


def reverse_lookup(j_name):
    """
    :param j_name: {str} Journal name
    :return: {str} Journal full name from JCR or Berkeley
    """
    cas_result = Cas.reverse_lookup(j_name)
    if cas_result is not None:
        return cas_result

    ber_result = Ber.reverse_lookup(j_name)
    if ber_result is not None:
        return ber_result

    return None


def search_fullname(j_name):
    """
    :param j_name:
    :return:
    """
    global local_journal_full_name, local_unmatched_full_name

    j_full_name = journal_full_name_local(j_name)
    if j_full_name is None:
        warning(f'{j_name} may be a non-standard journal name.')
        warning('Try to find the full name of the journal.')
        j_full_name = find_journal_full_name(j_name)

    if j_full_name is None:
        error(f'Unable to find the full name of the journal. {j_name}')
        local_unmatched_full_name[j_name] = None
        update_local_unmatched_full_name()
    else:
        log(f'Find the full name of the journal. {j_full_name}')
        local_journal_full_name[j_name] = j_full_name
        update_local_full_name()

    return j_full_name


def search_abbreviation(j_name, j_full_name):
    """
    :param j_name:
    :param j_full_name:
    :return:
    """
    global local_journal_abbreviation

    abbreviation = fabb(j_name)
    if abbreviation is None and j_full_name is not None:
        warning(f'{j_name} may be a non-standard journal name.')
        warning('Try to find the full name of the journal.')
        abbreviation = fabb(j_full_name)

    if abbreviation is None:
        error(f'Unable to find the abbreviation of the journal. {j_name}')
        local_unmatched_abbreviation[j_name] = None
        update_local_unmatched_abbreviation()
    else:
        log(f'Find the abbreviation of the journal. {j_name}')
        local_journal_abbreviation[j_name] = abbreviation
        update_local_abbreviation()

    return abbreviation


def search_func(bib_text):
    """
    :param bib_text: {str} Endnote export journal list path
    :return: {dict} Dictionary of journals' name from bib_text and their abbreviation
    """
    j_names = Bt.read_bib_txt(bib_text)
    if j_names is None:
        return None
    dict1 = {}
    total = len(j_names)
    i = 0
    for j_name in j_names:
        abb_child = {}
        localtime = time.asctime(time.localtime(time.time()))
        log(f'{localtime}\n{i}/{total}')
        log('Check journal name.')
        if is_chinese(j_name):
            warning('Chinese Journal.')
            continue

        j_full_name = search_fullname(j_name)
        abb_child["full"] = j_full_name

        abbreviation = search_abbreviation(j_name, j_full_name)
        abb_child["abbreviation"] = abbreviation

        dict1[j_name] = abb_child
    return dict1


def update_local_full_name():
    """
    :return:
    """
    global local_journal_full_name
    emphasize(f'Writing Journal_full_name.yml')
    rearrange.write_yaml_dict('local_database/Journal_full_name.yml', local_journal_full_name)
    emphasize('Completed.')


def update_local_abbreviation():
    """
    :return:
    """
    global local_journal_abbreviation
    emphasize(f'Writing Journal_abbreviation.yml')
    rearrange.write_yaml_dict('local_database/Journal_abbreviation.yml', local_journal_abbreviation)
    emphasize('Completed.')


def update_local_unmatched_full_name():
    """
    :return:
    """
    global local_unmatched_full_name
    emphasize(f'Writing Unmatched_full_name.yml')
    rearrange.write_yaml_dict('local_database/Unmatched_full_name.yml', local_unmatched_full_name)
    emphasize('Completed.')


def update_local_unmatched_abbreviation():
    """
    :return:
    """
    global local_unmatched_abbreviation
    emphasize(f'Writing Unmatched_abbreviation.yml')
    rearrange.write_yaml_dict('local_database/Unmatched_abbreviation.yml', local_unmatched_abbreviation)
    emphasize('Completed.')


def convert_journal_abbreviation_yml2txt():
    """
    :return:
    """
    emphasize(f'Convert Journal_abbreviation.yml => Journal_abbreviation.txt')
    rearrange.convert2txt('local_database/Journal_abbreviation.yml', 'output_files/Journal_abbreviation.txt')
    emphasize('Completed.')


def completed():
    """
    :return:
    """
    update_local_full_name()
    update_local_abbreviation()
    update_local_unmatched_full_name()
    update_local_unmatched_abbreviation()
    convert_journal_abbreviation_yml2txt()


if __name__ == '__main__':
    install_requires()
    load_local_database()
    bib_text_paths = input_journal_list_path()
    emphasize(str(bib_text_paths))
    time.sleep(2)

    for bib_text_path in bib_text_paths:
        result_dict1 = search_func(bib_text_path)
        if result_dict1 is not None:
            emphasize(f'Writing result for {bib_text_path}.')
            rearrange.write_result_txt(bib_text_path, result_dict1)

    completed()
    input('Press any key to close the window.')

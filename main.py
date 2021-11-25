import yaml

import convert2txt as cert
import Berkeley_search as Ber
import CASSI_search as Cas
import Paperpile_search as Pap
import bib_Txt as Bt
from JCR_abbreviation import JCR_abbreviation_search as Jcr
from style import log, warning, error
from rearrange import write_yaml, rearrange


def find_matches(j_name):
    yaml_path = 'Journal_abbreviation.yml'
    log('Use Local')
    local_result = local_database_comparison(j_name)
    if local_result is not None:
        return local_result

    log('Use Berkeley')
    ber_result = Ber.search(j_name)
    if ber_result is not None:
        write_yaml(yaml_path, j_name, ber_result)
        return ber_result

    log('Use Paperpile')
    pap_result = Pap.search(j_name)
    if pap_result is not None:
        write_yaml(yaml_path, j_name, pap_result)
        return pap_result

    log('Use CASSI')
    cas_result = Cas.search(j_name)
    if cas_result is not None:
        write_yaml(yaml_path, j_name, cas_result)
        return cas_result
    return None


def local_database_comparison(j_name):
    with open('Journal_abbreviation.yml', 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        if data is not None and j_name in data:
            return data[j_name]
    return None


def equivalent_journal_name_local(j_name):
    with open('Equivalent_journal_name.yml', 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        if data is not None and j_name in data:
            return data[j_name]
    return None


def equivalent_journal_name(j_name):
    data = equivalent_journal_name_local(j_name)
    if data is not None and j_name in data:
        return data[j_name]
    else:
        return reverse_Lookup(j_name)


def reverse_Lookup(j_name):
    jcr_result = Jcr(j_name)
    if jcr_result is not None:
        return jcr_result
    ber_result = Ber.reverse_lookup(j_name)
    if ber_result is not None:
        return ber_result
    return None


def main_func(bib_text):
    j_names = Bt.read_bib_Txt(bib_text)
    dict1 = {}
    for j_name in j_names:
        log('Check journal name.')
        ejn = equivalent_journal_name_local(j_name)
        if ejn is not None and ejn != j_name:
            log(f'{j_name} may not be the full name of the journal, the full name is {ejn}')
            j_name = ejn
        abbreviation = find_matches(j_name)
        if abbreviation is not None:
            dict1[j_name] = abbreviation
            print(j_name, '=>', abbreviation)
            continue
        else:
            warning(f'{j_name} may be a non-standard journal name.')
            warning('Try to find the original name of the journal.')
            ejn = equivalent_journal_name(j_name)
            if ejn is not None:
                log(f'Find the full name of the journal. {ejn}')
                yaml_path = 'Equivalent_journal_name.yml'
                write_yaml(yaml_path, j_name, ejn)
                abbreviation = find_matches(ejn)
                if abbreviation is not None:
                    dict1[j_name] = abbreviation
                    print(j_name, '=>', abbreviation)
                    continue
            else:
                warning('Unable to find the full name of the journal.')
        write_yaml('Unmatched_journals.yml', j_name, None)
        error(f"No match. {j_name}")
    return dict1


if __name__ == '__main__':

    bib_texts = [r'Review.txt']

    for bib_text in bib_texts:
        main_func(bib_text)

    rearrange()
    cert.convert2txt()

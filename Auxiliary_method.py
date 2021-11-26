def is_contain_chinese(check_str):
    """
    Determine whether the string contains Chinese
    :param check_str: {str} The string to be detected
    :return: {bool} Return True if included, False if not included
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

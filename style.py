"""
30 | 40 | 黑色
31 | 41 | 红色
32 | 42 | 绿色
33 | 43 | 黃色
34 | 44 | 蓝色
35 | 45 | 紫红色
36 | 46 | 青蓝色
37 | 47 | 白色
"""


"""
This script defines the debug output format.
"""


def log(text):
    """
    :param text: {str} Log content
    :return: null
    """
    print(f'\033[1;32mLog: {text}\033[0m')


def warning(text):
    """
    :param text: {str} Warning content
    :return: null
    """
    print(f'\033[1;33mWaring: {text}\033[0m')


def error(text):
    """
    :param text: {str} Error content
    :return: null
    """
    print(f'\033[1;31mError: {text}\033[0m')
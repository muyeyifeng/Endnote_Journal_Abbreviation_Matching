def check_requirement(require, package):
    """
    :param require:
    :param package:
    :return:
    """
    flag = False
    try:
        exec("import {0}".format(require))
    except ModuleNotFoundError:
        import os
        print("Execute commands: pip3 install {0}".format(package))
        os.system("pip3 install {0}".format(package))
        flag = True
    return flag


def install_requires():
    """
    :return:
    """
    require_dict = {"yaml": "pyyaml", "requests": "requests", "beautifulsoup4": "beautifulsoup4"}
    flag = False
    for key in require_dict:
        flag = check_requirement(key, require_dict[key])
    return flag

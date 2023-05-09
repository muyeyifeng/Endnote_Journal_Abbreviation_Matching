def check_requirement(require, package):
    """
    :param require:
    :param package:
    :return:
    """
    try:
        exec("import {0}".format(require))
    except ModuleNotFoundError:
        inquiry = input("This script requires {0}. Do you want to install {0}? [y/n]".format(package))
        while (inquiry != "y") and (inquiry != "n"):
            inquiry = input("This script requires {0}. Do you want to install {0}? [y/n]".format(package))
        if inquiry == "y":
            import os
            print("Execute commands: pip3 install {0}".format(package))
            os.system("pip3 install {0}".format(package))
        else:
            print("{0} is missing, so the program exits!".format(package))
            exit(-1)


def install_requires():
    """
    :return:
    """
    require_dict = {"yaml": "pyyaml", "requests": "requests", "beautifulsoup4": "beautifulsoup4"}
    for (requirement, package) in require_dict:
        check_requirement(requirement, package)

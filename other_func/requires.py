requirements = ["yaml", "requests", "beautifulsoup4"]


def check_requirement(package):
    """
    :param package:
    :return:
    """
    try:
        exec("import {0}".format(package))
    except ModuleNotFoundError:
        inquiry = input("This script requires {0}. Do you want to install {0}? [y/n]".format(package))
        while (inquiry != "y") and (inquiry != "n"):
            inquiry = input("This script requires {0}. Do you want to install {0}? [y/n]".format(package))
        if inquiry == "y":
            import os
            print("Execute commands: pip install {0}".format(package))
            os.system("pip install {0}".format(package))
        else:
            print("{0} is missing, so the program exits!".format(package))
            exit(-1)


def install_requires():
    """
    :return:
    """
    for requirement in requirements:
        check_requirement(requirement)

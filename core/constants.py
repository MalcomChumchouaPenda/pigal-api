# Définir les constantes globales utilisées par Flask et Dash

import os


SERVICE_NAME_EXP = '([a-z][a-z0-9]*)_v[0-9_]+'


CORE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CORE_DIR)
STORE_DIR = os.path.join(CORE_DIR, 'store')
SERVICES_DIR = os.path.join(ROOT_DIR, 'services')
PAGES_DIR = os.path.join(ROOT_DIR, 'pages')
TESTS_DIR = os.path.join(ROOT_DIR, 'tests')


ENCODINGS = []
for i in os.listdir(os.path.split(__import__("encodings").__file__)[0]):
    name=os.path.splitext(i)[0]
    try:
        "".encode(name)
    except:
        pass
    else:
        ENCODINGS.append(name.replace("_","-"))


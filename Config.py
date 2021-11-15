import os

import yaml


def set_config(key, value):
    if not os.path.exists('config.yaml'):
        with open('config.yaml', 'x'):
            pass
    with open('config.yaml') as file:
        doc = yaml.full_load(file)
    if not doc:
        doc = {}
    doc[key] = value
    with open('config.yaml', 'w') as file:
        yaml.dump(doc, file)


def set_config_alias(n, p, name):
    if not os.path.exists('config.yaml'):
        with open('config.yaml', 'x'):
            pass
    with open('config.yaml') as file:
        doc = yaml.full_load(file)
    if not doc:
        doc = {}
    if f'{name}_aliases' not in doc.keys():
        doc[f'{name}_aliases'] = {}
    doc[f'{name}_aliases'][n] = p
    with open('config.yaml', 'w') as file:
        yaml.dump(doc, file)


def get_config(key):
    if not os.path.exists('config.yaml'):
        with open('config.yaml', 'x'):
            pass
    with open('config.yaml') as file:
        docs = yaml.full_load(file)
        if not docs:
            return None
        if key.lower() in docs.keys():
            return docs[key]
    return None

import os
import json

def get_path(): 
    return os.path.dirname(os.path.realpath(__file__))

def google_value(list_, lang):    
    for _ in list_:
        if _['lang'].casefold() == lang.casefold():
            return _['code']
    g_json = json.load(open(f"{get_path()}/datas/googleLangCodes.json", "r"))
    return g_json[key]

def get_engine_data(engine):
    google = 'googleLangCodes.json'
    duckduckgo = 'duckduckgoLangCodes.json'
    path = f"{get_path()}/datas/"

    if engine == 'google':
        json_path = os.path.join(path, google)
    elif engine == "duckduckgo":
        json_path = os.path.join(path, duckduckgo)

    d_list = json.load(open(json_path, "r"))

    return d_list

def code_to_lang(list_, code):
    for _ in list_:
        if _['code'].casefold() == code.casefold():
            return _['lang']

def lang_to_code(list_, lang):
    for _ in list_:
        if _['lang'].casefold() == lang.casefold():
            return _['code']
    

def get_index(list_, lang: str):    
    for index, _ in enumerate(list_):
        if _['lang'].casefold() == lang.casefold():
            return index
import os
import json

def get_path(): 
    return os.path.dirname(os.path.realpath(__file__))
   
def google_list():    
    g_json = json.load(open(f"{get_path()}/datas/google-data-language-code.json", "r"))
    return [x for x in g_json]

def google_value(key):    
    g_json = json.load(open(f"{get_path()}/datas/google-data-language-code.json", "r"))
    return g_json[key]

def code_to_lang(key):
    g_json = json.load(open(f"{get_path()}/datas/google-data-language-code.json", "r"))
    value_l = list(g_json.values())
    key_l = list(g_json.keys())
    # Reverse dictionary lookup, takes value ('en') returns key ('English')
    for (v, k) in zip(value_l, key_l):        
        if v == key:            
            return k

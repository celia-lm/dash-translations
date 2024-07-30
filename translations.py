import inspect
import re
from flask import session
from dash import set_props, html, dcc
from icecream import ic

# https://www.geeksforgeeks.org/debugging-with-ice-cream-in-python/
#ic.enable()
#ic.configureOutput(includeContext=True) 
ic.disable()

DEFAULT_LANGUAGE = "en"
DEFAULT_PAGE = "home"

TRANSLATIONS = {
    "en": {
        'app':{
            "app-title.children": "My app",
            "link-home.children":"Home page",
            "link-math.children":"Calculator",
        },
        'home':{
            "home-title.children": "Hello world",
            "home-subtitle.children": "This is the home page.",
            "country.children": "Country",
            "year.children": "Year", 
            "country-dropdown.options":{
                'france':'France',
                'canada':'Canada',
                'usa':'USA',
                'uk':'United Kingdom'
                }
        },
        'math':{
            "calculate.children":"Calculate!",
            "operation-text.children":{
                '+':'sum', 
                '-':'substraction', 
                'x':'product', 
                '/':'division'
            },
            "math-output-text.children": "Result of the "
        }
    },
    "es": {
        "app":{
            "app-title.children": "Mi título",
            "link-home.children":"Página de inicio",
            "link-math.children":"Calculadora",
        },
        "home":{
            "home-title.children": "Hola mundo",
            "home-subtitle.children": "Esta es la página de inicio.",
            "country.children": "País",
            "year.children": "Año",
            "country-dropdown.options":{
                'france':'Francia',
                'canada':'Canada',
                'usa':'EEUU',
                'uk':'Reino Unido'
                }
        },
        'math':{
            "calculate.children":"¡Calcular!",
            "operation-text.children":{
                '+':'suma', 
                '-':'resta', 
                'x':'multiplicación', 
                '/':'división'
            },
            "math-output-text.children": "Resultado de la "
        }
    },
}

def translated_item(
    item_id, language=DEFAULT_LANGUAGE, page=None, 
    multiple=False, multiple_key=None,
    translations=TRANSLATIONS, 
    ):
    
    if 'language' in session:
        language = session['language']

    if not page:
        if 'current_page' in session:
            page = session['current_page']
        else:
            page = DEFAULT_PAGE

    item = translations.get(language, {}).get(page, {}).get(item_id)
    
    if multiple:
        ic(f"translating {item_id}, page: {page}, lan:{language}, multiple_key: {multiple_key} > result: {item.get(multiple_key)}")
        session['multiple_keys'][f"{page}.{item_id}"] = multiple_key
        #https://stackoverflow.com/a/39261342 reason for session.modified=True
        session.modified = True
        return item.get(multiple_key)
    else :
        ic(f"translating {item_id}, page: {page}, lan:{language} > result: {item}")  
        return item

def text_to_translate(text_id, multiple=False, multiple_key=None):
    return html.Span(
        children=translated_item(
            item_id=f"{text_id}.children",
            multiple=multiple,
            multiple_key=multiple_key
            ), 
        id=text_id
    )

def translated_page(translations=TRANSLATIONS, language=DEFAULT_LANGUAGE, page=None):
    # define language
    if 'language' in session:
        language = session['language']

    # define page
    if not page:
        page = DEFAULT_PAGE

    multiple_keys = session['multiple_keys']

    lang_dict = translations.get(language).get(page)

    for k,v in lang_dict.items():
        item_id, item_prop = k.split('.')
        if f"{page}.{k}" in multiple_keys.keys():
            item_value = v.get(multiple_keys[f"{page}.{k}"])
        else:
            item_value = v
        
        ic(f'set_props({item_id}, {item_prop}:{item_value})')
        set_props(item_id, {item_prop:item_value})
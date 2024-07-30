from dash import Input, Output, State, callback, dcc, html, register_page
from translations import TRANSLATIONS, text_to_translate, translated_item
from flask import session

def layout():
    """Home page layout"""
    default_country = 'france' # this should match the key of the options
    default_year = 2020

    return [
        html.H1(translated_item('home-title.children'), id='home-title'),
        html.H2(translated_item('home-subtitle.children'), id='home-subtitle'),
        html.Div(
            [
                dcc.Dropdown(
                    id="country-dropdown",
                    value=default_country,
                    options=translated_item("country-dropdown.options"),
                    style={"minWidth": 200}
                ),
                dcc.Dropdown(
                    id="year-dropdown",
                    value=default_year,
                    options=[{"label": str(y), "value": y} for y in range(1980, 2021)],
                    style={"minWidth": 200}
                ),
            ],
            style={"display": "flex", "gap": "1rem", "marginBottom": "2rem"},
        ),
        html.Div(id="contents")
    ]

@callback(
    Output("contents", "children"),
    Input("country-dropdown", "value"),
    Input("year-dropdown", "value")
)
def update_contents(country, year):
    """Update the contents when the dropdowns are updated."""
    language = session['language'] 
    translation_page_values = TRANSLATIONS.get(language).get('home')

    contents = html.Span([
        text_to_translate('country'),
        # we use this so that we get the "label" in the right language, the value will be the same 
        # if the language is English (value=france, label=France) or Spanish (value=france, label=Francia)
        f": {translation_page_values.get('country-dropdown.options').get(country)}, ", 
        text_to_translate('year'),
        f": {year}"
    ])
    return contents

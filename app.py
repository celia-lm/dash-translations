from dash import Dash, Input, Output, State, callback, dcc, html, ctx
import dash
from translations import DEFAULT_LANGUAGE, translated_item, translated_page
import pages
from flask import session
from icecream import ic
import os

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server
server.secret_key = os.environ.get('FLASK_SECRET_KEY', b'123456abcdef') # random string prefixed by b so it's bytes

def app_layout():
    # for the translated_items of this layout we need to specify page='app',
    # otherwise it will take the page name of the children page that's being rendered at the moment (home, math)
    return html.Div(
    [
        html.Div(
            [
                # We will need to update the title when the language changes as it is
                # rendered outside the page layout function
                html.Div(
                    id="app-title",
                    children=translated_item('app-title.children', page='app'), 
                    style={"fontWeight": "bold"}
                    ),
                html.Span(style={"padding-right":"20px"}),
                html.Div([
                    dcc.Link(id='link-home', href=dash.get_relative_path('/'), children=translated_item('link-home.children', page='app')),
                    html.Span(style={"padding-right":"20px"}),
                    dcc.Link(id='link-math', href=dash.get_relative_path('/math'), children=translated_item('link-math.children', page='app'))
                ]),
                html.Div(
                    [
                        # Language dropdown
                        dcc.Dropdown(
                            id="language",
                            options=[
                                {"label": "English", "value": "en"},
                                {"label": "Español", "value": "es"},
                            ],
                            value=DEFAULT_LANGUAGE,
                            persistence=True,
                            clearable=False,
                            searchable=False,
                            style={"minWidth": 150},
                        ),
                    ],
                    style={"marginLeft": "auto", "display": "flex", "gap": 10}
                )
            ],
            style={
                "background": "#CCC",
                "padding": 10,
                "marginBottom": 20,
                "display": "flex",
                "alignItems": "center",
            },
        ),
        # routing elements
        dcc.Location(id='location'),
        html.Div(id='content')
    ],
    style={"fontFamily": "sans-serif"}
)

app.layout = app_layout

# routing callback
@callback(
    Output('content', 'children'),
    Input('location', 'pathname')
)
def display_page(pathname):
    path = dash.strip_relative_path(pathname).strip()
    ic("location session:", session)
    # save location
    if not path: # path="/"
        path = 'home'  
        
    session['current_page'] = path

    # create defaults
    if 'language' not in session:
        session['language'] = DEFAULT_LANGUAGE
    if 'multiple_keys' not in session:
        session['multiple_keys'] = {}

    if path == 'math':
        return pages.math.layout()
    else:
        return pages.home.layout()

@callback(
    Input("language", "value")
    )
def update_main_layout_language(language: str):
    """Save the language to session"""
    ic(session)
    session['language'] = language
    ic(session)
    """Translate the parts of the layout outside of the pages layout functions."""
    translated_page(page="app")
    translated_page(page=session['current_page'])

if __name__ == "__main__":
    app.run(debug=True)
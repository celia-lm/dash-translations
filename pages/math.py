from dash import Input, Output, State, callback, dcc, html, register_page
from translations import text_to_translate, translated_item
from flask import session

def layout():
    """Page 1 layout"""

    return [
        html.Div([
            dcc.Input(id='number1', type='number', min=1, value=1),
            dcc.Dropdown(
                id='operation',
                options=["+", "-", "x", "/"],
                value='+'
            ),
            dcc.Input(id='number2', type='number', min=1, value=1),
            html.Button(id="calculate", children=translated_item("calculate.children"))
        ],
        style={
            "display": "flex",
            "alignItems": "center",
            },),
        html.Div(id="math-output")
    ]

@callback(
    Output("math-output", "children"),
    Input("calculate", "n_clicks"),
    State("operation", "value"),
    State("number1", "value"),
    State("number2", "value"),
    prevent_initial_call=True
)
def update_contents(click, operation, n1, n2):
    
    language = session['language'] 

    if operation == '+':
        result = n1+n2
    elif operation == '-':
        result = n1-n2
    elif operation == 'x':
        result=n1*n2
    else:
        result=n1/n2
    
    contents = html.Span([
        text_to_translate('math-output-text'),
        text_to_translate('operation-text', multiple=True, multiple_key=operation),
        #f"{translation_page_values.get('operation-text.children').get(operation)}: ", 
        ": ",
        str(result)
    ])
    return contents

This is a summary of what the app does:

- It uses traditional routing, as you requested.
- It uses the new (`dash>=2.17.1`) `set_props` feature: https://dash.plotly.com/advanced-callbacks#setting-properties-directly
  - I've decided to use this because it allows me to modify the text of multiple components (div children, input value, etc) without specifying them as outputs. I believe this simplifies the code a lot.
  - Compared to the docs example, the `TRANSLATIONS` dict is created in a different file (`translations.py`) to keep a cleaner organization.
  - I have also created some helper functions in `translations.py` to be used in the layout.
- The language is saved as part of the user's flask session, as well as the name of the current page and other relevant translation values.
- I use the `icrecream` library just for debugging purposes.
  - It's like a replacement for print() statements and I find it very useful, but it's not necessary at all for the example.
  - Here's more info about icrecream: https://milangeorge10.medium.com/icecream-a-nifty-debugging-tool-4ce26ec56bbb

If you want to implement this translation logic in an existing app, you'll need to:

- Copy the `translations.py` file in your app files and replace the `TRANSLATIONS` dict with the relevant values for your app.
  - This is how the TRANSLATIONS dict is structured: `{language_key:{page_key:{component_id.component_prop:component_translated_value}`
    - For example: {"en": {"math":{"calculate.children":"Calculate!"}} (link) would be the children text in English for the `html.Button` with `id="calculate"`, which is in the page `math` (link).
  - To indicate in the layout that a certain property is going to be translated, we `from translations import translated_item` and then indicate it as part of the relevant argument with this logic: `DashComponent(id=component_id, children=translated_item(component_id.component_property)`.
    - So, following the previous example, we would write: `html.Button(id="calculate", children=translated_item("calculate.children")`.
    - The value passed to `translated_item()` is the same as the key we have included in the `TRANSLATIONS` dict.
  - By default, translated_item will get the information of the current page and look automatically at the appropriate item key.
    - For example, if we are in `page='math'` and the saved language is `'en'` (English), the function will automatically look at `TRANSLATIONS['en']['math']`.
    - The only exception is the elements in `app.layout`, since they are in the "parent" ywe'll need to explicitly indicate `page='app'` (link to example)
  - There's also a `translated_page` function that is used only in the callback that uses the language dropdown as Input. It automatically updates the language of all elements on the current page, as long as they have been included in the TRANSLATIONS dict.
    - This happens because what this callback does is iterate over the `TRANSLATIONS` dict (link to the callback).
- Since we are using `flask.session`, this will need to be defined after the app object is created: 
```
server = app.server
server.secret_key = os.environ.get('FLASK_SECRET_KEY', b'123456abcdef') # random string prefixed by b so it's bytes
```
- `text_to_translate()` is a function that you should use in cases where you would typically just return a component whose children is a string that's part of a bigger component, if that string needs to be translated.
  - `text_to_translate()` takes a new component id as argument (remember to include the relevant reference in TRANSLATIONS) and it creates a `html.Span()`.
  - Following the case of the previous point if, instead of a string value you want to pass a dict of values because the options are multiple, we can do so by using the `multiple=True` and `multiple_key` arguments, like in this example: 
```
contents = html.Span([
    text_to_translate('math-output-text'),
    text_to_translate('operation-text', multiple=True, multiple_key=operation),
    ": ",
    str(result) # this is a number, so it doesn't require translation
])
```

- In a "single-language" app we would simply do return `f"Result of the {operation}: {value}"`. This is the equivalent in a multi-language app.

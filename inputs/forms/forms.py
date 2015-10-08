try:
    from BeautifulSoup import BeautifulSoup, SoupStrainer
except ImportError:
    from bs4 import BeautifulSoup, SoupStrainer

def get_form_inputs(html):
    inputs = set()
    for input in BeautifulSoup(html, parse_only=SoupStrainer('input')):
        d = { 'type' : input['type'] }
        if input.has_attr('name'): d['name'] = input['name']
        inputs.add(frozenset(d.items()))

    return inputs
from page import PageCollection
from inputs.forms.forms import get_form_inputs
from urllib.parse import urlparse, urlunsplit, urljoin

try:
    from BeautifulSoup import BeautifulSoup, SoupStrainer
except ImportError:
    from bs4 import BeautifulSoup, SoupStrainer 

def crawl(session, start_url, pages):
    can_url = urlparse(start_url)

    todo = set()

    todo.add(start_url)

    while len(todo) != 0:
        url = todo.pop()

        if 'logout' in url: continue # Terribly hacky wany to make fuzzer not log itself out

        page, created = pages.get_or_create(url)

        if (created or url not in page.aliases):
            crawl_page(session, can_url, url, todo, page)
    
    return

def crawl_page(session, can_url, url, todo, page):
    print ("Crawling " + url)
    page.add_alias(url)
    req = session.get(url)

    print("\t" + req.url)

    soup = BeautifulSoup(req.text, 'html.parser')


    for link in soup.find_all('a'):
        if link.has_attr('href'):
            dest = urljoin(url, link['href'])
            href = urlparse(dest)
            if href.netloc != '' and href.netloc != can_url.netloc: continue
            if href.path == '.': continue

            if dest not in todo:
                todo.add(dest)
    
    page.form_inputs.update(get_form_inputs(soup))
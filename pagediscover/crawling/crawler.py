from urllib.parse import urlparse, urlunsplit, urljoin

try:
    from BeautifulSoup import BeautifulSoup, SoupStrainer
except ImportError:
    from bs4 import BeautifulSoup, SoupStrainer 

def crawl(session, start_url):
    can_url = urlparse(start_url)

    todo = set()
    done = set()

    todo.add(start_url)

    while len(todo) != 0:
        url = todo.pop()
        done.add(url)
        crawl_page(session, can_url, url, done, todo)
    
    return done

def crawl_page(session, can_url, path, done, todo):
    url = path
    req = session.get(url)
    for link in BeautifulSoup(req.text, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            dest = urljoin(url, link['href'])
            href = urlparse(dest)
            if href.netloc != '' and href.netloc != can_url.netloc: continue
            if href.path == '.': continue

            if dest not in todo and dest not in done:
                todo.add(dest)
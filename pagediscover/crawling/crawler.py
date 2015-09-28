from urllib.parse import urlparse

try:
    from BeautifulSoup import BeautifulSoup, SoupStrainer
except ImportError:
    from bs4 import BeautifulSoup, SoupStrainer 

link_re = re.compile(r'href="(.?)"')

def crawl(session, start_url, results=set()):
    can_url = urlparse(start_url)

    todo = set()
    todo.add(can_url.path)

    while len(todo) != 0:
        url = todo.pop()
        results.add(url)
        crawl_page(session, can_url.netloc, url, results, todo)
    
    return results

def crawl_page(session, host, path, done, todo):
    req = session.get(host + url)
    for link in BeautifulSoup(req.text, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            href = urlparse(link['href'])
            if href.netloc != host: continue

            if href.path not in todo and href.path not in done:
                todo.add(href.path)
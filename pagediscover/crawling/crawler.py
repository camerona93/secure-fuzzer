try:
    from BeautifulSoup import BeautifulSoup, SoupStrainer
except ImportError:
    from bs4 import BeautifulSoup, SoupStrainer 

link_re = re.compile(r'href="(.?)"')

def crawl(session, url, results=set()):
    todo = set()
    todo.add(url)

    while len(todo) != 0:
        url = todo.pop()
        results.add(url)
        crawl_page(session, url, results, todo)
    
    return results

def crawl_page(session, url, done, todo):
    req = session.get(url)
    for link in BeautifulSoup(req.text, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            href = link['href']
            if href not in todo and href not in done:
                todo.add(href)
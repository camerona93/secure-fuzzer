import re

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
    links = link_re.findall(req.text)
    for link in links:
        link = urlparse.urljoin(url, link)
        if link not in todo and link not in done:
            todo.add(link)

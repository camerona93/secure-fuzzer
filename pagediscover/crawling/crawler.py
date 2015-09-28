import re

link_re = re.compile(r'href="(.?)"')

def crawl(session, url, maxlevel, results=set()):
    if (maxlevel == 0):
        return
    req = session.get(url)
    links = link_re.findall(req.text)
    for link in links:
        link = urlparse.urljoin(url, link)
        results = results.union(crawl(link, maxlevel - 1))

    return results
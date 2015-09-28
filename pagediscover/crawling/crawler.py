import re

link_re = re.compile(r'href="(.?)"')

def crawl(session, url, maxlevel):
    if (maxlevel == 0):
        return
    req = session.get(url)
    result = []
    links = link_re.findall(req.text)
    for link in links:
        link = urlparse.urljoin(url, link)
        result += crawl(link, maxlevel - 1)

    return result

stuff = crawl("http://127.0.0.1:8080/bodgeit/", 3)
print(stuff)
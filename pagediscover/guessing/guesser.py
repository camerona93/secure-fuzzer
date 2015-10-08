import requests
from pagediscover.crawling import crawl

notfound_codes = (requests.codes.no_response, requests.codes.not_found)
common_ext = { '', '.html', '.htm', '.xhtml', '.php', '.jsp', '.asp', '.aspx', '.xml', '.pl', '.do', '.cgi', '.txt' }

def guess(session, base_url, word_list, pages):
    if base_url[-1] != '/': base_url += '/'

    baselive, baseurl = is_live(session, base_url)
    if baselive: crawl(session, base_url, pages)

    for word in word_list:
        word = word.rstrip()
        for ext in common_ext:
            live, url = is_live(session, base_url + word + ext)
            #if live: print(url + ' ' + str(url in found))
            if live: crawl(session, url, pages)
#end def

def is_live(session, url):
    "Checks a url for liveness. Returns tuple of reachable, and the URL (in case of redirect)"
    # print('Checking ' + url, end=' ... ')
    r = session.get(url)
    # print(r.status_code)
    return (r.status_code not in notfound_codes), r.url
#end def
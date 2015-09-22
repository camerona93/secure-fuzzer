import requests

notfound_codes = (requests.codes.no_response, requests.codes.not_found)
common_ext = { '', '.html', '.htm', '.xhtml', '.php', '.jsp', '.asp', '.aspx', '.xml', '.pl', '.do', '.cgi', '.txt' }

def guess(base_url, word_list, found=set()):
    if base_url[-1] != '/': base_url += '/'
    for word in word_list:
        for ext in common_ext:
            live, url = is_live(base_url + word + ext)
            #if live: print(url + ' ' + str(url in found))
            if live and url not in found: found.add(url)

    return found
#end def

def is_live(url):
    "Checks a url for liveness. Returns tuple of reachable, and the URL (in case of redirect)"
    # print('Checking ' + url, end=' ... ')
    r = requests.get(url)
    # print(r.status_code)
    return (r.status_code not in notfound_codes), r.url
#end def
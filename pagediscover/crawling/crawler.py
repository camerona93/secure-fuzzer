#from requests.auth import HTTPBasicAuth
import re
import urllib.request
import urllib.error
import requests


'''
linkArray= []
boolean Auth = True

def grabRequstOfSite(url):
    if (Auth == True):
        if (url == 'http://127.0.0.1/dvwa/login.php'):
            urlRequest = requests.get(url, auth=('admin','password'))
        else if (url == 'http://127.0.0.1:8080/bodgeit/'):
            urlRequest = requests.get(url, auth=('admin','password'))
    else:
        pass;
    indexURL = url;
    return urlRequest
'''


def crawl(url,maxlevel):
    link_re =re.compile(r'href="(.?)"')
    if (maxlevel==0):
        return
    req = requests.get(url)
    result=[]
    links = link_re.findall(req.text)
    for link in links:
        link = urlparse.urljoin(url,link)
        result += crawl(link, maxlevel-1)

    return result
    
    
    

stuff= crawl("http://127.0.0.1:8080/bodgeit/",3)
print(stuff)

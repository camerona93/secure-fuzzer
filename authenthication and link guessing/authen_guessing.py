#from requests.auth import HTTPBasicAuth
import re
from urllib.parse import urlparse

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

def crawl( session, maxLevel):
    link_re = re.compile(r'href="(.*?)"')
    urls=[]
    if (maxLevel == 0):
        return urls
    url = link_re.findall(session)
    for link in url:
        link = urlparse.urljoin(session,i)
        urls += crawl(link, maxLevel-1)
    
    
    return urls
    
    
'''        
def auth_On_Off():
    if (Auth == False):
        Auth = True
    else
        Auth = False;
    
'''

stuff = crawl('https://www.google.com/?gws_rd=ssl',2)
for i in stuff:
    print (i)

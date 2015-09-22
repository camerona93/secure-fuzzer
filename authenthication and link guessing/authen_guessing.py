from requests.auth import HTTPBasicAuth


def grabRequestOfSite( String url):
    if (url == 'http://localhost:8000/DPWA'):
        urlRequest = requests.get(url, auth=('admin','password'))
    else if (url == 'http://localhost:8000/bigot'):
        urlRequest = requests.get(url, auth=('admin','password'))
    else:
        pass
    return urlRequest

def linkSaver(String currentUrl, String indexUrl, Array linkArray):
    if(currentUrl != indexUrl):
        linkArray.append(currentUrl)
        

def main():
    linkArray[String]


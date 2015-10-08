from requests import Session
from timeit import default_timer as timer

class TestSession(Session):

    def request(self, method, url, params = None, data = None, headers = None, cookies = None, files = None, auth = None, timeout = None, allow_redirects = True, proxies = None, hooks = None, stream = None, verify = None, cert = None, json = None):
        start = timer()
        response = super().request(method, url, params, data, headers, cookies, files, auth, timeout, allow_redirects, proxies, hooks, stream, verify, cert, json)
        end = timer()

        elapsed = end - start
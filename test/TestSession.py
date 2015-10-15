from requests import Session
from datetime import datetime
import http

class TestSession(Session):
    def __init__(self, dos_delay, sensitive_list):
        self.dos_delay = dos_delay
        self.sensitive_list = sensitive_list
        return super().__init__()

    def request(self, method, url, params = None, data = None, headers = None, cookies = None, files = None, auth = None, timeout = None, allow_redirects = True, proxies = None, hooks = None, stream = None, verify = None, cert = None, json = None):
        start = datetime.utcnow()
        response = super().request(method, url, params, data, headers, cookies, files, auth, timeout, allow_redirects, proxies, hooks, stream, verify, cert, json)
        end = datetime.utcnow()

        elapsed = (end - start).total_seconds() * 1000
        if elapsed > self.dos_delay:
            print("!!! {url} has a potential DOS vulnerability ({time} ms)".format(url=response.url, time=round(elapsed)))

        self.check_for_sensitive(response.url, response)
        self.check_status_code(response.url, response)

        return response

    def check_for_sensitive(self, url, response):
        for entry in self.sensitive_list:
            if entry in response.text:
                print("!!! {url} exposed sensitive data '{data}'!".format(url=url, data=entry))

    def check_status_code(self, url, response):
        if response.status_code != http.client.OK:
            print("!!! {url} returned non-200 status {status} ({human})".format(url=url, status=response.status_code, human=http.client.responses[response.status_code]))
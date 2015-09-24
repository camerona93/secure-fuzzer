from requests.cookies import RequestsCookieJar

class MemoryCookieJar(RequestsCookieJar):
    "A cookiejar that remembers every cookie stored in it"
    def __init__(self, policy = None):
        self.memory = set()
        return super(MemoryCookieJar, self).__init__(policy)

    def set_cookie(self, cookie, *args, **kwargs):
        if cookie not in self.memory: self.memory.add(cookie)
        return super(MemoryCookieJar, self).set_cookie(cookie, *args, **kwargs)
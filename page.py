from urllib.parse import urlsplit, urlunsplit, parse_qs

class Page:
    '''Represents a page on a website. All urls should be absolute'''
    def __init__(self, url, **kwargs):
        self.url_parts = urlsplit(url)[1:3]
        self.url = urlunsplit(('', self.url_parts[0], self.url_parts[1], '', ''))

        self.url_inputs = set()
        self.form_inputs = set()
        self.aliases = set()

        r = super().__init__(**kwargs)
        return r

    def __hash__(self, **kwargs):
        return hash(self.url_parts)

    def __eq__(self, other):
        return self.url_parts == other.url_parts

    def add_alias(self, url):
        '''Records a link to this page, parsing out url inputs'''
        self.aliases.add(url)
        parts = urlsplit(url)
        self.url_inputs.update(parse_qs(parts.query).keys())

class PageCollection:
    def __init__(self, **kwargs):
        self.pages = {}
        return super().__init__(**kwargs)

    def get_or_create(self, url):
        url_parts = urlsplit(url)[1:3]
        
        created = False
        p = self.pages.get(url_parts)

        if p is None:
            p = Page(url)
            self.pages[url_parts] = p
            created = True

        return (p, created)

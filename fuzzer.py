import argparse, requests
from inputs.cookies.MemoryCookieJar import MemoryCookieJar
from pagediscover.guessing import guesser
from pagediscover import crawling
from page import PageCollection
from test.TestSession import TestSession

def t_or_f(arg):
    ua = str(arg).upper()
    if ua == 'TRUE'[:len(ua)]:
       return True
    elif ua == 'FALSE'[:len(ua)]:
       return False
    else:
       pass  #error condition maybe?

parser = argparse.ArgumentParser(description='Security fuzzer')

parser.add_argument('command', help='Fuzzer mode. Discover or Test', choices=('discover', 'test'))
parser.add_argument('url', help='URL to fuzz')
parser.add_argument('--custom-auth', help='Signal that the fuzzer should use hard-coded authentication for a specific application (e.g. dvwa). Optional',
                    choices=('dvwa','bodgeit'), dest='auth')
parser.add_argument('--common-words', help='Newline-delimited file of common words to be used in page guessing and input guessing. Required.',
                    required=True, dest='word_file')
parser.add_argument('--vectors', help='Newline-delimited file of common exploits to vulnerabilities. Required.',
                    dest='vectors_file')
parser.add_argument('--sensitive', help="Newline-delimited file data that should never be leaked. It's assumed that this data is in the application's database (e.g. test data), but is not reported in any response. Required.",
                    dest='sensitive_file')
parser.add_argument('--random',help='When off, try each input to each page systematically.  When on, choose a random page, then a random input field and test all vectors. Default: false.',
                    type=t_or_f, default=False)
parser.add_argument('--slow', help='Number of milliseconds considered when a response is considered "slow". Default is 500 milliseconds',
                    type=int, default=500)

def main():
    args = parser.parse_args()

    if args.command == 'test':
        assert args.vectors_file is not None
        assert args.sensitive_file is not None

    print('Fuzzing ' + args.url + ' ...')

    p = discover(args)
    if args.command == 'test':
        test(p, args)

def discover(args):
    print('DISCOVER')
    # set up session
    print('Creating Session...')
    session = requests.Session()
    session.cookies = MemoryCookieJar()

    if args.auth is not None: login(session, args.auth)

    pages = PageCollection()

    ### Try to discover linked-to pages here
    print('Crawling for links')
    crawling.crawl(session, args.url, pages)

    print('Trying to guess additional pages...')
    with open(args.word_file, 'rU') as wf:
        word_list = [x.strip('\n') for x in wf.readlines()]
    #end with
    
    guesser.guess(session, args.url, word_list, pages)

    found = pages.pages

    print('{n} accesible pages discovered:'.format(n=len(found)))
    for key in sorted(found):
        page = found[key]
        print("\t" + page.url)
        print("\t\tForm Inputs:")
        for i in page.form_inputs:
            print ("\t\t\t" + str(dict(i)));
        print("\t\tURL Inputs:")
        for i in page.url_inputs:
            print ("\t\t\t" + str(i));

    print('{n} cookies found:'.format(n=len(session.cookies.memory)))
    for cookie in session.cookies.memory:
        print("\t" + str(cookie))

    return list(found.values())
#end def

def test(pages, args):
    print('TEST')

    # set up session
    print('Creating Session...')
    with open(args.sensitive_file, 'rU') as f:
        sensitive = [x.strip('\n') for x in f.readlines()]

    session = TestSession(args.slow, sensitive)

    if args.auth is not None: login(session, args.auth)

    # TODO: Calls to fuzz tester here
    a = list(pages[0].aliases)[0]
    session.get(a)


def login(session, site):
    if site == 'dvwa':
        r = session.post('http://127.0.0.1/dvwa/login.php', {'username' : 'admin', 'password' : 'password', 'Login' : 'Login'})
        assert not r.url.endswith('login.php')
    elif site == 'bodgeit':
        # user1@thebodgeitstore.com = H:dvLUD:DI
        # admin@thebodgeitstore.com = ?yJxP?A=Kovsh6
        # test@thebodgeitstore.com = password
        r = session.post('http://127.0.0.1:8080/bodgeit/login.jsp', {'username' : 'admin@thebodgeitstore.com', 'password' : '?yJxP?A=Kovsh6'})

    assert r.status_code == requests.codes.okay
#end def

if __name__ == '__main__':
    main()
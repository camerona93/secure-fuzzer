import argparse, requests
from inputs.cookies.MemoryCookieJar import MemoryCookieJar
from pagediscover.guessing import guesser

parser = argparse.ArgumentParser(description='Security fuzzer')

parser.add_argument('command', help='Fuzzer mode. Discover or Test', choices=('discover', 'test'))
parser.add_argument('url', help='URL to fuzz')
parser.add_argument('--custom-auth', help='Signal that the fuzzer should use hard-coded authentication for a specific application (e.g. dvwa). Optional',
                    choices=('dvwa',), dest='auth')
parser.add_argument('--common-words', help='Newline-delimited file of common words to be used in page guessing and input guessing. Required.',
                    required=True, dest='word_file')

def main():
    args = parser.parse_args()

    print('Fuzzing ' + args.url + ' ...')

    # set up session
    print('Creating Session...')
    session = requests.Session()
    session.cookies = MemoryCookieJar()

    if args.auth is not None: login(session, args.auth)

    ### Try to discover linked-to pages here
    found = set()
    # found = crawl(session, ...)
    # found should be a set()

    print('Trying to guess additional pages...')
    with open(args.word_file, 'rU') as wf:
        found = guesser.guess(session, args.url, wf)
    #end with

    print('{n} accesible pages discovered:'.format(n=len(found)))
    for page in sorted(found):
        print("\t" + page)

    print

    print('{n} cookies found:'.format(n=len(session.cookies.memory)))
    for cookie in session.cookies.memory:
        print("\t" + str(cookie))
    
#end def


def login(session, site):
    if site == 'dvwa':
        r = session.post('http://127.0.0.1/dvwa/login.php', {'username' : 'admin', 'password' : 'password', 'Login' : 'Login'})
        assert not r.url.endswith('login.php')

    assert r.status_code == requests.codes.okay
#end def

if __name__ == '__main__':
    main()
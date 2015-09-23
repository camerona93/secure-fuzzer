import argparse, requests
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
    s = requests.Session()
    if args.auth is not None: login(s, args.auth)

    print('Trying to guess additional pages...')
    with open(args.word_file, 'rU') as wf:
        found = guesser.guess(s, args.url, wf)
        for f in found: print(f)
    
#end def


def login(session, site):
    if site == 'dvwa':
        r = session.post('http://127.0.0.1/dvwa/login.php', {'username' : 'admin', 'password' : 'password', 'Login' : 'Login'})
        assert not r.url.endswith('login.php')

    assert r.status_code == requests.codes.okay
#end def

if __name__ == '__main__':
    main()
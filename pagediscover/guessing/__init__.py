if __name__ == '__main__':
    "URL guesser test code"
    import guesser
    urls = { 'admin', 'ids_log', 'CHANGELOG', 'php.ini' }
    for g in guesser.guess('http://127.0.0.1/dvwa', urls):
        print(g)
from urllib2 import urlopen
from HTMLParser import HTMLParser

import sys

class ACTHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._is_p = False
        self._ip = None

    def handle_starttag(self, tag, attrs):
        if not self._ip and tag == 'p':
            self._is_p = True

    def handle_endtag(self, tag):
        if not self._ip and tag == 'p':
            self._is_p = False

    def handle_data(self, data):
        if not self._ip and self._is_p:
            if 'Your IP:' in data:
                self._ip = data[data.index(':')+1:].strip()

    def get_ip(self):
        return self._ip


def main():
    domain = sys.argv[1]
    token = sys.argv[2]
    ip = find_your_ip()
    update_your_ip(domain, token, ip)
    print '#' * 100


def find_your_ip():
    r = urlopen('http://portal.acttv.in/web/chn/home')
    parser = ACTHTMLParser()
    parser.feed(r.read())
    return parser.get_ip()


def update_your_ip(domain, token, ip):
    url = 'https://www.duckdns.org/update?domains=%s&token=%s&ip=%s' % (domain, token, ip)
    print url
    r = urlopen(url)
    print r.read()

if __name__ == '__main__':
    main()
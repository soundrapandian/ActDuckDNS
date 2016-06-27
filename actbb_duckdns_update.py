from optparse import OptionParser
from urllib2 import urlopen
from HTMLParser import HTMLParser


class ACTHTMLParser(HTMLParser):
    """
    HTML Parser to get IP from portal.actbb.com
    """
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
    """
    Takes domain and token from arg
    Finds your current IP
    Updates it to DuckDNS
    :return: Nothing... None
    """
    token = None
    domain = None
    parser = OptionParser()
    parser.add_option('-d', '--domain', dest='domain', help='DuckDNS Domain')
    parser.add_option('-t', '--token', dest='token', help='DuckDNS Token')
    (options, args) = parser.parse_args()
    for opt_key, opt_value in options:
        if opt_key == 'domain':
            domain = opt_value
            continue
        if opt_key == 'token':
            token = opt_value
            continue

    ip = find_your_ip()
    if token and domain and ip:
        update_your_ip(domain, token, ip)
    else:
        print 'Token %s or Domain %s or IP %s is invalid. Not updated in duckDNS' % (token, domain, ip)
    print '#' * 100


def find_your_ip():
    """
    Finds IP from portal.acttv.in portal
    :return: IP
    """
    r = urlopen('http://portal.acttv.in/')
    parser = ACTHTMLParser()
    parser.feed(r.read())
    return parser.get_ip()


def update_your_ip(domain, token, ip):
    """
    Updates IP to DuckDNS
    :param domain: DuckDNS domain
    :param token: DuckDNS token
    :param ip: Your IP address
    :return: Nothing
    """
    url = 'https://www.duckdns.org/update?domains=%s&token=%s&ip=%s' % (domain, token, ip)
    print url
    r = urlopen(url)
    print r.read()


if __name__ == '__main__':
    main()

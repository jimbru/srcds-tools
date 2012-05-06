#!/usr/bin/python
#
# logproxy.py
#
# Service to forward srcds logs to a web server. Listens on a UDP port for log
# input in the style of the HLStatsX module. Collects log lines and transmits
# them in batches over HTTP POSTs to a web server.
# -jimbru
#

from socket import *
import sys
from urllib import urlencode
from urllib2 import urlopen

INTERFACE = ''  # all avaliable interfaces
PORT = 27500    # default hlstatsx port

# Runs the proxy.
# @param port 16-bit int indicating which port to listen for logs on.
# @param uri  The URL of the web server to post logs to.
def run_proxy(port, url):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind( (INTERFACE, port) )

    while True:
        data, addr = sock.recvfrom(1024)
        print '%s %s' % (addr, data),
        response = urlopen(url, urlencode({'q': data}))


def print_usage():
    print 'Usage: %s [port] uri' % sys.argv[0]


def main():
    argc = len(sys.argv)

    if argc < 2 or argc > 3:
        print_usage()
        sys.exit(1)
    elif argc == 2:
        run_proxy(PORT, sys.argv[1])
    else:
        run_proxy(int(sys.argv[1]), sys.argv[2])


if __name__ == '__main__':
    main()


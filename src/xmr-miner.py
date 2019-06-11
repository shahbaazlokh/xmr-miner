
import argparse
import os
import signal
import sys
import time
import urllib.request

from miner import miner

def init():
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    print('*** xmr-miner ***\n')
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help = 'remote configuration file - eg. https://pastebin.com/raw/TeXtFiLe (required, if not url given)')
    parser.add_argument('-o', '--url', help = 'mining pool - eg: stratum+tcp://mining.pool.com:3333 (required, if not file given)')
    parser.add_argument('-u', '--username', default = '', help = 'username or wallet address (required, if not file given)')
    parser.add_argument('-p', '--password', default = '', help = 'password (optional)')
    parser.add_argument('-v', '--variant', default = '4', help = 'pow variant (default = 4 [March 2019 CryptoNightR hard fork])')
    parser.add_argument('-t', '--threads', default ='1', help = 'mining threads (default = 1)')
    parser.add_argument('-d', '--debug', action='store_true')
    options = parser.parse_args(sys.argv[1:])
    if (options.url and options.username) or (options.file):
        if options.file:
            while True:
                try:
                    with urllib.request.urlopen(options.file) as config:
                        options.url = config.readline().decode().rstrip('\n').rstrip('\r')
                        options.username = config.readline().decode().rstrip('\n').rstrip('\r')
                        options.password = config.readline().decode().rstrip('\n').rstrip('\r')
                        options.variant = config.readline().decode().rstrip('\n').rstrip('\r')
                        options.threads = config.readline().decode().rstrip('\n').rstrip('\r')
                    if options.url == '' or options.username == '':
                        print('Wrong configuration file! Try with help (-h) before proceed.')
                        input('Press ENTER to quit...')
                        os._exit(1)
                    break
                except:
                    print('Trying to download configuration file. Please wait...')
                    time.sleep(10)
        if not options.url.startswith('stratum+tcp://'):
            options.url = 'stratum+tcp://' + options.url
        try:
            int(options.variant)
            if int(options.variant) > 4:
                options.variant = 4
        except:
            options.variant = 4
        try:
            int(options.threads)
        except:
            options.threads = 1
        m = miner()
        m.start(options)
    else:
        parser.print_help()
        print('\n')
        print('  remote configuration file formatting:')
        print('  [example with line numbers]:')
        print('  1  URL         mining pool - eg: stratum+tcp://mining.pool.com:3333 (required)')
        print('  2  USERNAME    username or wallet address (required)')
        print('  3  PASSWORD    password (optional)')
        print('  4  VARIANT     pow variant (default = 4 [March 2019 CryptoNightR hard fork])')
        print('  5  THREADS     mining threads (default = 1)')
        print('\n')
        input('Press ENTER to quit...')
        os._exit(1)

def quit(signum, frame): 
    os._exit(0)

if __name__ == '__main__':
    init()

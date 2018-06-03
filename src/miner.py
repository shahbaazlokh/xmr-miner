
import os
import signal
import threading
import time

from urllib.parse import urlparse
from client import client

class miner(object):
    
    def __init__(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        self.hostname = ''
        self.port = 0
        self.username = ''
        self.password = ''
        self.variant = 0
        self.threads = 0
        self.submitted_shares = 0
        self.accepted_shares = 0
        self.debug = False
        self.client = None
        self.hashrate = None

    def start(self, options):
        self.hostname = urlparse(options.url).hostname
        self.port = urlparse(options.url).port
        self.username = options.username
        self.password = options.password
        self.variant = int(options.variant)
        self.threads = int(options.threads)
        if options.debug:
            self.debug = True
        self.client = []
        self.hashrate = []
        for t in range(self.threads):
            self.client.append(client())
            self.hashrate.append(0)
            thread = threading.Thread(target=self.client[t].connect, args=(self, t))
            thread.daemon = True
            thread.start()
        while True:
            time.sleep(10)

    def stop(self, signum, frame): 
        for t in range(self.threads):
            self.client[t].disconnect(self, t)
        print('Quitting...')
        os._exit(0)
        time.sleep(3)

    def get_hashrate(self):
        try:
            total_hashrate = sum(self.hashrate)
            if total_hashrate >= 1000000000:
                return '%.3f Ghashes/s' % (total_hashrate / 1000000000)
            elif total_hashrate >= 1000000:
                return '%.3f Mhashes/s' % (total_hashrate / 1000000)
            elif total_hashrate >= 1000:
                return '%.3f khashes/s' % (total_hashrate / 1000)
            else:
                return '%.3f hashes/s' % total_hashrate
        except:
            return '%.3f hashes/s' % 0

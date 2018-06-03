
import binascii
import ctypes
import math
import os
import struct
import time

class job(object):
    
    def __init__(self):
        self.subscription_id = None
        self.job_id = None
        self.blob = None
        self.target = None
        self.nonce = None
        self.result = None
        self.dt = None
        self.hashcount = 0
        self.done = False

    def mine(self, client, miner, thread): 
        if client.message is not None:
            if 'params' in client.message:
                self.subscription_id = client.message['params']['id']
                self.job_id = client.message['params']['job_id']
                self.blob = client.message['params']['blob']
                self.target = client.message['params']['target'].encode('utf-8')
                self.target = b''.join([self.target[i:i+2] for i in range(0, len(self.target), 2)][::-1])
            else:
                self.subscription_id = client.message['result']['job']['id']
                self.job_id = client.message['result']['job']['job_id']
                self.blob = client.message['result']['job']['blob']
                self.target = client.message['result']['job']['target'].encode('utf-8')
                self.target = b''.join([self.target[i:i+2] for i in range(0, len(self.target), 2)][::-1])
        else:
            return
        print('[Thread #' + str(thread + 1) + '] Working on new job ID ' + self.job_id + '... Difficulty is ' + str(self.get_difficulty()))
        if os.name == 'nt':
            pow = ctypes.cdll.LoadLibrary(os.getcwd() + '/cryptonight.dll').cryptonight
        else:
            pow = ctypes.cdll.LoadLibrary(os.getcwd() + '/cryptonight.so').cryptonight 
        pow.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.c_int, ctypes.POINTER(ctypes.c_char), ctypes.c_int, ctypes.c_int]
        blob_bin = binascii.unhexlify(self.blob)
        t0 = time.time()
        for nonce in range(0x00000000, 0x7fffffff, 0x00000001):
            if self.done: 
                break
            nonce_bin = struct.pack('>I', nonce)
            input_bin = blob_bin[:39] + nonce_bin + blob_bin[39+len(nonce_bin):]
            output_bin = ctypes.create_string_buffer(32)
            pow(input_bin, 76, output_bin, miner.variant, 0)
            output = binascii.hexlify(output_bin)
            tar = output[-len(self.target):]
            tar = b''.join([tar[i:i+2] for i in range(0, len(tar), 2)][::-1])
            if tar <= self.target:
                self.nonce = '{0:0{1}x}'.format(nonce, 8)
                self.result = output.decode('utf-8')
                self.dt = time.time() - t0
                self.done = True
            self.hashcount += 1
        miner.hashrate[thread] = self.get_hashrate()

    def get_hashrate(self):
        if self.dt > 0:
            hashrate = self.hashcount / self.dt
        else:
            hashrate = 0
        return hashrate

    def get_difficulty(self):
        if int(self.target, 16) > 0:
            return math.floor((2**32 - 1) / int(self.target, 16))
        else:
            return 'undefined'

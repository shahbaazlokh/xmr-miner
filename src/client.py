
import binascii
import ctypes
import json
import socket
import time

from job import job

class client(object):
 
	def __init__(self):
		self.socket = None
		self.message_id = 0
		self.request = ''
		self.reply = ''
		self.message = None
		self.error = False
		self.job = None

	def connect(self, miner, thread):
		while True:
			if not self.error:
				print('[Thread #' + str(thread + 1) + '] Connecting to ' + miner.hostname + ':' + str(miner.port) + '...')
			else:
				print('[Thread #' + str(thread + 1) + '] Timeout occurred. Reconnecting to ' + miner.hostname + ':' + str(miner.port) + '...')
			self.error = False
			try:
				self.socket = socket.create_connection((miner.hostname, miner.port))
				self.socket.settimeout(3)
			except:
				self.error = True
				time.sleep(10)
				continue
			self.handle_login(miner, thread)

	def handle_login(self, miner, thread):
		while True:
			if self.error:
				break
			if self.message_id > 0:
				self.message_id += miner.threads
			else:
				self.message_id = thread + 1
			self.message = {}
			self.message['jsonrpc'] = '2.0'
			self.message['id'] = self.message_id
			self.message['method'] = 'login'
			self.message['params'] = {}
			self.message['params']['login'] = miner.username
			self.message['params']['pass'] = miner.password
			self.message['params']['agent'] = 'xmr-miner'
			self.request = self.json_encode(self.message)
			if miner.debug:
				print('\n[Thread #' + str(thread + 1) + '] Sending message #' + str(self.message_id) + ':')
				print(self.request)
			try:
				self.socket.send(str.encode(self.request))
				rid_1 = '"id": ' + str(self.message_id) + ','
				rid_2 = '"id":' + str(self.message_id) + ','
				rid_3 = '"id" : ' + str(self.message_id) + ','
				rid_4 = '"id" :' + str(self.message_id) + ','
				while True:
					self.reply = self.socket.recv(4096).decode()
					if rid_1 in self.reply or rid_2 in self.reply or rid_3 in self.reply or rid_4 in self.reply:
						break
			except:
				self.error = True
				break
			if miner.debug:
				print('[Thread #' + str(thread + 1) + '] Receiving message #' + str(self.message_id) + ':')
				print(self.reply)
			if not self.reply.startswith('{') or not self.reply.endswith('\n'):
				self.reply = ''
			if self.reply.count('\n') > 1:
				self.reply = self.reply.split('\n')[0]
			if 'job_id' in self.reply:
				self.handle_job(miner, thread)
			else:
				print('[Thread #' + str(thread + 1) + '] Invalid credentials or malformed job message! Retrying...')
				time.sleep(10)

	def handle_job(self, miner, thread):
		while True:
			self.message = self.json_decode(self.reply)
			self.job = job()
			self.job.mine(self, miner, thread)
			print('[Thread #' + str(thread + 1) + '] Done! Total hashrate is ' + miner.get_hashrate())
			self.message_id += miner.threads
			self.message = {}
			self.message['jsonrpc'] = '2.0'
			self.message['id'] = self.message_id
			self.message['method'] = 'submit'
			self.message['params'] = {}
			self.message['params']['id'] = self.job.subscription_id
			self.message['params']['job_id'] = self.job.job_id
			self.message['params']['nonce'] = self.job.nonce
			self.message['params']['result'] = self.job.result
			self.request = self.json_encode(self.message)
			if miner.debug:
				print('\n[Thread #' + str(thread + 1) + '] Sending message #' + str(self.message_id) + ':')
				print(self.request)
			try:
				self.socket.send(str.encode(self.request))
				rid_1 = '"id": ' + str(self.message_id) + ','
				rid_2 = '"id":' + str(self.message_id) + ','
				rid_3 = '"id" : ' + str(self.message_id) + ','
				rid_4 = '"id" :' + str(self.message_id) + ','
				while True:
					self.reply = self.socket.recv(4096).decode()
					if rid_1 in self.reply or rid_2 in self.reply or rid_3 in self.reply or rid_4 in self.reply:
						break
			except:
				self.error = True
				break
			if miner.debug:
				print('[Thread #' + str(thread + 1) + '] Receiving message #' + str(self.message_id) + ':')
				print(self.reply)
			miner.submitted_shares += 1
			if not self.reply.startswith('{') or not self.reply.endswith('\n'):
				self.reply = ''
			if self.reply.count('\n') > 1:
				self.reply = self.reply.split('\n')[0]				
			if 'OK' in self.reply:
				miner.accepted_shares += 1
			print('[Thread #' + str(thread + 1) + '] Result sent! Accepted ' + str(miner.accepted_shares) + ' of ' + str(miner.submitted_shares) + ' total shares.')
			break

	def disconnect(self, miner, thread):
		if self.socket is not None:
			print('[Thread #' + str(thread + 1) + '] Disconnecting from ' + miner.hostname + ':' + str(miner.port) + '...')
			self.socket.close()

	def json_encode(self, object):
		try:
			return json.dumps(object) + '\n'
		except:
			return ''
 
	def json_decode(self, string):
		try:
			return json.loads(string)
		except:
			return None

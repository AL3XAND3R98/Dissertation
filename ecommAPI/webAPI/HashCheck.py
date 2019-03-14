import uuid
import hashlib
import json
import base64
import os
from math import *

class HashCheck:
	def __init__(self):

		self.salt = "EEM!eiv*9ezxf3@Y%3kK@@dDZyfDAo"
		self.salt2 = "hUCx&mbEiy1uw78BBWKF^C2bdcAjeIaPV6@5BVRDFX!E8UAku7"

	def gen_nonce(self, length):
		""" Generates a random string of bytes, base64 encoded """
		return uuid.uuid4().hex + uuid.uuid1().hex
	def hashText(self, text):
		"""
			Basic hashing function for a text using random unique salt.  
		"""
		text = json.dumps(text, indent=4, sort_keys=True)
		hash = hashlib.sha256(self.salt.encode() + text.encode()).hexdigest() 
		print(hash)
		return(hash)

	def hashCookie(self, text):
		"""
			Basic hashing function for a text using random unique salt.  
		"""
		text = str(text)
		nonce = self.gen_nonce(12)
		print(nonce)
		hash = hashlib.sha256(self.salt2.encode() + text.encode()+ nonce.encode()).hexdigest() 
		print(hash)
		return(hash)
		
	def checkHash(self, hashToVerify, dataToHash):
		print("checkHashdataToHash::"+json.dumps(dataToHash, indent=4, sort_keys=True))
		dataToHash = json.dumps(dataToHash, indent=4, sort_keys=True)
		hashCheck = hashlib.sha256(self.salt.encode() + dataToHash.encode()).hexdigest()
		print("checkHashHashCheck::"+hashCheck)
		if hashCheck == hashToVerify:
			return True
		else:
			return False
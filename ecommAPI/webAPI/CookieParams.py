import uuid
import json
import requests
import rsa
from .HashCheck import *
'''{
	"session_id":"",
	"user_ip":"",
	"user_userAgent":"",
	"user_deviceOrientation"
	"user_innerHeight":"",
	"user_innerWidth":"",
	"user_innerHTML":"",
	"user_touchEvent":"",
	"user_buttonTouch":"",
	"user_keyDown":"",
	"user_mouseDown":"",
	"user_accelleration":"",
	"user_locale":"",
	"user_timeZone":"",
	"user_selenium":{"user_cdc":,"user_wdc":,"user_seleniumKW":},
	"user_product":"",
	"user_hash"
}'''

'''https://www.blacklistmaster.com/apiv0#blacklistcheck'''

'''big issue is loads of people making random data and senbding that, therefore will compute a hash of the data'''

class CookieParams:
	def __init__(self, jsonData):

		with open('private.pem', mode='rb') as privatefile:
			keydata = privatefile.read()
			self.privkey = rsa.PrivateKey.load_pkcs1(keydata)
	
		self.jsonData = jsonData
		self.session_id = self.getString(jsonData['session_id'])
		self.ip = self.getString(jsonData['user_ip'])
		self.ua = self.getString(jsonData['user_userAgent'])
		self.deviceOrientation = self.getString(jsonData['user_deviceOrientation'])
		self.innerHeight = self.getString(jsonData['user_innerHeight'])
		self.innerWidth = self.getString(jsonData['user_innerWidth'])
		self.innerHTML = self.getString(jsonData['user_innerHTML'])
		self.touchEvent = self.getString(jsonData['user_touchEvent'])
		self.buttonTouch = self.getString(jsonData['user_buttonTouch'])
		self.mouseDown = self.getString(jsonData['user_mouseDown'])
		self.keyDown = self.getString(jsonData['user_keyDown'])
		self.accelleration = self.getString(jsonData['user_accelleration'])
		self.timeZone = self.getString(jsonData['user_timeZone'])
		self.locale = self.getString(jsonData['user_locale'])
		self.selenium = jsonData['user_selenium']
		self.cdc = self.getString(self.selenium['user_cdc'])
		self.seleniumKW = self.getString(self.selenium['user_seleniumKW'])
		self.wdc = self.getString(self.selenium['user_wdc'])
		self.product = self.getString(jsonData['user_product'])
		self.hashVal = jsonData['user_hashVal']

	def getString(self, cipher):
		print("CIPHER"+cipher)
		plain= rsa.decrypt(bytes.fromhex(str(cipher)), self.privkey).decode('utf-8')
		print(plain)
		return plain

	def ipCheck(self):

		'''response = requests.get('https://www.blacklistmaster.com/restapi/v0/blacklistcheck/ip/'+self.ip, auth=('ec16159', 'apiEC16159'))
		jsonRes = json.loads(response.text)
		print(jsonRes)
		status = jsonRes['status']
		if status=="Not blacklisted":
			return True
		else:
			return False'''

		return True


	def uaCheck(self):

		#response = requests.get('http://www.useragentstring.com/?uas='+str(self.ua.encode(encoding='UTF-8'))+'&getJSON=all', auth=('ec16159', 'apiEC16159'))
		#jsonRes = json.loads(response.text)
		#print(jsonRes)
		#status = jsonRes['agent_name']
		#if status=="unknown":
			#return False
		#else:
		return True

	def browserCheck(self):
		
		if self.deviceOrientation=="LS" or self.deviceOrientation=="PT" and int(self.innerHeight)>150 and int(self.innerWidth)>100 and self.str2bool(self.innerHTML):
			return True
		else:
			return False

	def str2bool(self, v):
	  return v.lower() in ("yes", "true", "t", "1")

	def seleniumCheck(self):
		

		if (not self.str2bool(self.cdc)) and (not self.str2bool(self.cdc)) and (not self.str2bool(self.seleniumKW)):
			return True
		else:
			return False

	def usageCheck(self):

		if int(self.keyDown)>5 and int(self.buttonTouch)>=1 and self.str2bool(self.touchEvent) and int(self.mouseDown)>=1 and float(self.accelleration)>0.5:
			return True
		else:
			return False

	def productCheck(self):

		if self.product:
			return True
		else:
			return False

	def localeCheck(self):

		if self.locale=="en_GB" and self.timeZone=="CET":
			return True
		else:
			return False

	def hashCheck(self):
		data = {
			"session_id":self.session_id,
			"user_ip":self.ip,
			"user_userAgent":self.ua,
			"user_deviceOrientation":self.deviceOrientation,
			"user_innerHeight":self.innerHeight,
			"user_innerWidth":self.innerWidth,
			"user_innerHTML": self.innerHTML,
			"user_touchEvent":self.touchEvent,
			"user_buttonTouch":self.buttonTouch,
			"user_keyDown":self.keyDown,
			"user_mouseDown":self.mouseDown,
			"user_accelleration":self.accelleration,
			"user_locale":self.locale,
			"user_timeZone":self.timeZone,
			"user_selenium":
			{
				"user_cdc":self.cdc,
				"user_seleniumKW":self.seleniumKW,
				"user_wdc":self.wdc
			},
			"user_product":self.product
		}
		print("InsideCookiePCheck::"+json.dumps(data, indent=4, sort_keys=True))
		return HashCheck().checkHash(self.hashVal, data)

	def generateCookie(self):
		return HashCheck().hashCookie(self.jsonData)

'''
data = {
	"session_id":" ",
	"user_ip":"89.36.68.198",
	"user_userAgent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
	"user_deviceOrientation":" ",
	"user_innerHeight":" ",
	"user_innerWidth":" ",
	"user_innerHTML":" ",
	"user_touchEvent":" ",
	"user_buttonTouch":" ",
	"user_keyDown":" ",
	"user_mouseDown":" ",
	"user_accelleration":" ",
	"user_locale":" ",
	"user_timeZone":" ",
	"user_selenium":{"user_cdc":False,"user_wdc":False,"user_seleniumKW":False},
	"user_product":" ",
}
hashVal = HashCheck().hashText(data)
data = {
	"session_id":" ",
	"user_ip":"89.36.68.198",
	"user_userAgent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
	"user_deviceOrientation":" ",
	"user_innerHeight":" ",
	"user_innerWidth":" ",
	"user_innerHTML":" ",
	"user_touchEvent":" ",
	"user_buttonTouch":" ",
	"user_keyDown":" ",
	"user_mouseDown":" ",
	"user_accelleration":" ",
	"user_locale":" ",
	"user_timeZone":" ",
	"user_selenium":{"user_cdc":False,"user_wdc":False,"user_seleniumKW":False},
	"user_product":" ",
	"user_hashVal":hashVal
}
print(CreateCookie(data).hashCheck())'''
import pandas
import numpy
import uuid
import requests
import json

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

		self.jsonData = jsonData
		self.session_id = jsonData['session_id']
		self.ip = jsonData['user_ip']
		self.ua = jsonData['user_userAgent']
		self.deviceOrientation = jsonData['user_deviceOrientation']
		self.innerHeight = jsonData['user_innerHeight']
		self.innerWidth = jsonData['user_innerWidth']
		self.innerHTML = jsonData['user_innerHTML']
		self.touchEvent = jsonData['user_touchEvent']
		self.buttonTouch = jsonData['user_buttonTouch']
		self.mouseDown = jsonData['user_mouseDown']
		self.keyDown = jsonData['user_keyDown']
		self.accelleration = jsonData['user_accelleration']
		self.timeZone = jsonData['user_timeZone']
		self.locale = jsonData['user_locale']
		self.selenium = jsonData['user_selenium']
		self.product = jsonData['user_product']
		self.hashVal = jsonData['user_hashVal']

	def ipCheck(self):

		response = requests.get('https://www.blacklistmaster.com/restapi/v0/blacklistcheck/ip/'+self.ip, auth=('ec16159', 'apiEC16159'))
		jsonRes = json.loads(response.text)
		print(jsonRes)
		status = jsonRes['status']
		if status=="Not blacklisted":
			return True
		else:
			return False


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
		
		if self.deviceOrientation=="LS" or self.deviceOrientation=="PT" and self.innerHeight>150 and self.innerWidth>100 and self.innerHTML:
			return True
		else:
			return False


	def seleniumCheck(self):
		
		if (not self.selenium['user_cdc']) and (not self.selenium['user_cdc']) and (not self.selenium['user_seleniumKW']):
			return True
		else:
			return False

	def usageCheck(self):

		if self.keyDown>5 and self.buttonTouch>=1 and self.touchEvent and self.mouseDown>=1 and self.accelleration>0.5:
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
			"user_selenium":self.selenium,
			"user_product":self.product
		}
		print(data)
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
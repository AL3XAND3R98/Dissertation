from django.test import TestCase
import json

import rsa

with open('private.pem', mode='rb') as privatefile:
	keydata = privatefile.read()
	privkey = rsa.PrivateKey.load_pkcs1(keydata)

with open('public.pem', mode='rb') as privatefile:
	keydata = privatefile.read()
	pubkey = rsa.PublicKey.load_pkcs1(keydata)


with open('public.pem', mode='rb') as privatefile:
   keydata = privatefile.read()
   pubkey = rsa.PublicKey.load_pkcs1(keydata)






message = {  
   "user_deviceOrientation":rsa.encrypt("PT".encode('utf-8'), pubkey).hex(),
   "user_buttonTouch":rsa.encrypt("3".encode('utf-8'), pubkey).hex(),
   "user_mouseDown":rsa.encrypt("8".encode('utf-8'), pubkey).hex(),
   "user_ip":rsa.encrypt("89.36.68.198".encode('utf-8'), pubkey).hex(),
   "session_id":rsa.encrypt("889d64e0-93fc-4db3-9b18-81919bb5bd1d".encode('utf-8'), pubkey).hex(),
   "user_innerHTML":rsa.encrypt("true".encode('utf-8'), pubkey).hex(),
   "user_innerWidth":rsa.encrypt("150".encode('utf-8'), pubkey).hex(),
   "user_keyDown":rsa.encrypt("10".encode('utf-8'), pubkey).hex(),
   "user_hashVal":"3cbcbe16c003ccf41c8bad1849ef88f3c582bbf0ad96a851d04f07bb17d2b659",
   "user_product":rsa.encrypt(" ".encode('utf-8'), pubkey).hex(),
   "user_userAgent":rsa.encrypt("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0".encode('utf-8'), pubkey).hex(),
   "user_accelleration":rsa.encrypt("0.6".encode('utf-8'), pubkey).hex(),
   "user_selenium":{  
      "user_cdc":rsa.encrypt("false".encode('utf-8'), pubkey).hex(),
      "user_wdc":rsa.encrypt("false".encode('utf-8'), pubkey).hex(),
      "user_seleniumKW":rsa.encrypt("false".encode('utf-8'), pubkey).hex()
   },
   "user_touchEvent":rsa.encrypt("true".encode('utf-8'), pubkey).hex(),
   "user_timeZone":rsa.encrypt("CET".encode('utf-8'), pubkey).hex(),
   "user_innerHeight":rsa.encrypt("250".encode('utf-8'), pubkey).hex(),
   "user_locale":rsa.encrypt("en_GB".encode('utf-8'), pubkey).hex(), 
}

cipher=rsa.encrypt("PT".encode('utf-8'), pubkey).hex()
print(rsa.decrypt(bytes.fromhex(cipher), privkey).decode('utf-8'))





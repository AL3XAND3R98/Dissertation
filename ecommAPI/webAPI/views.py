from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse, JsonResponse, QueryDict, Http404
import json
from django.views.decorators.csrf import csrf_exempt
from .CookieParams import *
from .HashCheck import *
from django.utils import timezone
from .models import BDetect as BDetectCookie, Product, Basket  # Import the model classes we just wrote.
import datetime 
import pytz
import uuid


utc=pytz.UTC


def index(request):

	return render(request, "index.html")


def listProducts(request):
	products = {'Products': 
		[dict(product) for product in list(Product.objects.values())] 
	}
	print(products)
	return JsonResponse(products)

def getProductHelper(pid):
	print(pid)
	productObject = Product.objects.get(productID = pid)
	print(productObject)
	productJSON = {
		"productID":productObject.productID,
		"productName":productObject.productName,
		"productDesc":productObject.productDesc,
		"productStock":productObject.productStock
	}
	return productJSON, productObject

def getProduct(request, pid):
	try:
		productJSON, product =getProductHelper(pid)
		return JsonResponse(productJSON, safe=False)
	except:
		raise Http404("No produ matches the given query.")


def getCartHelper(bid):
	cart = Basket.objects.get(basketID = bid)
	cartJSON = {
		"basketID":cart.basketID,
		"basketItem":cart.basketItem.productName,
		"basketQty":cart.basketQty,
		"basketTotal":cart.basketTotal,
		"basketExpiry":cart.basketExpiry
	}
	return cartJSON, cart

def getCart(request, basketID):
	print("hi")
	try:
		cartJSON, cart = getCartHelper(basketID)
	except:
		raise Http404("No cart matches the given query.")

	if(cart.basketID):
		print(cartJSON)
		return JsonResponse(cartJSON, safe=False)
	else:
		return JsonResponse({"success":False})



@csrf_exempt
def addToCart(request):
	if isValidCookieHelper(request):
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		_basketID = uuid.uuid4()
		_product = body['productID']
		_qty = body['qty']
		try:
			productJSON, productObj = getProductHelper(_product)
			if(productObj.productStock>_qty):
			
				productObj.productStock=int(productObj.productStock-_qty)
				productObj.save()
				now = datetime.datetime.now()
				now_plus_10 = now + datetime.timedelta(minutes = 10)
				newBasket = Basket(basketExpiry=now_plus_10, basketItem=productObj, basketQty=_qty, basketTotal=_qty*productObj.productPrice)
				newBasket.save()

				if newBasket.basketID:
					productJSON, productObj = getProductHelper(_product)
					cartJSON, cart = getCartHelper(newBasket.basketID)
					return JsonResponse(cartJSON, safe=False)
				else:
					return JsonResponse({"success":False})
			else:
					return JsonResponse({"success":False, "message":"Quantity Not Available"})
		except:
			raise Http404("No Product Found.")

	else:
		return JsonResponse({"Message":403})

def isValidCookieHelper(request):
	cookieVal = request.COOKIES['BDetect']
	print(cookieVal)
	try:
		cookie_object = BDetectCookie.objects.get(cookie_value = cookieVal)

		print(cookie_object.cookie_value)
		if cookie_object:
			present = utc.localize(datetime.datetime.now())
			cookie_expiration = cookie_object.cookie_expiration
			print(cookie_expiration)
			if(cookie_expiration>present):
				return True
		return False

	except Exception as E:
		print(E)
		return False

def isValidCookie(request):
	cookieVal = request.COOKIES['BDetect']
	try:
		cookie_object = BDetectCookie.objects.get(cookie_value = cookieVal)

		print(cookie_object.cookie_value)
		if cookie_object:
			present = utc.localize(datetime.datetime.now())
			cookie_expiration = cookie_object.cookie_expiration
			print(cookie_expiration)
			if(cookie_expiration>present):
				return JsonResponse({'success': True})
		return JsonResponse({'success': False})

	except Exception as E:
		print(E)
		return JsonResponse({'success': False})



@csrf_exempt
def setCookie(request):

	body_unicode = request.body.decode('utf-8')
	body = json.loads(body_unicode)
	try:
		user_ip = body['user_ip']
	except:
		return JsonResponse({"message":"Failed Parsing Cookie Data"})


	print("PRE HASH::"+json.dumps(body,indent=4, sort_keys=True))


	hashVal = HashCheck().hashText(body)
	print("Hashed Value::"+hashVal)


	dataHashed = {
		"session_id":body["session_id"],
		"user_ip":body["user_ip"],
		"user_userAgent":body["user_userAgent"],
		"user_deviceOrientation":body['user_deviceOrientation'],
		"user_innerHeight":body['user_innerHeight'],
		"user_innerWidth":body['user_innerWidth'],
		"user_innerHTML":body['user_innerHTML'],
		"user_touchEvent":body['user_touchEvent'],
		"user_buttonTouch":body['user_buttonTouch'],
		"user_keyDown":body['user_keyDown'],
		"user_mouseDown":body['user_mouseDown'],
		"user_accelleration":body['user_accelleration'],
		"user_locale":body['user_locale'],
		"user_timeZone":body['user_timeZone'],
		"user_selenium":body['user_selenium'],
		"user_product":body['user_product'],
		"user_hashVal":hashVal
	}
	print("POST HASH::"+json.dumps(dataHashed, indent=4, sort_keys=True))

	CookieDataCheck = CookieParams(dataHashed)


	if(CookieDataCheck.hashCheck()):
		print("Cookie Data Integrity")
		print("Checking Cookie Data...")
		if(CookieDataCheck.ipCheck()):
			print("IP Good")
			if(CookieDataCheck.uaCheck()):
				print("UA Good")
				if(CookieDataCheck.browserCheck()):
					print("Browser Good")
					if(CookieDataCheck.seleniumCheck()):
						print("Selenium Good")
						if(CookieDataCheck.usageCheck()):
							print("Usage Good")
							if(CookieDataCheck.localeCheck()):
								print("Locale Good")

								BDetect = CookieDataCheck.generateCookie()
								response = JsonResponse({"message":"Setting BDetect Cookie to %s!" % BDetect})
								now = datetime.datetime.now()
								now_plus_10 = now + datetime.timedelta(minutes = 15)
								cookieRow = BDetectCookie(cookie_value=BDetect, cookie_expiration=now_plus_10)
								cookieRow.save()
								if cookieRow.id:
									response.set_cookie('BDetect', BDetect)
									print("Cookie Set")
									cookies = {'products': 
										[dict(cookie) for cookie in list(BDetectCookie.objects.values())] 
									}
									print(cookies)
							else:
								print("Failed Locale Check")
						else:
							print("Failed Usage Check")
					else:
						print("Failed Selenium Check")
				else:
					print("Failed Browser Check")					
			else:
				print("Failed UA Check")									
		else:
			print("Failed IP Check")
	else:
		print("Failed Integrity Check")

	return response
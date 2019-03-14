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
from querystring_parser import parser as qsparser


utc=pytz.UTC
def index(request):

	return render(request, "index.html")

def showProduct(request, pid):
	productJSON, product = getProductHelper(pid)
	return render(request, "productPage.html", productJSON)

def showCart(request, basketID):
	cartJSON, cart = getCartHelper(basketID)
	return render(request, "showCart.html", cartJSON)

def listProducts(request):
	products = {'Products': 
		[dict(product) for product in list(Product.objects.values())] 
	}
	return JsonResponse(products)

def getProductHelper(pid):
	productObject = Product.objects.get(productID = pid)
	print("Retrieved::"+str(productObject))
	productJSON = {
		"productID":productObject.productID,
		"productName":productObject.productName,
		"productDesc":productObject.productDesc,
		"productPrice":productObject.productPrice,
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
	productJSON, productObject = getProductHelper(cart.basketItem.productID)
	cartJSON = {
		"basketID":cart.basketID,
		"basketItem":productJSON,
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
		try:
			query_string_as_dict = qsparser.parse(body_unicode)
			body = json.dumps(query_string_as_dict,indent=4, sort_keys=True)
		except:
			body = body_unicode

		body = json.loads(body)
		_basketID = uuid.uuid4()
		_product = body['productID']
		_qty = int(body['qty'])
		print("Adding "+_product)


		try:
			productJSON, productObj = getProductHelper(_product)
		except:
			return JsonResponse({"success":False, "Message":"Product Not Found"}, status=404)

		print("Product found...")
		try:
			if(productObj.productStock>=_qty):
				productObj.productStock=int(productObj.productStock-_qty)
				productObj.save()
				print(productObj.productStock)
				now = datetime.datetime.now()
				now_plus_10 = now + datetime.timedelta(minutes = 10)
				newBasket = Basket(basketExpiry=now_plus_10, basketItem=productObj, basketQty=_qty, basketTotal=_qty*productObj.productPrice)
				newBasket.save()

				if newBasket.basketID:
					productJSON, productObj = getProductHelper(_product)
					cartJSON, cart = getCartHelper(newBasket.basketID)
					return JsonResponse(cartJSON, safe=False, status=201)
				else:
					return JsonResponse({"success":False}, status=409)
			else:
				print("HIIIII")
				return JsonResponse({"success":False, "message":"Quantity Not Available"}, status=202)
		except:
			return JsonResponse({"success":False, "message":"Server Error"}, status=500)


	else:
		return JsonResponse({"Message":"ACCESS DENIED"}, status=290)

def isValidCookieHelper(request):
	try:
		cookieVal = request.COOKIES['BDetect']
	except:
		return False
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
	try:
		query_string_as_dict = qsparser.parse(body_unicode)
		print("QUERY")
		print(str(query_string_as_dict))
		body = json.dumps(query_string_as_dict,indent=4, sort_keys=True)
	except:
		body = body_unicode


	body = json.loads(body)
	user_ip= body['user_ip']

	user_hashVal = body['user_hashVal']
	print("SET COOKIE PRE HASH::"+json.dumps(body,indent=4, sort_keys=True))
	
	print("ClientSide Hashed Value::"+str(user_hashVal))

	CookieDataCheck = CookieParams(body)

	response = JsonResponse({"success":False})

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
									response.set_cookie('BDetect', BDetect, max_age=900)
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
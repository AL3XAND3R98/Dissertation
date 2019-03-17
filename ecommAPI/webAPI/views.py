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


#################################################################################################################################
 
def index(request):
	return render(request, "index.html") 						#renders index.html

def showProduct(request, pid):
	productJSON, product = getProductHelper(pid) 				#get's product details
	return render(request, "productPage.html", productJSON) 	#renders productPage.html

def showCart(request, basketID):
	cartJSON, cart = getCartHelper(basketID) 					#get's cart details
	return render(request, "showCart.html", cartJSON) 			#renders showCart.html

#################################################################################################################################



#################################################################################################################################

def listProducts(request):
	products = {'Products': 
		[dict(product) for product in list(Product.objects.values())] 		#Fetch all products from database and store in JSON
	}
	return JsonResponse(products)											#Return Product list

#################################################################################################################################



#################################################################################################################################

def getProductHelper(pid):
	productObject = Product.objects.get(productID = pid) 	#gets product object from database, search by PID
	print("Retrieved::"+str(productObject))
	productJSON = {											#store in readable JSON format
		"productID":productObject.productID,
		"productName":productObject.productName,
		"productDesc":productObject.productDesc,
		"productPrice":productObject.productPrice,
		"productStock":productObject.productStock
	} 											
	return productJSON, productObject						#return productJSON and the productObject

#################################################################################################################################





#################################################################################################################################

def getProduct(request, pid):
	try:
		productJSON, product = getProductHelper(pid)			#get productJSON from helper method
		return JsonResponse(productJSON, safe=False)			#return productJSON as json response to client
	except:
		raise Http404("No product matches the given query.")

#################################################################################################################################










#################################################################################################################################################################

@csrf_exempt 
def addToCart(request):
	
	if isValidCookieHelper(request):													#Check BDetect Cookie is Valid
		body_unicode = request.body.decode('utf-8') 									#Decode body to utf-8
		try:
			query_string_as_dict = qsparser.parse(body_unicode)							#Parse query string to dict
			body = json.dumps(query_string_as_dict,indent=4, sort_keys=True)			#Convert dict to json object
		except:
			body = body_unicode															#If above fails assume JSON body sent 

		try:
			body = json.loads(body)
			_basketID = uuid.uuid4()
			_product = body['productID']
			_qty = int(body['qty'])
		except:
			return JsonResponse({"success":False, "Message":"Bad Request - Malformed Data"}, status=400) 	#If above fails data is malformed, return to client

		try:
			productJSON, productObj = getProductHelper(_product)
		except:
			return JsonResponse({"success":False, "Message":"Product Not Found"}, status=404)				#If above fails product is not in db, return to client

		try:
			if(productObj.productStock>=_qty):																#Check enough stock is available
				productObj.productStock=int(productObj.productStock-_qty)						
				productObj.save()																			#Update DB with new stock qty of product
				print(productObj.productStock)												
				now = datetime.datetime.now()
				now_plus_10 = now + datetime.timedelta(minutes = 10)										#Set Basket Expiry to 10 minutes from now
				newBasket = Basket(basketExpiry=now_plus_10, basketItem=productObj, basketQty=_qty, basketTotal=_qty*productObj.productPrice)
				newBasket.save()																			#Save new Basket in DB

				if newBasket.basketID:																		#Check basket was properly saved
					cartJSON, cart = getCartHelper(newBasket.basketID)	
					return JsonResponse(cartJSON, safe=False, status=201)									#Return 201 - basket created - with cartJSON as body
				else:
					return JsonResponse({"success":False}, status=409)										#Return 500 - Server error - Basket was not created
			else:	
				return JsonResponse({"success":False, "message":"Quantity Not Available"}, status=202)		#Return 202 - request accepted - qty not avail
		except:
			return JsonResponse({"success":False, "message":"Server Error"}, status=500)					#Return 500 - server error

	else:
		return JsonResponse({"Message":"ACCESS DENIED"}, status=403)										#Return 403 - cookie not valid - deny access

#####################################################################################################################################################################







##############################################################################################################################################################

def getCartHelper(bid):
	cart = Basket.objects.get(basketID = bid)											#gets basket object from database, search by BasketID		
	productJSON, productObject = getProductHelper(cart.basketItem.productID)			#gets product object from helper
	cartJSON = {																		#store basket in readable JSON
		"basketID":cart.basketID,
		"basketItem":productJSON,
		"basketQty":cart.basketQty,
		"basketTotal":cart.basketTotal,
		"basketExpiry":cart.basketExpiry	
	}
	return cartJSON, cart 																#return cartJSON and cartObject

##############################################################################################################################################################



##############################################################################################################################################################

def getCart(request, basketID):
	try:
		cartJSON, cart = getCartHelper(basketID)										#get cartJSON and cart object from helper method
	except:
		raise Http404("No cart matches the given query.")								#if above fails return 404 cart not found

	if(cart.basketID):
		return JsonResponse(cartJSON, safe=False)										#if basketID present return cartJSON as response
	else:
		return JsonResponse({"success":False})											#else return false›

##############################################################################################################################################################





##############################################################################################################################################################

def isValidCookieHelper(request):
	try:
		cookieVal = request.COOKIES['BDetect'] 											#get BDetect Cookie from client session
	except:
		return False 																	#cookie not present - return False
	print(cookieVal)
	try:
		cookie_object = BDetectCookie.objects.get(cookie_value = cookieVal)				#Lookup cookie in db

		if cookie_object:																#cookie value found in db
			present = utc.localize(datetime.datetime.now())								#current time
			cookie_expiration = cookie_object.cookie_expiration							#cookie expiry time
			if(cookie_expiration>present):												#check if expired
				return True
		return False

	except Exception as E:
		print(E)
		return False

##############################################################################################################################################################




##############################################################################################################################################################

def isValidCookie(request):
	
	cookieValid = isValidCookieHelper(request)			#check if cookie is valid with helper method
	return JsonResponse({'success': cookieValid})

##############################################################################################################################################################





##############################################################################################################################################################

@csrf_exempt
def setCookie(request):

	response = JsonResponse({"success":False})

	body_unicode = request.body.decode('utf-8')									#Decode body to utf-8					
	try:
		query_string_as_dict = qsparser.parse(body_unicode)						#Parse query string to dict
		body = json.dumps(query_string_as_dict,indent=4, sort_keys=True)		#Convert dict to json object
	except:
		body = body_unicode														#If above fails assume JSON body sent 


	try:
		body = json.loads(body)
		user_ip= body['user_ip']
		user_hashVal = body['user_hashVal']
	except:
		return JsonResponse(response)
	
	CookieDataCheck = CookieParams(body)
	

	if(CookieDataCheck.hashCheck()):
		if(CookieDataCheck.ipCheck()):
			if(CookieDataCheck.uaCheck()):
				if(CookieDataCheck.browserCheck()):
					if(CookieDataCheck.seleniumCheck()):
						if(CookieDataCheck.usageCheck()):
							if(CookieDataCheck.localeCheck()):			
								BDetect = CookieDataCheck.generateCookie()											#Verify Data values are accepted
								response = JsonResponse({"message":"Setting BDetect Cookie to %s!" % BDetect})			
								now = datetime.datetime.now()
								now_plus_10 = now + datetime.timedelta(minutes = 15)
								cookieRow = BDetectCookie(cookie_value=BDetect, cookie_expiration=now_plus_10)
								cookieRow.save()																	#Save Cookie value to DB
								if cookieRow.id:					
									response.set_cookie('BDetect', BDetect, max_age=900)							#Set cookie on clientside 
							
			
																													#return response to client
	return response

##############################################################################################################################################################


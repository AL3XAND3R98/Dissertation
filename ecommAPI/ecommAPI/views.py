from django.shortcuts import redirect
#################################################################################################################################
 
def index(request):
	return redirect('/storefront/') 						#renders index.html
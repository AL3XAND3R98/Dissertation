from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('setCookie/', views.setCookie, name='setCookie'),
    path('listProducts/', views.listProducts, name='listProducts'),
    path('isValid/', views.isValidCookie, name='isValid'),
    path('availability/<str:pid>/', views.getProduct, name='getProduct'),
    path('product/<str:pid>/', views.showProduct, name='productPage'),
    path('addToCart/', views.addToCart, name='addToCart'),
    path('getCart/<str:basketID>/', views.getCart, name='getCart'),
    path('showCart/<str:basketID>/', views.showCart, name='showCart'),

]
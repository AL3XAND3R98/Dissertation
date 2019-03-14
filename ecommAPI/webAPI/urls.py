from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/setCookie/', views.setCookie, name='setCookie'),
    path('api/listProducts/', views.listProducts, name='listProducts'),
    path('api/isValid/', views.isValidCookie, name='isValid'),
    path('api/availability/<str:pid>/', views.getProduct, name='getProduct'),
    path('product/<str:pid>/', views.showProduct, name='productPage'),
    path('api/addToCart/', views.addToCart, name='addToCart'),
    path('api/getCart/<str:basketID>/', views.getCart, name='getCart'),
    path('showCart/<str:basketID>/', views.showCart, name='showCart'),

]
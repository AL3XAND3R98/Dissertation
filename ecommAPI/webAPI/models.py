from django.db import models
import uuid
# Create your models here.

#################################################################################################################################################################

class BDetect(models.Model):
	cookie_value = models.CharField(max_length=200)
	cookie_expiration = models.DateTimeField('Cookie Expiration')

#################################################################################################################################################################

#################################################################################################################################################################

class Product(models.Model):

	productName = models.CharField(max_length=100)
	productID = models.CharField(primary_key=True, max_length=6)
	productDesc = models.TextField()
	productPrice = models.DecimalField(max_digits=6, decimal_places=2)
	productStock = models.PositiveIntegerField()

	def _str_(self):
		return self.productName

#################################################################################################################################################################

#################################################################################################################################################################

class Basket(models.Model):

	basketID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	basketExpiry = models.DateTimeField('Basket Expiration')
	basketItem = models.ForeignKey(Product, on_delete=models.CASCADE)
	basketQty = models.PositiveIntegerField()
	basketTotal = models.DecimalField(max_digits=8, decimal_places=2)

	def _str_(self):
		return self.basketID
	
#################################################################################################################################################################
	
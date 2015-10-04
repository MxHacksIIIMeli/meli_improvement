from django.db import models

class Product(models.Model):
	des_product = models.CharField(max_length=500)
	def __str__(self):
		return self.des_product
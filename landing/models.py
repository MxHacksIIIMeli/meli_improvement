from django.db import models

class Product(models.Model):
	des_product = models.CharField(max_length=500)
	avg_price = models.FloatField(default=0)
	def __str__(self):
		return self.des_product
		return self.avg_price
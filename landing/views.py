from django.shortcuts import render
from django.http import HttpResponse
from .forms import Search
import urllib.request
import json
from .models import Product

# Create your views here.
def login(request):
	return render(request, 'landing/login.html')

def index(request):
	form = Search()
	prices = []
	if request.method == 'GET':
		q = request.GET.get('q', None)
		url = "https://api.mercadolibre.com/sites/MLM/search?q={}".format(q.replace(' ', '%20'))
		print("*" * 20)
		print(url)
		print("*" * 20)
		with urllib.request.urlopen(url) as response: data = response.read()
		string_url = data.decode(encoding='UTF-8')
		resp = json.loads(string_url)
		length = len(resp['results'])
		print(length)
		for i in range(0, length):
			prices.append(resp['results'][i]['price'])

		average_price = sum(prices)/len(prices)
		print(average_price)
		p = Product(des_product=q, avg_price=average_price)
		p.save()
		return render(request, 'landing/index.html', {'form': form, 'precio': average_price})
	else:
		return render(request, 'landing/index.html', {'form': form})
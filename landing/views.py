from django.shortcuts import render
from django.http import HttpResponse
from .forms import Search
import urllib2
import json

# Create your views here.
def login(request):
	return render(request, 'landing/login.html')

def index(request):
	form = Search()
	prices = []
	if request.method == 'GET':
		q = request.GET.get('q', None)
		url = "https://api.mercadolibre.com/sites/MLM/search?q={}".format(q.replace(' ', '%20'))
		print "*" * 20
		print url
		print "*" * 20
		data = urllib2.urlopen(url).read()
		resp = json.loads(str(data))
		for i in range(len(resp['results'])):
			prices.append(resp['results'][i]['price'])
		average_price = sum(prices)/len(prices)
		print average_price
	return render(request, 'landing/index.html', {'form': form})
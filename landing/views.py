from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .forms import Search
import urllib.request
import json
from . import preguntas_mercadolibre
from .models import Product

# Create your views here.
def login(request):
	return render(request, 'landing/login.html')

def index(request):
	prices = []
	if request.method == 'GET':
		form = Search()
		q = request.GET.get('q', None)
		if (q is not None) and (q != ""):
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
			return render(request, 'landing/index.html', {'form': form, 'precio': average_price})
	elif request.method == 'POST':
		form = Search()
		return render(request, 'landing/index.html', {'form': form})
	form = Search()
	return render(request, 'landing/index.html', {'form': form})

def bot(request):
	print(preguntas_mercadolibre.obtener_respuestas())
	return render(request, 'landing/preguntas.html')
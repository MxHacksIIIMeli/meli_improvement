from django.shortcuts import render
from django.http import HttpResponse
from .forms import Search
import urllib2

# Create your views here.
def login(request):
	return render(request, 'landing/login.html')

def index(request):
	form = Search()
	if request.method == 'GET':
		q = request.GET.get('q', None)
		url = "https://api.mercadolibre.com/sites/MLM/search?q={}".format(q.replace(' ', '%20'))
		data = urllib2.urlopen(url)
		print type(data)
	return render(request, 'landing/index.html', {'form': form})
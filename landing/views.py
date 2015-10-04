from django.shortcuts import render
from django.http import HttpResponse
from .forms import Search

# Create your views here.
def login(request):
	return render(request, 'landing/login.html')

def index(request):
	form = Search()
	return render(request, 'landing/index.html', {'form': form})
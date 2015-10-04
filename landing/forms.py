from django import forms

class Search(forms.Form):
	your_search = forms.CharField(label='Busca un producto', max_length=250)
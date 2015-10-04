from django import forms

class Search(forms.Form):
	q = forms.CharField(label='Busca un producto', max_length=250, required=True)
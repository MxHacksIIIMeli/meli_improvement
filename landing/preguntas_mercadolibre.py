#!/usr/bin/python
# Mercadolibre: Respuesta automatica
# Ejecucion: python preguntas_mercadolibre.py 
# Date: 03-10-2015

# -------------------------------------------------------------------------------------
# ---------------------------- Librerias ----------------------------------------------
# -------------------------------------------------------------------------------------
# Llamadas al sistema
import os
import sys
# Expresiones regulares
import re
# Mercadolibre
import subprocess
sys.path.append("/home/oscar/Escritorio/AnswerBot/landing/lib/")
from meli import Meli
# JSON
import json
# NLTK
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
# unicode
import unicodedata

# -------------------------------------------------------------------------------------
# ---------------------------- Funciones ----------------------------------------------
# -------------------------------------------------------------------------------------

def pre_procesamiento(pregunta):
	pregunta = pregunta.lower()
	return ''.join((c for c in unicodedata.normalize('NFD', pregunta) if unicodedata.category(c) != 'Mn'))


def sustitucion_numero_letra(pregunta):
	pregunta_filtrada={}
	letras={'1':'i','2':'2','3':'e','4':'a','5':'s','6':'g','7':'7','8':'8','9':'9','0':'o'}
	for palabras in wordpunct_tokenize(pregunta):
		aux_str=""
		bandera_numero=False
		if(palabras.isdigit()):
			pregunta_filtrada[palabras]=palabras
		else:
			for x in palabras:
				if(x.isdigit()):
					aux_str=aux_str+letras[x]
				else:
					aux_str=aux_str+x
					bandera_numero=True
			pregunta_filtrada[palabras]=aux_str
	return pregunta_filtrada

#def corrector_ortografico(pregunta):


def eliminar_caracteres_basura(pregunta):
	return re.sub(r'[^\w| ]', '', pregunta)

def eliminar_stopwords(pregunta):
	excepciones={"no","sin"}
	pregunta = set(wordpunct_tokenize(pregunta))
	español_stopwords = set(stopwords.words("spanish"))
	excepciones = excepciones.intersection(pregunta)
	palabras_clave_oracion = pregunta.difference(español_stopwords)
	return palabras_clave_oracion.union(excepciones)

def reconstruccion_pregunta(pregunta,tags):
	oracion=[]
	if isinstance(tags, dict):
		for palabra in pregunta.split():
			if(tags[palabra]):
				oracion.append(tags[palabra])
		return oracion
	else:
		for palabra in pregunta.split():
			if palabra in tags:
				oracion.append(palabra)
		return oracion


def generar_respuesta(categorias_correspondientes,categorias_preguntas,info_producto):
	respuesta = ""
	for categoria in categorias_correspondientes:
		#print(categorias_preguntas[categoria]["respuestas"])
		for etiquetas in categorias_preguntas[categoria]["respuestas"]:
			#print(etiquetas)
			#print ("\n",info_producto,"\n")
			if etiquetas in info_producto:
				descripcion_pago = categorias_preguntas[categoria]["respuestas"][etiquetas]
				obtener_tokens={word:re.split('\(|\)|\,',word[1:]) for word in categorias_preguntas[categoria]["respuestas"][etiquetas].split() if word.startswith('$')}
				#print(obtener_tokens)
				for tokens in obtener_tokens:
					if(obtener_tokens[tokens][0]=="array"):
						aux_str=[]
						for precios in info_producto[obtener_tokens[tokens][1]]:
							aux_str.append(str(precios[obtener_tokens[tokens][2]]))
						obtener_tokens[tokens]=','.join(aux_str)
					else:
						obtener_tokens[tokens]=str(info_producto[obtener_tokens[tokens][0]])

					#print ("aux:",aux_str)
				if(obtener_tokens):
					aux = []
					for palabras in descripcion_pago.split():
						if palabras in obtener_tokens:
							if(palabras=="available_quantity" and obtener_tokens[palabras]==0):
								aux.append("por el momento no contamos con inventario")
							else:
								aux.append(obtener_tokens[palabras])
						else:
							aux.append(palabras)
					respuesta = respuesta +" ".join(aux)
				else:
					respuesta = respuesta +" "+descripcion_pago
	return "Buenos días, "+respuesta+" saludos."

def obtener_respuesta(tags_pregunta,info_producto):
	categorias_preguntas = {"pagos":{
								"tags":{"sin","intereses","pago","contraentrega","contra","entrega","tarjeta","oxxo","transferencia","mercadopago","pagos"},
								"respuestas":{ 	"accepts_mercadopago":"aceptamos mercadopago ",
												"non_mercado_pago_payment_methods":"aceptamos los siguientes metodos de pago: $array(non_mercado_pago_payment_methods,description) "
											}
								},
							"precio":{
						         "tags":{"precio","es","lo","menos"},
						         "respuestas":{"price":"el precio de nuestro producto $title es de $price $currency_id"}
						        },
						    "cambio":{
				                 "tags":{"haces","realizas","puedes","cambio","ofrezco"},
				                 "respuestas":{"cambio":"no realizo cambios, solo venta por el momento"}
								},
							"existencia":{
				                 "tags":{"existencia","cuentas","con","todavia","agotado","quedan"},
				                 "respuestas":{"available_quantity":"todavía cuento con $available_quantity disponible"}
				              	},
				            "estado":{
				                 "tags":{"nuevo","usado"},
				                 "respuestas":{   "condition":"El producto esta $condition"}
                                },
							"garantia"  :{
				                 "tags":{"garantia","tiempo"},
				                 "respuestas":{  "warranty":"el producto $title cuenta con una garantía de $warranty"}
                            	}
						}
	categorias_correspondientes = []
	categoria_conteo=0
	for categoria in categorias_preguntas:
		#print (categorias_preguntas[categoria]["tags"])
		#print (tags_pregunta)
		similitud = len(tags_pregunta.intersection(categorias_preguntas[categoria]["tags"]))
		#print(similitud)
		if(categoria_conteo<similitud and similitud!=0):
			categorias_correspondientes=[]
			categoria_conteo = similitud
			categorias_correspondientes.append(categoria)
		elif(categoria_conteo==similitud and similitud!=0):
			categorias_correspondientes.append(categoria)
	#print("categorias localizadas:",categorias_correspondientes)
	if(categoria_conteo!=0):
		return generar_respuesta(categorias_correspondientes,categorias_preguntas,info_producto)
	return ""


def respuesta_pregunta(respuesta):
	print (respuesta)
	"""body = {"question_id":respuesta[0],"text":respuesta[2]}
	responseAns = meli.post(path="/answers?access_token=APP_USR-6490405204826174-100404-3cdf65176efc7a83d86d08271279c4b2__F_G__-66153861", body=body)
	print(responseAns)"""

def atender_preguntas(listado_preguntas,descripcion_producto):
	preguntas=[]
	for x in listado_preguntas:
		if(x["status"]!="ANSWERED"):
			#print("Pregunta: ",x["text"],"\n")
			pregunta_guardar = x["text"]
			pregunta = pre_procesamiento(x["text"])
			pregunta = eliminar_caracteres_basura(pregunta)
			pregunta_carateres_numeros = sustitucion_numero_letra(pregunta)
			pregunta = reconstruccion_pregunta(pregunta,pregunta_carateres_numeros)
			pregunta = ' '.join(pregunta)
			palabras_clave_pregunta = eliminar_stopwords(pregunta)
			#palabras_clave_pregunta = reconstruccion_pregunta(pregunta,palabras_clave_pregunta)
			#print(palabras_clave_pregunta)
			#print("Respuesta: ",obtener_respuesta(palabras_clave_pregunta,descripcion_producto),"\n")
			preguntas.append({"question":pregunta_guardar,"answer":obtener_respuesta(palabras_clave_pregunta,descripcion_producto)})
	return preguntas

# -------------------------------------------------------------------------------------
# ---------------------------- Codigo principal ---------------------------------------
# -------------------------------------------------------------------------------------

# limpiado de consola
#os.system('clear')

def obtener_respuestas():
	#Sustituir por variables de sesion
	CLIENT_ID = 66153861
	CLIENT_SECRET = "ZAVALAELIZABETH82"
	ACCESS_TOKEN = "APP_USR-6490405204826174-100410-967a3eff52ab09b7f3c8ff195ec5c48e__I_E__-66153861"

	meli = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=ACCESS_TOKEN, refresh_token="Refresh_Token")

	#Funcion que crea lista de caracteristicas de objeto y de preguntas
	responseItems = meli.get(path="/users/66153861/items/search?access_token=APP_USR-6490405204826174-100410-967a3eff52ab09b7f3c8ff195ec5c48e__I_E__-66153861")
	idItems = responseItems.json()['results']
	respuestas_preguntas = []
	for id in idItems:
		responsCaracteristicas = meli.get(path="/items/?ids="+id)
		responseQuestion = meli.get(path="/questions/search?item="+id)
		
		#print(caracteristicas)	
		caracteristicas = responsCaracteristicas.json()[0]
		questions = responseQuestion.json()['questions']

		#print(questions)
		respuestas_preguntas.append({"product":caracteristicas,"question_answers":atender_preguntas(questions,caracteristicas)})
	return json.dumps(respuestas_preguntas)

#print(obtener_respuestas())
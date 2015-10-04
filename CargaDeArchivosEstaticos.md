Descargar los archivos de bootstrap o cualquier framework y guardarlos en un sus respectivos directorios(sean css o js) dentro de AnswerBot/landing/static. (Al final quedaría la ruta: AnswerBot/landing/static/css o 
AnswerBot/landing/static/js)
Añadir la siguiente linea a los archivos html en la parte superior: {% load staticfiles %}
Luego poner el href o src correspondiente: 
	<link type="text/css" rel="stylesheet" href="{% static 'css/materialize.css' %}">
	<script type="text/javascript" src="{% static 'js/jquery-1.9.1.js' %}"></script>

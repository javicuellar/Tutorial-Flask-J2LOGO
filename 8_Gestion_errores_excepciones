Lección 8: Gestión y manejo de errores y excepciones
Categoría: Flask
flask, medio, python, tutorial flask
Lección 8 Gestión de errores
Errores. Toda aplicación es susceptible a errores. Incluso aunque nuestro código sea perfecto, siempre puede haber algún bug en una librería de un tercero u ocurrir un fallo en la base de datos, en la red, en un servicio externo… Por eso es importante esta parte del tutorial.

En esta lección vamos a repasar una serie de conceptos básicos sobre manejo de errores y las herramientas que nos proporciona Flask para ello. Y es que es importantísimo de cara a nuestros usuarios que la aplicación sea lo más robusta posible, es decir, que al usuario se le presenten el mínimo número de errores. Da muy mala imagen que a un usuario se le muestre, por ejemplo, una traza de error o un mensaje como Error 500: Internal Server Error. Todo este tipo de cosas no deberían llegar a nuestros usuarios.

¿Estás list@ para saber cómo manejar los errores? ¡Comencemos! Pero antes, ¡recuerda! Este tutorial es la continuación de la Lección 7. Así que si te has despistado o no has seguido todas las lecciones del tutorial, puedes descargar el código por donde lo dejamos como te indico a continuación:

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 7 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion7 -b leccion7

Índice
Aquí tienes los puntos principales de esta lección:

Introducción
Qué sucede cuándo hay un error no controlado
abort
Manejadores de errores
Introducción
Como te decía al comienzo de este post, cualquier aplicación puede fallar en el momento más inesperado. Por mucho que nos esforcemos en programar teniendo en cuenta hasta el más mínimo detalle, los errores siempre pueden suceder. Entre los errores más típicos encontramos:

Errores de programación. Sí, el error más típico es que el código tenga un bug.
Errores al escribir en un fichero: el fichero ya existe, no hay permisos de escritura en un directorio, …
Errores de base de datos: de integridad, permisos, fallos de conexión, …
Errores al conectar con un servicio externo: permisos de acceso, indisponibilidad, errores de conexión, …
Como vemos, nunca sabemos cuándo, dónde ni cómo nuestra aplicación va a fallar. Por eso, lo mejor que podemos hacer es ponerle remedio en la medida de lo posible con las herramientas que nos facilita cada lenguaje de programación y cada framework. En nuestro caso, Python y Flask, respectivamente.

Qué sucede cuando hay un error no controlado
En el caso de una aplicación web, lo más común cuando ocurre un error no controlado es que al usuario se le muestre una página de error, acompañada de un código de estado HTTP. Estas páginas de error bien las sirve la propia aplicación, bien el servidor web en función del código de estado devuelto por la respuesta de la aplicación.

Los códigos de estado HTTP sirven para clasificar los posibles errores sucedidos durante el procesamiento de la petición HTTP. Entre los más comunes se encuentran:

200: La petición se procesó correctamente.
4xx: Hubo un problema relacionado con la petición. Normalmente relacionados con el cliente o el usuario.
5xx: Hubo un problema en la parte del servidor. Suelen ser fallos en la aplicación.
No es el propósito de este post hablar sobre los códigos de estado. Si quieres saber más puedes aprender sobre ello aquí.

Ejemplos de errores no controlados
Siguiendo con nuestro código del tutorial, imaginemos que tratamos de acceder a la página http://localhost:5000/contacto

Efectivamente, al acceder nos aparecerá un error indicando que la página no existe como el que muestro a continuación:

Errores: página no encontrada
Ahora vamos a añadir un poco de acción 😜 Abre el fichero public/routes.py y añade al final del todo la siguiente vista:

@public_bp.route("/error")
def show_error():
    res = 1 / 0
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)
El ejemplo es muy tonto, hace lo mismo que la función index() solo que he añadido un error a propósito: una división por cero. Como bien sabrás, esto produce una excepción en cualquier lenguaje de programación. Compruébalo tú mism@. Si ahora intentas acceder a http://localhost:5000/error, se mostrará la siguiente página:

Errores: división por cero
Realmente vemos esta página porque en su día configuramos la aplicación para arrancar con el modo DEBUG activo, dado que estamos en un entorno de desarrollo (local). El modo debug hace que veamos la traza completa del error.

Estos errores no se deberían mostrar al usuario, primero porque dan mala imagen y segundo porque damos pistas sobre nuestro código, lo que puede suponer un problema de seguridad

Si desactivamos el modo DEBUG y volvemos a acceder a la página anterior, veremos que en esta ocasión se nos muestra una página de error genérica:

Error 500
Los dos ejemplos anteriores muestran los casos de un error no controlado producido por el usuario (quiere acceder a una página que no existe) y un error no controlado producido por un bug en el código (división por cero). En las siguientes secciones veremos cómo podemos tratar estos errores para hacer que la aplicación sea robusta.

abort
Muchas veces, al programar, somos conscientes que el programa o la aplicación no puede continuar su ejecución porque hemos detectado una situación de error. En este caso, lo que tiene más sentido es interrumpir la ejecución e informar de ello al usuario.

En el caso de Flask contamos con la función abort(). Esta función detiene la ejecución de la petición de forma prematura y devuelve un código de estado HTTP permitido (el que le pasemos como parámetro).

Veámoslo con calma. Abre el fichero public/routes.py y fíjate en la función show_post():

@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("public/post_view.html", post=post)
En esta función, si no encontramos ningún post con el slug pasado como parámetro, no podemos mostrar la página del post, post_view.html. Por ello, es mejor detener la ejecución de la petición, indicando un código de estado 404 (No encontrado). Haz la prueba. Trata de acceder a un post que no exista. Verás de nuevo la página 404 Not Found 😩

Si modificáramos el código de estado y en su lugar establecemos el valor 400, al acceder, la página de error sería distinta. Mostraría el error 400 Bad Request.

❗️ Cuando manejes y/o gestiones las situaciones de error, utiliza la función abort() con el código de estado más apropiado a cada caso.

Manejadores de errores
Hasta aquí hemos visto que cuando sucede un error no controlado o ejecutamos la función abort(), al usuario se le muestra una página de error dependiente del código de estado devuelto por la petición. Sin embargo, estas páginas de error se pueden personalizar para que, por ejemplo, sigan el mismo estilo o plantilla que el resto de nuestra web. ¿Cómo podemos hacer esto? A través de los manejadores de errores.

Como su nombre indica, los manejadores de errores son funciones que se ejecutan cuando se produce una situación de error. Son muy útiles porque nos permiten hacer multitud de cosas cuando ocurre un error: escribir en un log, mostrar una página de error personalizada, añadir una cabecera a la respuesta, etc.

Hay dos formas de definir un manejador de error:

Decorando una función con errorhandler()
Registrando una función como errorhandler: app.register_error_handler(codigo_estado, funcion)
Se pueden manejar dos tipos de errores:

Códigos de estado HTTP conocidos
Excepciones
¿Qué quiere decir lo anterior? Hasta ahora habíamos visto que para detener la ejecución de una petición e informar de un error hacíamos uso de la función abort(). No obstante, también es posible lanzar una excepción y asociarla a un manejador de error.

Mejor veamos todo esto con un ejemplo, ¿no?

Páginas de error personalizadas
Abre el fichero app/__init__.py y añade al final del todo el siguiente código:

def register_error_handlers(app):
    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500
    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404
Añade también lo siguiente al final del método create_app(), justo antes del return app:

    ...
    from .public import public_bp
    app.register_blueprint(public_bp)
    # Custom error handlers
    register_error_handlers(app)
    return app
Como ves, lo que estamos haciendo es devolver páginas de error personalizadas para los errores 404 y 500.

¡OJO! En el manejador del error, además de indicar el nombre de la página a renderizar, se devuelve como segundo parámetro el código de estado (500 y 404, respectivamente). Recuerda añadirlos siempre.

Tan solo falta crearlas. Vamos a ello 💪🏻 Crea un fichero con nombre 404.html y otro llamado 500.html en el directorio app/templates/.

Abre el fichero 404.html y añade el siguiente código:

{% extends 'base_template.html' %}
{% block content %}
    Ooops!! La página que buscas no existe xD
{% endblock %}
Haz lo mismo con el fichero 500.html pero con este otro contenido:

{% extends 'base_template.html' %}
{% block content %}
    Ooops!! Parece que ha habido un error :(
{% endblock %}
Si ahora accedemos a un post que no existe, veremos nuestra página de error 404 personalizada:

Página error 404 personalizada
Por último y antes de terminar esta sección, recuerda que te he comentado que además de tratar códigos de estado HTTP también se pueden manejar excepciones. Vamos a actualizar la función show_post() como te muestro a continuación:

from werkzeug.exceptions import NotFound
@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        raise NotFound(slug)
    return render_template("public/post_view.html", post=post)
Como puedes ver, en esta ocasión, en lugar de llamar a la función abort con el código de estado 404, lanzamos la excepción NotFound que hereda de werkzeug.exceptions.HTTPException.

Al lanzarse la excepción, esta será manejada por el manejador definido por @app.errorhandler(404) ya que el código de estado y el código de cualquier excepción que herede de HTTPException son los mismos. Es decir, 404 = NotFound.code

Pero no solo podemos definir excepciones que hereden de HTTPException en los manejadores de errores. Podemos controlar cualquier excepción que nosotros queramos.

¡ATENCIÓN! No es una buena práctica registrar un manejador de error para la excepción Exception. Este manejador podría devolver un código de estado 500 para excepciones que hereden de HTTPException que no hayan sido controladas.

Conclusión
Bueno, hemos llegado al final de esta lección. Aquí te he mostrado los conceptos básicos sobre control de errores en una aplicación con Flask:

La importancia de comprender que cualquier aplicación es susceptible a fallos.
Hay que ocultar los errores internos de la aplicación a los usuarios.
Los errores se deben comunicar de forma amigable (con páginas de error, por ejemplo).
Uso de la función abort() para interrumpir una petición cuando se detecta un error con un código de estado. De forma alternativa se puede lanzar una excepción.
Cómo se definen manejadores de errores para tratar los casos de error de forma personalizada.
Tan solo queda que apliques todo esto en tu día a día y, ya sabes, si tienes cualquier duda, puedes consultarme dejándome un mensaje al final del post, por email o a través de mis redes sociales.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 8 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion8 -b leccion8

En el siguiente tutorial veremos cómo usar mensajes de log en Flask para conocer la traza de ejecución de la aplicación y registrar errores, de manera que podamos identificar bugs y corregirlos. Nos vemos.
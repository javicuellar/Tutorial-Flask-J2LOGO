Lección 15: Trabajar con Fechas en Flask
Categoría: Flask
flask, medio, python, tutorial flask
Lección 15 Trabajar con fechas en Flask
Las fechas son una parte delicada de muchas aplicaciones. Saber trabajar y operar con ellas es, por tanto, una tarea fundamental. En esta lección del tutorial vas a descubrir cómo manipular fechas en Flask para mostrarlas adecuadamente en tus plantillas JINJA2.

¿Deseando comenzar? ¡Vamos a ello! Pero antes, ¡recuerda! Esta lección es la continuación de la anterior, en la que vimos cómo enviar emails con Flask. Puedes descargar el código correspondiente a dicha lección como te indico a continuación:

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 14 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion14 -b leccion14

Índice
Aquí te dejo los puntos principales de esta lección:

Mostrar fechas en las plantillas Flask
Formatear fechas en las plantillas
Usar filtros en Flask para formatear fechas
Mostrar fechas en las plantillas Flask
Hay dos elementos del miniblog que hacen uso de fechas. Son los posts y los comentarios. Si abres el fichero app/models.py, verás que tanto el modelo Post como el modelo Comment definen un atributo llamado created. Este atributo guarda, de forma automática, la fecha en que se crea un post y un comentario, respectivamente.

Sin embargo, hasta ahora, no habíamos usado dichos atributos en ninguna parte del proyecto 🤔 Pongámosle remedio. Como en cualquier blog, mostraremos la fecha de publicación de un post y la fecha en que se produjo un comentario.

Abre el fichero app/public/templates/public/index.html y justo después del título del post, añade todo lo que está entre las etiquetas <span> (incluida) para que aparezca la fecha en que se creó/publicó el post:

<li>
    <a href="{{ url_for('public.show_post', slug=post.title_slug) }}">
        {{ post.title }} <span class="postCreated">({{ post.created }})</span>
    </a>
</li>
Si accedes a la página principal del blog, verás que ahora se muestra la fecha de creación de cada post:

Fechas en Flask formateadas por defecto
Formatear fechas en las plantillas
Te habrás dado cuenta de que, por defecto, las fechas se muestran en formato anglosajón. Si quisiéramos dar otro formato a las fechas, podríamos hacer uso de la función strftime en el código de la propia plantilla.

Abre de nuevo la plantilla index.html y sustituye:

{{ post.created }}
Por esto otro:

{{ post.created.strftime('%d-%m-%Y') }}
Al acceder ahora a la página principal del blog, veremos que se muestran las fechas con el nuevo formato:

Fechas en Flask con formato personalizado
El único problema de formatear así las fechas es que tendríamos que repetir lo mismo en la plantilla app/public/templates/public/post_view.html para mostrar la fecha del post y la fecha de cada uno de los comentarios. ¿Qué ocurriría si por cualquier motivo decidimos mostrar las fechas del blog en otro formato? Pues tendríamos que recorrer todas las plantillas en busca de campos tipo fecha y actualizar la cadena de formato de cada uno de ellos.

¡Suena a problema! ¿Verdad? No te preocupes que en la siguiente sección descubrirás un truco mucho mejor para mostrar fechas en Flask.

Usar filtros en Flask para formatear fechas
Una alternativa mejor a usar la función strftime en las plantillas para formatear una fecha, es hacer uso de los filtros que provee JINJA2.

Un filtro no es más que una función que modifica el valor de una variable y que se usa dentro de una plantilla. Pero mejor veámoslo con un ejemplo. Vamos a crear un filtro personalizado para formatear las fechas a nuestro gusto en las páginas de nuestro blog.

Añade un nuevo fichero llamado filters.py al directorio app/common/. A continuación, pega el siguiente código:

def format_datetime(value, format='short'):
    value_str = None
    if not value:
        value_str = ''
    if format == 'short':
        value_str = value.strftime('%d/%m/%Y')
    elif format == 'full':
        value_str = value.strftime('%d de %m de %Y')
    else:
        value_str = ''
    return value_str
La función format_datetime tiene dos parámetros: value es la fecha a transformar y format el formato de salida que aplicaremos a la fecha (short o full). Pero para usar la función en las plantillas del blog, antes debemos indicar que es un filtro.

Abre el fichero app/__init__.py y, justo después de la función create_app(), añade la siguiente:

from app.common.filters import format_datetime
def register_filters(app):
    app.jinja_env.filters['datetime'] = format_datetime
La función register_filters() registra la función format_datetime() como filtro de JINJA2. Tan solo queda hacer la llamada a la función. Añade la siguiente línea dentro de la función create_app(), tras inicializar las extensiones y antes de registrar los Blueprins:

def create_app(settings_module):
    ...
    migrate.init_app(app, db)
    mail.init_app(app)
    # Registro de los filtros
    register_filters(app)
    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    ...
¡¡Con esto, ya podemos usar el filtro en nuestras páginas!! 💃🏻🎉

Abre la plantilla app/public/templates/public/index.html y sustituye el siguiente código:

{{ post.created.strftime('%d-%m-%Y') }}
Por este otro:

{{ post.created|datetime }}
Para usar un filtro añade el carácter | después del nombre de una variable y a continuación el nombre del filtro a aplicar.

Ahora abre la plantilla app/public/templates/public/post_view.html

Añade el siguiente bloque div, justo después del título del post, para mostrar la fecha en que se creó la entrada con formato full:

<h1>{{ post.title }}</h1>
<div>
    <span class="blogDate">{{ post.created|datetime('full') }}</span>
</div>
{{ post.content }}
Tan solo nos falta mostrar la fecha en que se escribió un comentario. Dentro de la plantilla post_view.html, añade lo siguiente en la línea en que se muestra el nombre de la persona:

<div>
    El usuario {{ comment.user_name }} comentó el <span class="blogDate">{{ comment.created|datetime }}</span>:
</div>
Si accedemos a la página de detalle de un post, podremos ver las fechas tanto de la entrada como de sus comentarios:

Fechas en Flask detalle de un post
Y hasta aquí llega esta lección.

Conclusión
Como has podido comprobar, usar fechas en las plantillas es muy fácil en Flask. Mi recomendación es que, siempre que sea posible, definas un filtro para dar formato a las fechas. De esta forma puedes reutilizarlo en todas tus páginas y cualquier cambio que quieras/debas hacer estará localizado en un único punto.

Como siempre, si tienes alguna duda puedes ponerte en contacto conmigo dejándome un mensaje al final del post, a través de mis redes sociales o enviándome un email. Estaré encantado de poder ayudarte.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 15 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion15 -b leccion15

En la siguiente lección veremos cómo procesar ficheros en Flask para guardar la imagen de cabecera de los posts. ¡Será muy interesante! ¡No te la pierdas!
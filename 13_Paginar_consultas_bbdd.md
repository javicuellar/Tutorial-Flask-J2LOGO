Lección 13: Paginar las consultas de base de datos
Categoría: Flask
flask, medio, python, tutorial flask
Lección 13 Paginar las consultas de base de datos
En muchas aplicaciones web, trabajar con listados es una tarea muy común: listado de usuarios, listado de productos, listado de posts, … En esta lección te enseñaré un truco muy sencillo para paginar las consultas de base de datos, de manera que los listados no afecten negativamente al rendimiento de tu aplicación.

Como ves, las lecciones finales del tutorial sobre Flask están llenas de trucos y mejoras en la aplicación que son de gran utilidad. ¡Vamos, no te pierdas el maravilloso mundo de la paginación! ¿Lo quieres descubrir?

Continuaremos el tutorial por donde lo dejamos en la lección anterior, en la que vimos cómo crear tests con Flask para hacer nuestro código más seguro frente a cambios. Puedes descargar el código de dicha lección como te indico a continuación:

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 12 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion12 -b leccion12

Índice
Aquí te dejo los puntos principales de esta lección:

La consulta básica para mostrar un listado de elementos
Añadir una consulta paginada de base de datos al modelo Post
Actualizar la vista index para hacer uso de la consulta paginada
Añadir controles de navegación a un listado paginado
Definir parámetros de configuración para la paginación
La consulta básica para mostrar un listado de elementos
Cuando tenemos que mostrar un listado de elementos en una aplicación, lo primero que nos viene a la mente es realizar una consulta para obtenerlos todos.

Una consulta de este tipo la podemos encontrar en el modelo Post. En concreto, la consulta que se realiza en el método get_all():

@staticmethod
def get_all():
    return Post.query.all()
Como puedes apreciar, esta consulta devuelve un listado con todas las entradas que existen en el blog. Si activamos los logs de SQLAlchemy, podremos observar que el código SQL que se ejecuta es el siguiente:

Consulta básica de un listado de posts
En principio, este tipo de consultas no está mal si tenemos la certeza de que el número de elementos devuelto es reducido. Por ejemplo, un listado de provincias, las direcciones de un usuario, etc. Ahora bien, ¿te imaginas que el blog tuviera 500 posts? ¿Lo lento que sería renderizar la página del listado de posts?

Pues imagina que estuvieras desarrollando una aplicación para gestionar un catálogo con miles y miles de productos. ¡¡No los puedes mostrar todos a la vez en una misma página!! Si lo haces, puedes consumir muchos recursos, tanto del servidor web como del servidor de base de datos y, con unas pocas peticiones, te quedas sin aplicación.

Añadir una consulta paginada de base de datos al modelo Post
Sin embargo, como ya te he mostrado en otras lecciones, todo problema tiene solución y la nuestra se llama consultas paginadas de base de datos.

Básicamente, una consulta paginada tiene la misma forma que una consulta que devuelve todos los elementos de una tabla, con la diferencia de que define unos límites para obtener únicamente un subgrupo de elementos. Imagina que los elementos de una tabla se ordenan en base a un índice (0, 1, 2, 3, 4, …). Pues una consulta paginada establece a partir de qué índice se devuelven los elementos y cuántos de ellos.

¿Difícil? Todo lo contrario. La clase BaseQuery de Flask-SQLAlchemy nos ofrece el método paginate() que nos facilita la ejecución de este tipo de consultas.

¡A jugar! Vamos a añadir una consulta paginada al modelo Post de manera que obtengamos un listado paginado de entradas del blog.

Añade el siguiente método al final de la clase Post:

@staticmethod
def all_paginated(page=1, per_page=20):
    return Post.query.order_by(Post.created.asc()).\
        paginate(page=page, per_page=per_page, error_out=False)
Esta consulta devuelve un listado paginado de posts ordenados por fecha de creación. La paginación la controlamos con el parámetro page, que indica la página a partir de la cuál obtener los resultados, y el parámetro per_page, que indica cuántos elementos se devuelven en la consulta. Realmente, el método paginate() devuelve un objeto de tipo Pagination que, además de los elementos devueltos, tiene campos para controlar la paginación de la consulta. El método paginate() se encarga de traducir los parámetros page y per_page para indicar en la consulta SQL que se genera a partir de qué índice se obtienen los elementos y cuántos de ellos.

Actualizar la vista index para hacer uso de la consulta paginada
En esta sección vamos a ver cómo usar el método all_paginated().

Actualmente, esta es la pinta que tiene mi página principal del blog cuando accedo a ella (http://localhost:5000):

Paginar consultas de base de datos - Listado completo
Para que este listado se muestre paginado, tenemos que modificar la vista index() que se encuentra en el fichero app/public/routes.py. Ábrelo y actualiza la vista como te indico a continuación:

@public_bp.route("/")
def index():
    logger.info('Mostrando los posts del blog')
    posts = Post.all_paginated(2, 3)
    return render_template("public/index.html", posts=posts.items)
Las únicas diferencias con respecto la versión anterior son que hacemos uso del método all_paginated() y que, como dicha consulta nos devuelve un objeto de tipo Pagination, tenemos que acceder al campo items del mismo para recuperar el listado de elementos.

Observa que se llama al método all_paginated() con los argumentos page=2 y per_page=3. Esto nos devolverá los elementos que pertenezcan a la página 2 si estos se agrupan de 3 en 3, es decir, obtendremos las entradas correspondientes a los índices 3, 4 y 5. Si accedo ahora a la página principal del blog, esto es lo que veo:

Paginar consultas de base de datos - Listado paginado de entradas
Y la consulta SQL que se genera es la siguiente:

Paginar consultas de base de datos - Consulta SQL paginada
Añadir controles de navegación a un listado paginado
Bueno, la cosa va tomando forma. Hemos visto cómo usar la consulta paginada, sin embargo, siempre devuelve las mismas entradas del blog. Estaría bien poder navegar por el listado para consultar todas las entradas, ¿no te parece?

Empecemos introduciendo los siguientes cambios en la vista index():

@public_bp.route("/")
def index():
    logger.info('Mostrando los posts del blog')
    page = int(request.args.get('page', 1))
    post_pagination = Post.all_paginated(page, 3)
    return render_template("public/index.html", post_pagination=post_pagination)
Básicamente, hemos realizado dos cambios. El primero es que el número de página se recupera de un parámetro de la URL llamado page (en caso de que no se pase el parámetro en la URL, se usa por defecto el valor 1). El segundo es que en lugar de pasar los items del objeto Pagination a la plantilla, se pasa el objeto completo, post_pagination.

Ahora toca modificar la plantilla app/public/templates/public/index.html.

Actualiza el bucle for sustituyendo la variable posts por post_pagination.items. A continuación, añade tras el listado el script que genera los controles de navegación. El resultado sería el siguiente:

{% extends "base_template.html" %}
{% block title %}Tutorial Flask: Miniblog{% endblock %}
{% block content %}
    <ul>
    {% for post in post_pagination.items %}
        <li><a href="{{ url_for('public.show_post', slug=post.title_slug) }}">{{ post.title }}</a></li>
    {% else %}
        <li>No hay entradas</li>
    {% endfor %}
    </ul>
    <div class=pagination>
        {%- for page in post_pagination.iter_pages() %}
            {% if page %}
                {% if page != post_pagination.page %}
                    <a href="{{ url_for('public.index', page=page) }}">{{ page }}</a>
                {% else %}
                    <strong>{{ page }}</strong>
                {% endif %}
            {% else %}
                <span class=ellipsis>…</span>
            {% endif %}
        {%- endfor %}
    </div>
{% endblock %}
Esta vez, si accedo a la página principal del blog, puedo ver los controles de la paginación y puedo navegar entre ellos:

Listado paginado con controles de navegación
¡¡¡Como te habrás dado cuenta, paginar las consultas de base de datos es muy, muy sencillo con Flask-SQLAlchemy!!!

Definir parámetros de configuración para la paginación
Con todo lo visto hasta ahora, ya tienes por dónde empezar para paginar tus consultas de base de datos. No obstante, hay un aspecto que todavía podemos mejorar. Si te has fijado, en la llamada al método all_paginated() que se realiza en la vista index(), el segundo argumento siempre es fijo con valor 3. Que ese valor esté ahí definido no me gusta. ¿De dónde sale? ¿Por qué vale 3 y no 17?

Definamos un parámetro de configuración a nivel de aplicación. Dicho parámetro establece el número de elementos por defecto a mostrar en los listados paginados.

Abre el fichero config/default.py y al final del mismo añade lo siguiente:

ITEMS_PER_PAGE = 3
A continuación, actualiza la vista index() para que haga uso de ese parámetro:

@public_bp.route("/")
def index():
    logger.info('Mostrando los posts del blog')
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    post_pagination = Post.all_paginated(page, per_page)
    return render_template("public/index.html", post_pagination=post_pagination)
¡Wow! ¡Ahora sí que nos ha quedado una paginación casi de 10!

Conclusión
Esta lección ha sido más corta que otras. En ella hemos repasado los posibles problemas que puede haber al hacer consultas a toda una tabla. También has aprendido como paginar consultas de base de datos con el método paginate() del objeto BaseQuery de Flask-SQLAlchemy.

Si quieres seguir practicando, te dejo como ejercicio los siguientes puntos de mejora:

Limitar el número de controles de navegación que se muestran. Algo así como: 1 2 3 ... 8 9 10.
Permitir al usuario indicar el número de elementos que se recuperan: 10, 20 o 30. (Ayuda: Pasa este parámetro en la URL).
Como siempre, si tienes alguna duda puedes ponerte en contacto conmigo dejándome un mensaje al final del post, a través de mis redes sociales o enviándome un email. Estaré encantado de poder ayudarte.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 13 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion13 -b leccion13

En la siguiente lección veremos algo que seguro te va a gustar: cómo enviar emails en Flask. ¡No te la pierdas!
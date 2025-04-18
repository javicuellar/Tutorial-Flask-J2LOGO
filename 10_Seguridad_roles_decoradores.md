Lección 10: Añadiendo seguridad en las vistas
Categoría: Flask
flask, medio, python, tutorial flask
Lección 10 Añadiendo seguridad en las vistas
A estas alturas del tutorial ya tenemos la mayor parte de la funcionalidad de nuestro blog desarrollada. Tan solo nos falta ir añadiendo pequeños detalles para mejorar sustancialmente nuestra aplicación. Vamos a empezar a implementar estos detalles en esta lección, donde veremos cómo añadir seguridad a las vistas para que solo ciertos roles puedan realizar determinadas acciones.

Como dijimos en la presentación del tutorial, en el blog existen usuarios administradores, que son los únicos que pueden crear entradas en el blog, eliminarlas, consultar los usuarios registrados y asignarles el rol de administrador. Por tanto, solo los usuarios con el rol de administrador pueden tener acceso a estas partes de la aplicación.

👉🏾 Esta lección es IM-PER-DI-BLE, ya que en ella te enseñaré un truco que muchos desarrolladores Python no conocen. ¿Quieres descubrirlo? ¡No te pierdas lo que sigue a continuación!

El tutorial sigue por donde lo dejamos en la lección anterior, en la que te explicaba cómo añadir mensajes de log para conocer cómo usaban los usuarios la aplicación y detectar bugs lo antes posible.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 9 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion9 -b leccion9

Índice
Aquí te dejo los puntos principales de esta lección:

La forma menos buena de añadir seguridad en las vistas
Añadiendo seguridad en las vistas con decoradores
Mejorando la parte de administración del blog
La forma menos buena de añadir seguridad en las vistas
El grueso de esta lección del tutorial se centrará principalmente en el paquete app.admin. En él vamos a implementar toda la lógica necesaria para satisfacer los requisitos de nuestro blog que tienen que ver con su administración.

Haciendo un pequeño repaso, recuerda que el modelo User definía un atributo is_admin. Este atributo sirve para identificar si un usuario es administrador o no. Por otro lado, vamos a revisar el fichero app/admin/routes.py. En él se encuentra la vista post_form() que usamos para añadir nuevas entradas al blog. A esta vista le añadimos el decorador @login_required para que solo los usuarios autenticados pudieran tener acceso. ¿Se te ocurre alguna manera de que solo los usuarios administradores puedan crear entradas en el blog?

Quizá una primera aproximación sea la que el 90% de los principiantes imaginan:

from flask_login import current_user
@admin_bp.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@admin_bp.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    if current_user.is_admin:
        form = PostForm()
        if form.validate_on_submit():
            title = form.title.data
            # Resto del código
            ...
    else:
        # El usuario no está autorizado a acceder (error 401)
        abort(401)
Bueno, en un principio, con esto logramos resolver lo que se nos pide. Pero ahora yo hago de mala conciencia y te aviso que todavía nos queda por implementar la funcionalidad para editar un post, eliminar una entrada, listar y eliminar usuarios y asignarles el rol administrador.

Añadir el condicional if current_user.is_admin y su respectivo else al inicio y final de cada una de las vistas es muy engorroso, el código pierde legibilidad, por no decir qué ocurriría en caso de que el atributo is_admin cambiara de nombre o de tipo.

En la siguiente sección veremos una forma mejor de añadir seguridad en las vistas utilizando decoradores.

Añadiendo seguridad en las vistas con decoradores
¿Te acuerdas que te dije que te iba a enseñar un truco que muchos principiantes no conocen? Pues aquí lo tienes: el uso de decoradores para añadir seguridad en las vistas.

Vamos a mejorar el código de la sección anterior creando un decorador similar a @login_required que llamaremos @admin_required ¿No sabes qué es un decorador? No te preocupes, que lo vas a entender en unos segundos.

Como no es el propósito de esta lección explicar los decoradores en profundidad, básicamente te diré que un decorador es una función que recibe como parámetro otra función y devuelve como resultado una función diferente.

Lo que nos permiten los decoradores es hacer que una función envuelva a otra función, ejecutando código previo a la ejecución de esta última. Resultan muy útiles para eliminar código repetitivo, separar la responsabilidad del código, añadir seguridad a las vistas y aumentar su legibilidad.

Existen varias formas de crear un decorador, pero la más simple, un decorador sin parámetros, sigue la siguiente estructura:

from functools import wraps
def mi_decorador(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        # Código del decorador
        ...
        return f(*args, **kws)
    return decorated_function
Puedes apreciar que el decorador mi_decorador recibe como parámetro la función f y devuelve como resultado la función decorated_function (que es el resultado de ejecutar el código del decorador y después ejecutar la función f).

Ejemplo de decorador
Mejor con un ejemplo. Imagina que tenemos las siguientes funciones:

def print_nombre(nombre):
    print(nombre)
def print_hola(f):
    print('Hola')
    f
Como puedes ver, la segunda recibe como parámetro una función. Si las concatenamos del siguiente modo, el resultado sería la ejecución de print_nombre más el resultado de print_hola:

print_hola(print_nombre('j2logo'))
j2logo
Hola
Si ahora transformamos la función print_hola() en un decorador el resultado sería diferente, puesto que primero se ejecuta el código del decorador como envoltorio de la función print_nombre().

from functools import wraps
def print_hola(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        print('Hola')
        return f(*args, **kws)
    return decorated_function
@print_hola
def print_nombre(nombre):
    print(nombre)
>>> print_nombre('j2logo')
Hola
j2logo
Al decorar la función print_nombre() con @print_hola, se ejecuta el código del decorador antes que el de la propia función.

Usando nuestro propio decorador @admin_required
Al principio de esta lección te comentaba que ya habíamos usado el decorador @login_required en la función post_form(). Este decorador comprueba que el usuario se ha autenticado en la aplicación antes de ejecutar el código de la función post_form(). Si no está autenticado, se redirige al usuario a la página de login. ¡Haz la prueba!

Ahora lo que queremos es que solo los usuarios administradores tengan acceso al formulario de crear una nueva entrada (es decir, a la vista post_form()). Por tanto, vamos a crear un decorador que haga esta comprobación y que podremos reutilizar en otras vistas. Como esta funcionalidad está relacionada con la parte de gestión de usuarios, lo añadiremos en el paquete app.auth.

Crea un nuevo fichero llamado decorators.py en el directorio app/auth. Abre el fichero con tu editor de código y pega lo siguiente:

from functools import wraps
from flask import abort
from flask_login import current_user
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_admin = getattr(current_user, 'is_admin', False)
        if not is_admin:
            abort(401)
        return f(*args, **kws)
    return decorated_function
Lo que hemos hecho es crear el decorador @admin_required. Este decorador comprueba si el objeto current_user tiene el atributo is_admin y su valor es True. Si es así, ejecuta la función f. En caso contrario devuelve un error 401, no permitiendo la ejecución de f.

¿Tienes ganas de verlo en acción? ¡Vamos a ello! 🏃🏻‍♂️

Abre el fichero app/admin/routes.py, importa el decorador que acabamos de crear y añádelo justo después del decorador @login_required a la vista post_form(). Tu código debería parecerse a este:

from app.auth.decorators import admin_required
@admin_bp.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@admin_bp.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # Resto del código
        ...
Al añadir el decorador @admin_required seguidamente de @login_required estamos concatenando las funcionalidades de ambos decoradores. Esto implica que antes de ejecutar la vista post_form() se comprueba si el usuario está autenticado y si es administrador.

¡A jugar! Ejecuta el servidor de Flask, autentícate con un usuario y prueba a acceder a la dirección http://localhost:5000/admin/post/

¿Qué ocurre? ¿Te aparece una página con un mensaje Unauthorized? Entonces lo hemos hecho bien 😊

Tan solo nos falta crear un usuario de tipo administrador para comprobar que tiene permisos para crear nuevas entradas en nuestro blog.

Abre la consola de tu base de datos y ejecuta la siguiente sentencia:

INSERT INTO blog_user(name, email, password, is_admin) VALUES ('ADMIN', 'admin@xyz.com', 'pbkdf2:sha256:150000$5oClIM0i$c155be080802a2299bf20f891ea9e542c8fb11ea4a5927d390c36d2d91252a60', TRUE);
Esto añadirá un usuario administrador cuya contraseña es 1234. Créalo y comprueba que ahora sí tienes acceso a la vista post_form().

Mejorando la parte de administración del blog
En lo que resta de lección vamos a implementar los requisitos relacionados con la parte de administración del blog haciendo uso del decorador @admin_required.

Página de error personalizada para accesos no autorizados
Lo primero que haremos será añadir una página de error personalizada para accesos no autorizados. Cada vez que un usuario que no sea administrador acceda a una vista con el decorador @admin_required, se le mostrará una página en la que se indique que no tiene acceso.

Ya vimos en la lección 8 cómo se hacía esto. ¿Recuerdas?

Añade una nueva página html al directorio app/templates con nombre 401.html y el siguiente contenido:

{% extends 'base_template.html' %}
{% block content %}
    Ooops!! No tienes permisos de acceso
{% endblock %}
A continuación abre el fichero app/__init__.py. Sitúate en la función register_error_handlers() y añade un nuevo manejador para los errores de tipo 401 (que es el que se lanza en el decorador @admin_required cuando el usuario no es administrador):

def register_error_handlers(app):
    # Otros error handlers
    ...
    @app.errorhandler(401)
    def error_404_handler(e):
        return render_template('401.html'), 401
Actualiza los modelos User y Post
A continuación vamos a actualizar el modelo User para añadir un método que permita eliminar usuarios y otro método para listar todos los usuarios registrados en el sistema.

Abre el fichero app/auth/models.py y añade los siguientes métodos a la clase User:

class User(db.Model, UserMixin):
    __tablename__ = 'blog_user'
    id = db.Column(db.Integer, primary_key=True)
    # Resto del código
    ...
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @staticmethod
    def get_all():
        return User.query.all()
Ahora modificaremos el modelo Post añadiendo un método para eliminar posts y otro para obtener un post a partir de su id.

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Resto del código
    ...
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @staticmethod
    def get_by_id(id):
        return Post.query.get(id)
❗️¡ATENCIÓN! Elimina el método public_url de la clase Post. De este modo eliminamos dependencias a otros paquetes en este módulo. Veremos las consecuencias a continuación.

Al eliminar el método public_url() de la clase Post tenemos que actualizar la plantilla app/public/templates/public/index.html. Ábrela y modifica la línea:

<li><a href="{{ post.public_url() }}">{{ post.title }}</a></li>
Por esta otra:

<li><a href="{{ url_for('public.show_post', slug=post.title_slug) }}">{{ post.title }}</a></li>
Listado de posts del panel de administración
El siguiente paso es añadir toda la lógica para mostrar el listado de entradas del blog desde el punto de vista del administrador. Esto es necesario ya que este listado muestra opciones diferentes respecto del de la página publica.

Abre el fichero app/admin/routes.py y añade la siguiente vista justo antes de la función post_form():

@admin_bp.route("/admin/posts/")
@login_required
@admin_required
def list_posts():
    posts = Post.get_all()
    return render_template("admin/posts.html", posts=posts)
Sí, a esta vista también le hemos añadido seguridad con los decoradores @login_required y @admin_required. Ahora toca añadir la plantilla del listado de entradas. Crea el fichero posts.html dentro del directorio app/admin/templates/admin con el siguiente contenido:

{% extends "base_template.html" %}
{% block title %}
    Listado de posts
{% endblock %}
{% block content %}
    <div>
        <a href="{{ url_for('admin.post_form') }}">Añadir entrada</a>
    </div>
    <h2>Listado de entradas</h2>
    <ul>
    {% for post in posts %}
        <li>
            <a href="{{ url_for('admin.update_post_form', post_id=post.id) }}">{{ post.title }}</a>
        </li>
    {% endfor %}
    </ul>
{% endblock %}
Nueva vista para editar las entradas del blog
De lecciones anteriores, en el fichero app/admin/routes.py teníamos la vista post_form():

@admin_bp.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@admin_bp.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def post_form(post_id):
    if current_user.is_admin:
    # Resto del código
    ...
Como puedes apreciar, esta vista estaba preparada tanto para crear nuevas entradas (respondiendo a la URL /admin/post), como para editar una entrada a partir de su id (respondiendo a la URL /admin/post/<post_id>). Para no mezclar la lógica de ambas cosas, he decidido separar la vista en dos: una para crear nuevos posts y otra para editarlos a partir de un id de entrada. El resultado es el siguiente:

@admin_bp.route("/admin/post/", methods=['GET', 'POST'])
@login_required
@admin_required
def post_form():
    """Crea un nuevo post"""
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()
        logger.info(f'Guardando nuevo post {title}')
        return redirect(url_for('admin.list_posts'))
    return render_template("admin/post_form.html", form=form)
@admin_bp.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_post_form(post_id):
    """Actualiza un post existente"""
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f'El post {post_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del post.
    form = PostForm(obj=post)
    if form.validate_on_submit():
        # Actualiza los campos del post existente
        post.title = form.title.data
        post.content = form.content.data
        post.save()
        logger.info(f'Guardando el post {post_id}')
        return redirect(url_for('admin.list_posts'))
    return render_template("admin/post_form.html", form=form, post=post)
Funcionalidad para eliminar un post
Lo último que nos queda por hacer respecto de un post en el módulo de administración es poder eliminarlo. Para ello, añade la siguiente vista al final del fichero app/admin/routes.py:

from flask import abort
@admin_bp.route("/admin/post/delete/<int:post_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_post(post_id):
    logger.info(f'Se va a eliminar el post {post_id}')
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f'El post {post_id} no existe')
        abort(404)
    post.delete()
    logger.info(f'El post {post_id} ha sido eliminado')
    return redirect(url_for('admin.list_posts'))
En ella recuperamos de la base de datos un post a partir de su id (post_id). Si no existe, se devuelve un error 404. Por el contrario, si recuperamos el post, lo eliminamos haciendo uso del método delete() que creamos previamente. Al final, redirigimos al usuario al listado de posts del administrador.

Tan solo falta añadir una opción en el formulario de edición de un post para poder eliminarlo. Abre el fichero app/admin/templates/admin/post_form.html y añade el siguiente formulario a continuación del anterior:

        <div>
            {{ form.submit() }}
        </div>
    </form>
    {% if post %}
    <form action="{{ url_for('admin.delete_post', post_id=post.id) }}" method="post" novalidate>
        <input type="submit" value="Eliminar" />
    </form>
    {% endif %}
{% endblock %}
Listar los usuarios registrados en el sistema
Para listar los usuarios registrados en el sistema, añade una nueva vista al final del fichero app/admin/routes.py:

from app.auth.models import User
@admin_bp.route("/admin/users/")
@login_required
@admin_required
def list_users():
    users = User.get_all()
    return render_template("admin/users.html", users=users)
Y ahora crea la plantilla users.html en el directorio app/admin/templates/admin:

{% extends "base_template.html" %}
{% block title %}
    Listado de usuarios
{% endblock %}
{% block content %}
    <ul>
    {% for user in users %}
        <li><a href="{{ url_for('admin.update_user_form', user_id=user.id) }}">{{ user.name }}</a> (Admin: {{ user.is_admin}})</li>
    {% endfor %}
    </ul>
{% endblock %}
En esta plantilla se muestra el listado de usuarios registrados en el blog. Por cada usuario, se añade un enlace que abre un formulario para editar el detalle del mismo. Es lo que explicaré en la siguiente sección.

Formulario para editar los datos de un usuario
A continuación añadiremos la lógica para que un usuario administrador pueda asignar a otro usuario del blog como admin. Comienza añadiendo el formulario UserAdminForm en el siguiente fichero app/admin/forms.py:

from wtforms import (StringField, SubmitField, TextAreaField, BooleanField)
class PostForm(FlaskForm):
    # Campos del formulario
    ...
class UserAdminForm(FlaskForm):
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Guardar')
Ahora añade la vista update_user_form() al final del fichero app/admin/routes.py:

from .forms import PostForm, UserAdminForm
@admin_bp.route("/admin/user/<int:user_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_user_form(user_id):
    # Aquí entra para actualizar un usuario existente
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del usuario.
    form = UserAdminForm(obj=user)
    if form.validate_on_submit():
        # Actualiza los campos del usuario existente
        user.is_admin = form.is_admin.data
        user.save()
        logger.info(f'Guardando el usuario {user_id}')
        return redirect(url_for('admin.list_users'))
    return render_template("admin/user_form.html", form=form, user=user)
Esta vista hace uso del formulario UserAdminForm que lo inicializa con los datos de un usuario dado su id. En ella se procesa el formulario, obteniendo el campo is_admin para actualizar el atributo del mismo nombre del usuario. Si la petición es un GET, se muestra la página del formulario. Añade esta página, con nombre user_form.html, en el directorio app/admin/templates/admin:

{% extends "base_template.html" %}
{% block title %}
    {{ user.name }}
{% endblock %}
{% block content %}
    <h2>Detalle del usuario</h2>
    <div>
    Nombre: {{ user.name }}
    </div>
    <div>
    Email: {{ user.email }}
    </div>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <div>
            {{ form.is_admin.label }}
            {{ form.is_admin }}<br>
            {% for error in form.is_admin.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </div>
        <div>
            {{ form.submit() }}
        </div>
    </form>
    <form action="{{ url_for('admin.delete_user', user_id=user.id) }}" method="post" novalidate>
        <input type="submit" value="Eliminar" />
    </form>
{% endblock %}
Esta plantilla contiene dos formularios: uno para modificar el atributo is_admin de un usuario y otro que se utiliza para eliminar al usuario del sistema. Lo veremos a continuación.

Vista para eliminar a un usuario
En la plantilla anterior veíamos que existía un formulario cuyo atributo action hacía referencia a la vista admin.delete_user, la cual se utiliza para eliminar a un usuario del sistema. Añade dicha vista al final del fichero app/admin/routes.py:

@admin_bp.route("/admin/user/delete/<int:user_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_user(user_id):
    logger.info(f'Se va a eliminar al usuario {user_id}')
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    user.delete()
    logger.info(f'El usuario {user_id} ha sido eliminado')
    return redirect(url_for('admin.list_users'))
Página principal del panel de administración
Lo último que nos falta para que nuestro blog se quede de lujo es añadir una página con las opciones principales del panel de administración.

Para ello, en primer lugar, añadiremos una nueva vista al principio del fichero app/admin/routes.py:

# Imports
...
@admin_bp.route("/admin/")
@login_required
@admin_required
def index():
    return render_template("admin/index.html")
# Resto de vistas
...
Seguidamente, crearemos la plantilla index.html en el directorio app/admin/templates/admin:

{% extends "base_template.html" %}
{% block title %}
    Miniblog | Admin
{% endblock %}
{% block content %}
    <ul>
        <li><a href="{{ url_for('admin.list_posts') }}">Posts</a></li>
        <li><a href="{{ url_for('admin.list_users') }}">Usuarios</a></li>
    </ul>
{% endblock %}
Como puedes observar, esta plantilla contiene un enlace a las páginas del listado de posts y de usuarios.

Por último, añadiremos un enlace al menú del blog que nos lleve a esta página del panel de administración. Para ello, abre la plantilla app/templates/base_template.html y justo después de donde se muestra el nombre del usuario añade lo siguiente:

    ...
    {% else %}
        <li>{{ current_user.name }}</li>
        {% if current_user.is_admin %}
            <li> | </li>
            <li><a href="{{ url_for('admin.index') }}">Admin</a></li>
        {% endif %}
        <li> | </li>
        <li><a href="{{ url_for('auth.logout') }}">Logout</a></li>
    {% endif %}
    ...
Fíjate que añadimos el enlace al panel de administración solo si el usuario es administrador.

Conclusión
Pues ya solo te queda salir corriendo 🏃🏻‍♂️ y jugar con las nuevas funcionalidades que hemos añadido al miniblog 🤓💃🏻

Esta lección ha sido muy interesante ya que en ella hemos introducido el concepto de los decoradores para facilitar y mejorar la seguridad en las vistas. Además, le hemos metido caña al blog incluyendo todas las funcionalidades de la parte de administración.

El final del tutorial se aproxima, y cada vez estás más capacitad@ para volar por ti mism@, pero como siempre, si tienes alguna duda puedes ponerte en contacto conmigo dejándome un mensaje al final del post, a través de mis redes sociales o enviándome un email. Estaré encantado de poder ayudarte.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 10 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion10 -b leccion10

¡Por cierto! La siguiente lección no te la pierdas. En ella te presentaré una nueva extensión que te ayudará a generar scripts de bases de datos, junto con sus cambios incrementales a medida que haces modificaciones en tus modelos. ¡Te espero!
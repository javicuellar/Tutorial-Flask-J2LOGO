Lección 5: Base de datos con Flask SQLAlchemy
Categoría: Flask
flask, medio, python, sqlalchemy, tutorial flask
Tutorial flask - Lección 5 Base datos SQLAlchemy
Poco a poco el miniblog está tomando forma, aunque todavía quedan muchas cosas por aprender. En este tutorial vamos a ver algo que es imprescindible en la mayoría de aplicaciones web: La integración con una base de datos. Y lo haremos a través de la extensión Flask-SQLAlchemy.

Como sucedía en los tutoriales previos, esta lección es la continuación de la anterior, en la que vimos cómo realizar el login de los usuarios del blog y en la que creamos una primera versión del modelo User.

Bueno, pues ya no te entretengo más, que estoy seguro de que estás impaciente por aprender cómo integrar una base de datos con Flask. Espero que te guste el tutorial 😊

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 4 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion4 -b leccion4

Índice
A continuación te muestro el índice de esta lección:

Introducción a Flask-SQLAlchemy
Configurar Flask-SQLALchemy
Actualizamos el modelo User
Flask SQLALchemy en acción
Añadimos el modelo Post
Actualizando las vistas que gestionan los posts
Creando la base de datos
Introducción a Flask-SQLAlchemy
No sé si lo sabes pero, por defecto, Flask no viene integrado con ninguna base de datos. Y esto que en principio puede parecer un inconveniente es, en realidad, una gran ventaja. Te explicaré por qué.

En la actualidad existen, principalmente, dos grandes familias de bases de datos: las relacionales (PostgreSQL, MySQL, Oracle, …) y las NoSQL (MongoDB, CouchDB, Cassandra, …). Utilizar un tipo u otro en nuestra aplicación dependerá de múltiples factores, como la escalabilidad o asegurar la fiabilidad de los datos.

Gracias a que Flask no integra por defecto ninguna base de datos, podemos usar en nuestra aplicación la que mejor satisfaga nuestras necesidades en cada momento.

Nosotros, en este tutorial de Flask, trabajaremos con bases de datos relacionales (yo personalmente utilizaré PostgreSQL, aunque tú puedes usar aquella con la que te sientas más cómod@).

Fundamentalmente, las bases de datos relacionales se caracterizan por utilizar el lenguaje SQL como lenguaje para realizar consultas y estar compuestas de varias tablas. A su vez, estas tablas están formadas por un conjunto de campos (columnas) y registros (filas). Otra propiedad muy característica es que entre las tablas se establecen relaciones.

En Python (realmente en cualquier lenguaje), y particularmente en Flask, podemos usar diferentes librerías para trabajar, consultar y manipular nuestra base de datos usando directamente el lenguaje SQL. No obstante, en la mayoría de los casos resulta más apropiado utilizar un ORM, sobre todo cuando en nuestra aplicación hacemos uso de objetos (Programación Orientada a Objetos).

Flask-SQLALchemy: un ORM para Flask
Un ORM (Object-Relational Mapper) es un toolkit que nos ayuda a trabajar con las tablas de la base de datos como si fueran objetos, de manera que cada tabla se mapea con una clase y cada columna con un campo de dicha clase. Además, también nos permite mapear las relaciones entre tablas como relaciones entre objetos.

No obstante, una de las características que más atractivos hacen a los ORMs es que puedes cambiar tu base de datos sin apenas modificar código. De manera que puedes programar tu aplicación con un ORM sin pensar que la base de datos es, por ejemplo, PostgreSQL o MySQL (por eso te decía que yo utilizaré PostgreSQL pero tú puedes usar la base de datos con la que te sientas más cómod@).

En este tutorial utilizaremos Flask-SQLAlchemy, una extensión para Flask que da soporte al popular ORM escrito en Python SQLAlchemy. Su objetivo es simplificar el uso de SQLAlchemy con Flask facilitando la realización de tareas comunes.

❗️Queda fuera del alcance de este tutorial explicar cómo instalar una base de datos como PostgreSQL o MySQL así como los fundamentos del lenguaje SQL. Tampoco se explicarán a fondo los detalles de SQLAlchemy. Si quieres saber más, puedes consultar su tutorial aquí.

Configurar Flask-SQLALchemy
Instalar Flask-SQLAlchemy
Al igual que con otras extensiones que hemos usado en el tutorial, lo primero que tenemos que hacer para utilizar Flask-SQLAlchemy es instalarla. Para ello, ejecuta lo siguiente en el terminal:

pip install flask-sqlalchemy
Si quieres conocer los detalles de Flask-SQLAlchemy, puedes hacerlo aquí.

Como te dije en la sección anterior, en el tutorial voy a utilizar una base de datos PostgreSQL, aunque tú puedes usar la que quieras (siempre que sea relacional). Para poder hacer uso de la base de datos, además de Flask-SQLAlchemy necesitamos un driver o port para que Python sepa cómo comunicarse con ella.

En mi caso usaré psycopg2, un adaptador PostgreSQL para el lenguaje Python implementado utilizando libpq, la librería oficial del cliente PostgreSQL.

Para instalar el driver ejecuta desde el terminal lo siguiente:

pip install psycopg2
Bien, ahora que ya lo tenemos todo listo, podemos empezar.

El primer paso para integrar Flask-SQLAlchemy en nuestra aplicación será crear el objeto SQLAlchemy e inicializarlo con la instancia de nuestra app. Este objeto contiene todas las funciones y helpers de sqlalchemy y sqlalchemy.orm. Además, proporciona una clase llamada Model que es la base para utilizar en todos nuestros modelos.

Actualizar el fichero run.py
Abre el fichero run.py y añade el siguiente import:

from flask_sqlalchemy import SQLAlchemy
Además, justo después de la línea login_manager.login_view = "login" añade lo siguiente para crear el objeto SQLAlchemy:

db = SQLAlchemy(app)
Lo último que tenemos que hacer para configurar la extensión y conectarnos a la base de datos es indicar la URI de esta. Dicha URI tiene el siguiente formato: postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>

La URI se define como un parámetro de configuración de la app, por tanto, añade lo siguiente después de la línea en la que se indica el parámetro SECRET_KEY:

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testing@localhost:5432/miniblog'
Tú define la URI con los parámetros correspondientes a tu base de datos.

En definitiva, las primeras líneas del fichero run.py deben ser como las siguientes:

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testing@localhost:5432/miniblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)
❗️También he añadido el parámetro de configuración SQLALCHEMY_TRACK_MODIFICATIONS = False, tal y como la documentación oficial te recomienda que hagas. Básicamente, de este modo deshabilito que se envíe una señal cada vez que se modifica un objeto (pero de esto no te preocupes por el momento si no sabes qué es una señal).

Actualizamos el modelo User
Una vez que hemos establecido la configuración del objeto SQLAlchemy, al cuál hemos llamado db, el siguiente paso es actualizar el modelo User para que herede de la clase Model. Esto creará la equivalencia entre la tabla user de la base de datos y la clase User.

Abre el fichero models.py, borra todo lo que hay hasta ahora y pega lo siguiente en su lugar:

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from run import db
class User(db.Model, UserMixin):
    __tablename__ = 'blog_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<User {self.email}>'
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
🎯 ¿Qué cambios se han producido con respecto la versión anterior?

En primer lugar, la clase User ahora hereda también de la clase Model (definida en el objeto SQLALchemy que hemos llamado db).
Ha desaparecido el método __init__.
Todo modelo debe definir el atributo (o atributos) que conforma su clave primaria: primary_key=True
Hemos eliminado la lista users. Ya no es necesario mantener en memoria el listado de usuarios registrados en la aplicación. Están guardados en base de datos.
Se ha sustituido la función get_user(email) por el método estático get_by_email(email) de la clase User (que explicaré a continuación).
Entendiendo el modelo User
Por defecto, Flask-SQLAlchemy se referirá a la tabla que equivale con nuestra clase con notación camel_case, es decir, todo en minúsculas y separando las palabras con un guión bajo (cada vez que encuentre una letra mayúscula a excepción de la primera). Sin embargo, en este caso particular no queremos que sea así. Por eso he definido el atributo de clase __tablename__ y le he dado el nombre blog_user. Esta es la forma de dar un nombre a las tablas de nuestra base de datos si no queremos usar la opción por defecto. ❗️ Pero, ¿por qué lo he hecho en la clase User? Básicamente porque user, que sería el nombre que Flask-SQLAlchemy le daría a la tabla, es una palabra reservada en PostgreSQL.

Por otro lado, cada columna de la tabla se define mediante un atributo de clase de tipo Column. Por defecto, el nombre que se le asigna a la columna es el nombre del atributo. Además, el primer argumento que se le pasa define el tipo de dicha columna. Las columnas que no admiten nulos se indicarán con el argumento nullable=False y aquellas que deban ser únicas, como el caso de la columna email, se especificarán con unique=True.

Guardando el modelo y haciendo consultas
En Flask-SQLALchemy, para guardar un objeto en base de datos, este debe estar previamente asociado al objeto session. Una vez asociado, para que los cambios se vean reflejados en la base de datos hay que hacer un commit. Todo esto se realiza en el método save() de la clase User.

Lo último que veremos en esta introducción a SQLAlchemy serán las consultas a base de datos. Por defecto, todos los objetos que heredan de la clase Model, disponen del objeto query, a través del cuál se realizan todas las consultas a base de datos. En nuestro caso, hemos definido la consulta para recuperar un usuario a partir de su id get_by_id y para recuperar un usuario a partir de su email get_by_email.

Flask SQLALchemy en acción
Una vez que hemos configurado el objeto SQLAlchemy y hemos definido nuestro modelo User, ya podemos integrar este en las diferentes vistas.

Lo primero que vamos a hacer es importar la clase User en el fichero run.py (ya la importamos en la lección anterior). En esta ocasión vamos a realizar una excepción al importar esta clase. El import lo declararemos justo después de inicializar el objeto db, ya que si no el intérprete se quejará de que no lo encuentra. Esto lo arreglaremos en la lección siguiente cuando explique los Blueprint. Por el momento, créete lo que te digo 😉

...
db = SQLAlchemy(app)
from models import User
Lo bueno que tiene hacer uso de una base de datos es que los datos son persistentes y perduran incluso tras reiniciar el servidor.

Cambios en la vista login()
El primer cambio que vamos a realizar es en la vista login(). En esta función comprobamos si existe un usuario dado un email. Pues bien, vamos a sustituir la llamada a la función get_user() (que ha sido eliminada) por la llamada al método get_by_email() de la clase User.

...
form = LoginForm()
if form.validate_on_submit():
    user = User.get_by_email(form.email.data)
    if user is not None and user.check_password(form.password.data):
        login_user(user, remember=form.remember_me.data)
        ...
Actualizamos la función load_user()
El segundo cambio será en la función load_user(), responsable de obtener un usuario a partir del id que había guardado en sesión. En esta ocasión sustituiremos la lógica de esta función por una simple llamada al método get_by_id() de la clase User:

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))
Creamos un objeto User en la vista de registro
Por último, vamos a actualizar la vista show_signup_form(), en la cuál se realiza el registro de los usuarios. Aquí realizaremos dos cambios. En primer lugar, antes de crear un usuario comprobaremos si ya existe uno con el mismo email, para devolver el error correspondiente. En segundo lugar, ya no guardaremos el usuario en la lista en memoria sino en la base de datos:

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)
Como puedes observar, la vista es muy similar a la que definimos en la lección anterior. ❗️ Fíjate en la variable error que se le pasa a la plantilla signup_form.html. Esta variable contiene un mensaje de error en caso de que ya exista un usuario con el email introducido en el formulario.

He actualizado la plantilla signup_form.html para que se muestre el error en caso de existir:

{% extends "base_template.html" %}
{% block title %}Registro de usuarios{% endblock %}
{% block content %}
    {% if error %}
        <p style="color: red;"><strong>Error:</strong> {{ error }}
    {% endif %}
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <div>
            {{ form.name.label }}
            {{ form.name(size=64) }}<br>
            {% for error in form.name.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </div>
        
        ...
Añadimos el modelo Post
Hasta aquí hemos actualizado toda la lógica que tiene que ver con los usuarios del blog pero todavía falta una parte importante del mismo: los posts. Del mismo modo que en las dos secciones anteriores, vamos a realizar los cambios oportunos para almacenar los posts en base de datos.

Lo primero será crear la clase Post en el fichero models.py:

from slugify import slugify
from sqlalchemy.exc import IntegrityError
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text)
    def __repr__(self):
        return f'<Post {self.title}>'
    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)
        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1
                self.title_slug = f'{slugify(self.title)}-{count}'
    def public_url(self):
        return url_for('show_post', slug=self.title_slug)
    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(title_slug=slug).first()
    @staticmethod
    def get_all():
        return Post.query.all()
Analicemos esta clase por partes:

Al igual que en la clase User, la clase Post define el atributo id como primary_key.
Se ha establecido una relación entre la clase Post y la clase User a través del atributo user_id. Este atributo es una clave ajena a la tabla blog_user, para referenciar al usuario que escribió el post.
El método save es más complejo que el de la clase User y te lo explicaré a continuación.
Se ha definido el método public_url() para obtener la url pública del post a partir del slug del título.
Como en la clase User, se han creado operaciones de consulta sobre los posts: get_by_slug() y get_all().
El método save()
En la clase Post el método save() difiere un poco del que vimos en la clase User. Básicamente, lo que haremos será generar el slug único del título de manera automática. Para ello, hago uso de la librería slugify.

Para instalar esta librería ejecuta en el terminal lo siguiente:

pip install python-slugify
Además, como el slug debe ser único, tratamos el error IntegrityError que se lanzará cada vez que se guarde un post pero haya uno con dicho slug. En este caso, lo único que haremos será añadirle un sufijo con el valor del contador count.

Actualizando las vistas que gestionan los posts
Ya estamos cerca del final. Del mismo modo que hicimos con las vistas relacionadas con los usuarios, en esta ocasión vamos a actualizar las vistas relacionadas con los posts.

Lo primero es importar la clase Post en el fichero run.py:

from models import User, Post
index()
Lo siguiente será actualizar la vista principal del blog, de manera que se recuperen todos los posts que haya en base de datos para mostrarlos en el listado:

@app.route("/")
def index():
    posts = Post.get_all()
    return render_template("index.html", posts=posts)
La plantilla index.html quedaría del siguiente modo:

{% extends "base_template.html" %}
{% block title %}Tutorial Flask: Miniblog{% endblock %}
{% block content %}
    <ul>
    {% for post in posts %}
        <li><a href="{{ post.public_url() }}">{{ post.title }}</a></li>
    {% endfor %}
    </ul>
{% endblock %}
show_post()
A continuación cambiaremos la implementación de la vista show_post():

@app.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("post_view.html", post=post)
Como puedes observar, lo primero que se hace es recuperar un post a partir del slug que se pasa como parámetro. En caso de que no exista ningún post, se devuelve un error 404 (lo que mostrará una página con dicho código de error). Por el contrario, si el post existe, se renderiza la vista post_view.html. En esta ocasión a la vista se le pasa la instancia del post y no solamente el slug.

La nueva plantilla post_view.html tendría el siguiente aspecto:

{% extends "base_template.html" %}
{% block title %}{{ post.title }}{% endblock %}
{% block content %}
    <h1>{{ post.title }}</h1>
    {{ post.content }}
{% endblock %}
post_form()
La última vista a modificar es post_form(). En esta ocasión, lo único que haremos será crear un objeto Post y llamar a su método save():

@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()
        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)
❗️ Ten en cuenta que se han borrado todas las referencias a title_slug, tanto del formulario PostForm como de la plantilla post_form.html. Recuerda que ahora este campo se genera de forma automática.

Creando la base de datos
Pues con todo esto ya tendríamos nuestro miniblog integrado con una base de datos. Aunque, seguro que te estás preguntando: «¿Cuándo se crean la base de datos y las tablas?».

Bien, la base de datos tendrás que crearla tú a mano y para crear las tablas, Flask-SQLAlchemy trae una utilidad que las genera automáticamente.

Una vez que hayas creado la base de datos, ejecuta lo siguiente desde un intérprete de Python:

>>> from run import db
>>> db.create_all()
Después de ejecutar estos comandos, verás que en tu base de datos se habrán creado las tablas blog_user y post.

Te has ganado una recompensa 💰 Es hora de jugar con la aplicación 😊

Conclusión
Y hasta aquí este tutorial. Creo que ha sido de los más intensos de los que llevamos hasta la fecha, pero la ocasión merecía un post especial y denso. En este artículo hemos visto los conceptos principales de Flask-SQLAlchemy y SQLAlchemy, por eso te recomiendo que le eches un ojo a los tutoriales oficiales de cada una de estas librerías para que entiendas todo más en profundidad.

En cualquier caso, si tienes alguna duda siempre puedes ponerte en contacto conmigo dejándome un mensaje al final del post, a través de mis redes sociales o enviándome un email. Estaré encantado de poder ayudarte.

🎯 Puedes descargar el código correspondiente a esta lección desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion5 -b leccion5

En el siguiente tutorial veremos cómo dividir una aplicación Flask en diferentes módulos por medio de los Blueprint.
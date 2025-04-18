Lección 6: Estructura de un proyecto Flask. Blueprints
Categoría: Flask
flask, medio, python, tutorial flask
Lección 6 Estructura de un proyecto Flask: Blueprints
Bueno amig@s, tras la resaca de las primeras lecciones, que creo que son las más duras, en esta lección vamos a bajar de revoluciones y me centraré en algo que muchos de vosotr@s me consultáis a menudo, sobre todo al principio, cuando estáis un poco más perdidos: Cómo definir la estructura de un proyecto Flask.

Y este es un aspecto importante que afecta al mantenimiento del proyecto, especialmente cuando trabajamos en equipo y crece en líneas de código. ¿Te imaginas el caos de tener todo el proyecto escrito en un solo fichero? No me gustaría tener que pelearme con el repositorio cada vez que tuviera que mergear mi código 😂

Por eso he creído conveniente desarrollar esta lección en este punto, cuando todavía la complejidad de nuestro blog no es desorbitada. En la guía principal de Flask o si haces una búsqueda en Google, la mayoría de ejemplos y tutoriales mencionan un fichero llamado app.py en el cuál está todo el código de la aplicación: la inicialización de la app y las extensiones, las vistas, los modelos, los formularios, métodos para crear la base de datos, … Pero esto no es funcional en la mayoría de las ocasiones.

💥 En esta lección aprenderás cómo estructurar tu proyecto de forma adecuada. Un proyecto con cierta complejidad. Un proyecto del mundo real. Te enseñaré la forma en que, personalmente, estructuro yo todos mis proyectos y que he aprendido a base de pelearme con el código.

Como siempre, retomaremos el tutorial donde lo dejamos en la lección anterior.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 5 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion5 -b leccion5

Índice
A continuación te muestro el índice de esta lección:

Estructura básica de un proyecto Flask
Dividiendo la aplicación en módulos
Cómo estructurar un proyecto Flask cuando crece: Blueprints
División estructural
División funcional
Estructura de un proyecto con Blueprints
La estructura que sigo yo en todos mis proyectos
Reorganizando nuestro miniblog con Blueprints
Estructura básica de un proyecto Flask
La estructura más sencilla de un proyecto Flask es tener toda la aplicación en un solo módulo (un fichero con código Python). Por convenio, dicho módulo es nombrado app.py Teniendo esto en cuenta, la estructura más simple que nos podemos encontrar es la siguiente:

+ mi_proyecto
|_ app.py
|_ static/
|_ templates/
A continuación te indico qué contiene cada uno de los elementos:

app.py: Contiene toda la lógica de la aplicación: inicialización de la app y las extensiones, vistas, modelos, formularios, etc.
static: Es un directorio con todos los recursos estáticos: CSS, Javascript, imágenes, …
templates: Contiene las plantillas de la web, es decir, los ficheros HTML/Jinja2.
Como te decía, esta estructura es válida si estamos haciendo pruebas con Flask o nuestro proyecto es muy simple: tiene dos o tres vistas, un modelo, un formulario… Pero en el mundo real, ¿esto cuándo ocurre?

Dividiendo la aplicación en módulos
Podemos pasar al siguiente nivel cuando nuestra aplicación crece en complejidad 😰 En este nivel lo que haremos será sacar parte del código del módulo app.py a otros módulos, de manera que el mantenimiento de la aplicación resulte más sencillo. Por ejemplo, un módulo para crear y arrancar la aplicación y definir las vistas, un módulo para los modelos, un módulo para los formularios, …

La estructura que propongo sería como sigue:

+ mi_proyecto
|_ app.py
|_ forms.py
|_ models.py
|_ static/
|_ templates/
Si te das cuenta, es la estructura que hemos seguido a lo largo de los diferentes tutoriales hasta ahora. En caso de que hayas seguido el tutorial sobre Flask paso a paso o hayas clonado el repositorio hasta la Lección 5, la estructura de tu proyecto debe ser similar a la siguiente:

Estructura proyecto Flask leccion5

Al igual que en el primer caso, esta estructura nos vale si el proyecto no es muy complejo y/o lo está desarrollando un solo programador. Personalmente, esta estructura me gusta más que la anterior. Me da la sensación de que todo está mejor ordenado. Sí, soy un maniático del orden 🤓

Pero como te decía, en mi día a día todavía no he desarrollado un proyecto tan pequeño como para que esta división me sea útil.

Cómo estructurar un proyecto Flask cuando crece: Blueprints
Pero Juanjo, ¿a qué te refieres con un proyecto del mundo real? Bien, la mayoría de aplicaciones web tienen una serie de requisitos que podemos agrupar funcionalmente: gestión de usuarios, parte pública, parte privada, panel de administración, envío de emails, envío de notificaciones push, API para las aplicaciones móviles, ejecución de tareas en background, … Cada una de estas partes puede ser vista como un módulo independiente de la aplicación (aunque es cierto que a veces estos módulos tienen dependencias entre sí).

En nuestro miniblog, veremos muchos de estos conceptos a lo largo de todas las lecciones. Por eso es preciso estructurar bien el proyecto. Como te decía, esto hará que sea más mantenible a la larga y que nos permita desarrollar en equipo.

¿Cómo podemos agrupar el miniblog en funcionalidades? Hasta ahora, los principales requisitos funcionales que hemos visto hacen referencia a gestión de usuarios, visualizar los posts por parte de los visitantes del blog y gestión privada de los posts por parte de los administradores.

Entonces, ¿cómo podemos organizar el código? En principio, de dos formas: siguiendo una división estructural o bien una división funcional a partir de componentes/módulos llamados Blueprints.

División estructural
Mediante una división estructural, lo que hacemos es agrupar el código por lo que hace, es decir, separar las vistas, plantillas, modelos, formularios, etc. en diferentes módulos. De este modo, una aplicación cualquiera tendría la siguiente estructura:

+ mi_proyecto/
   |_ app/
      |_ __init__.py
      |_ static/
      |_ templates/
         |_ public/
            |_ index.html
            |_ ...
         |_ users/
            |_ login.html
            |_ sign_up.html
            |_ ...
         |_ private/
            |_ index.html
         |_ ...
      |_ routes/
         |_ __init__.py
         |_ private.py
         |_ public.py
         |_ users.py
         |_ ...
      |_ models/
         |_ users.py
         |_ ...
      |_ forms/
         |_ users.py
         |_ ...
   |_ run.py
   |_ requirements.txt
   |_ ...
División funcional
Con una división funcional lo que hacemos es agrupar los distintos componentes según los requisitos funcionales. De esta forma, todas las vistas, plantillas, modelos, formularios, etc. de una parte relacionada de la aplicación se definen dentro de un mismo paquete:

+ mi_proyecto/
   |_ app/
      |_ __init__.py
      |_ public/
         |_ __init__.py
         |_ routes.py
         |_ static/
         |_ templates/
         |_ models.py
         |_ forms.py
         |_ ...
      |_ private/
         |_ __init__.py
         |_ routes.py
         |_ static/
         |_ templates/
         |_ models.py
         |_ forms.py
         |_ ...
      |_ users/
         |_ __init__.py
         |_ routes.py
         |_ static/
         |_ templates/
         |_ models.py
         |_ forms.py
         |_ ...
      |_ ...
      |_ static/
      |_ templates/
   |_ run.py
   |_ requirements.txt
   |_ ...
Yo personalmente suelo seguir esta última porque, a la larga, me parece que el código se estructura mejor, pero eres libre de optar por la que te sientas más cómod@.

Estructura de un proyecto con Blueprints
Una vez que hemos visto dos de las principales formas que existen para estructurar una aplicación, a continuación mostraré cómo podemos hacer esto en Flask a través de los Blueprints.

¿Qué es un Blueprint? Básicamente, un Blueprint define una colección de vistas, plantillas, recursos estáticos, modelos, etc. que pueden ser utilizados por la aplicación. Los usaremos siempre y cuando queramos organizar la aplicación en diferentes módulos. En nuestro caso, como ya hemos visto, la parte pública del blog, el panel de administración, la gestión de usuarios, … Cada una de estas partes la agruparemos en un Blueprint propio.

¿Cómo se usan los Blueprints?
Para usar un Blueprint siempre seguiremos los siguientes pasos: primero, creación e inicialización del Bluenprint; segundo, registro del Blueprint en la app.

Si tomamos como referencia el paquete public del ejemplo de la división funcional, la creación e inicialización del Blueprint se realiza en el fichero __init__.py:

# mi_proyecto/app/public/__init__.py
from flask import Blueprint
public = Blueprint('public', __name__, template_folder='templates', static_folder='static')
from . import routes
Como podemos observar, hemos importado la clase Blueprint para crear nuestro Blueprint public. Para ello, lo inicializamos con cuatro parámetros: un nombre; el nombre de la importación (este último suele ser el nombre del módulo, por eso he utilizado la variable __name__); y dado que hemos optado por una división funcional, hay que indicar el nombre de los directorios para las plantillas y los recursos estáticos en caso de que existieran. Si hubiéramos optado por una división estructural, estos dos últimos parámetros no hubieran sido necesarios. Además, hay que importar aquí todas las vistas del Blueprint para que la app sea consciente de que existen. Por eso la última línea.

Cuando hacemos uso de Blueprints, el decorador route para definir las URLs de las vistas se toma del objeto Blueprint y no de la app. Por tanto, en el fichero routes.py del Blueprint public, definiremos las vistas del siguiente modo:

# mi_proyecto/app/public/routes.py
from flask import render_template
from . import public
@public.route('/index'):
def index():
    # Nuestro código
    return render_template('...')
Por último hay que registrar el Blueprint en la app. El registro lo haremos en el módulo __init__.py del paquete app:

# mi_proyecto/app/__init__.py
from flask import Flask
app = Flask(__name__)
from .public import public
app.register_blueprint(public)
Y en principio, esto sería todo.

La estructura que sigo yo en todos mis proyectos
Y ahora te contaré un secreto: cuál es la estructura que sigo yo en todos mis proyectos Flask y qué significa cada elemento.

En líneas generales, todos mis proyectos siguen el siguiente patrón básico:

+ mi_proyecto/
   |_ app/
      |_ __init__.py
      |_ common/
      |_ mod1/
         |_ __init__.py
         |_ routes.py
         |_ templates/
            |_ mod1/
               |_ template1.html
               |_ template2.html
         |_ models.py
         |_ forms.py
         |_ ...
      |_ mod2/
         |_ __init__.py
         |_ routes.py
         |_ templates/
            |_ mod2/
               |_ template1.html
               |_ template2.html
         |_ models.py
         |_ forms.py
         |_ ...
      |_ ...
      |_ static/
         |_ css/
         |_ images/
         |_ js/
      |_ templates/
         |_ base_template.html
         |_ ...
   |_ config
      |_ development.py
      |_ local.py
      |_ production.py
      |_ testing.py
   |_ env/
   |_ fixtures/
   |_ instance
      |_ __init__.py
      |_ config.py
   |_ .gitignore
   |_ CHANGELOG.md
   |_ entrypoint.py
   |_ README.md
   |_ requirements.txt
A continuación explico qué significa cada uno de ellos:

app/	Es el paquete en el que reside toda la aplicación Flask.
app/__init__.py	Este fichero contiene métodos factoría para crear e inicializar la app y los distintos componentes y extensiones.
app/common	Este paquete contiene librerías y funciones comunes.
app/mod1	Este paquete hace referencia al Blueprint ‘mod1’.
app/mod1/__init__.py	Este fichero inicializa el Blueprint ‘mod1’.
app/mod1/routes.py	Este módulo contiene las vistas del Blueprint ‘mod1’.
app/mod1/templates/mod1	Este directorio contiene las páginas Jinja2 del Blueprint ‘mod1’. El subdirectorio ‘mod1’ existe para que no entren en conflicto páginas que se llamen igual entre diferentes Blueprints.
app/mod1/models.py	Este módulo contiene los modelos referentes al Blueprint ‘mod1’.
app/mod1/forms	Este módulo contiene los formularios referentes al Blueprint ‘mod1’.
app/static/	Este directorio contiene todos los recursos estáticos del proyecto. Yo no los suelo separar entre los distintos Blueprints sino que utilizo este directorio para incluirlos todos.
app/templates/	Este directorio contiene las plantillas Jinja2 que sirven de base y las comunes a todo el proyecto.
config/…	El directorio config contiene módulos con las variables de configuración de cada uno de los entornos de ejecución. Entraré en detalle en la Lección 7.
env/	Entorno de ejecución Python del proyecto.
instance/	Este directorio contiene variables de configuración del entorno de ejecución local y que no deben formar parte del repositorio de código. Por ejemplo, contraseñas personales. Entraré más en detalle en la Lección 7.
.gitignore	Este fichero define los directorios y ficheros que no deben ser tenidos en cuenta por Git.
CHANGELOG.md	Fichero en formato markdown en el que registro las funcionalidades y corrección de errores de cada versión.
entrypoint.py	Este fichero es el punto de entrada a la aplicación. En él se crea la aplicación y se lanza el servidor de desarrollo.
fixtures/	Este directorio contiene recursos que utilizo durante el desarrollo: test del API, ficheros SQL, …
README.md	Fichero en formato markdown en el que indico cosas a tener en cuenta para la ejecución de la aplicación.
requirements.txt	Este fichero contiene todas las dependencias Python del proyecto.
Reorganizando nuestro miniblog en Blueprints
Bueno, ha llegado el momento de poner en marcha todo lo aprendido. Vamos a reestructurar nuestro miniblog para dividir las funcionalidades desarrolladas hasta el momento en distintos módulos por medio de Blueprints. El resultado final será algo parecido a la estructura que te he enseñado en el apartado anterior.

Prácticamente no escribiremos nada de código, sino que pasaremos el contenido de los módulos run.py, models.py y forms.py actuales a la nueva estructura propuesta. Esta nueva estructura tendría el siguiente aspecto:

+ miniblog
|_ app
   |_ __init__.py
   |_ models.py
   |_ admin/
      |_ __init__.py
      |_ forms.py
      |_ routes.py
      |_ templates/
         |_ admin/
            |_ post_form.html
   |_ auth/
      |_ __init__.py
      |_ forms.py
      |_ models.py
      |_ routes.py
      |_ templates/
         |_ auth/
            |_ login_form.html
            |_ signup_form.html
   |_ public/
      |_ __init__.py
      |_ routes.py
      |_ templates/
         |_ public
            |_ index.html
            |_ post_view.html
   |_ static/
      |_ base.css
   |_ templates/
      |_ base_template.html
|_ env/
|_ .gitignore
|_ CHANGELOG.md
|_ entrypoint.py
|_ LICENSE
|_ README.md
|_ requirements.txt
Como puedes observar he optado por una división funcional en la que existen tres módulos (Blueprints): admin, para la gestión del blog; auth, para la gestión de los usuarios y public, para todo lo relacionado con la parte pública del blog.

¿Qué ha ocurrido con el código anterior? Intentaré resumirlo lo más brevemente posible. En la tabla siguiente tenemos dos columnas: la de la izquierda contiene los recursos del proyecto antes de la reestructuración, la columna de la derecha indica la correspondencia actual de dichos recursos.

run.py	entrypoint.py
app/__init__.py

app/admin/__init__.py

app/admin/routes.py

app/auth/__init__.py

app/auth/routes.py

app/public/__init__.py

app/public/routes.py

forms.py	app/admin/forms.py
app/auth/forms.py

models.py	app/auth/models.py
app/models.py

templates/index.html	app/public/templates/public/index.html
templates/login_form.html	app/auth/templates/auth/login_form.html
templates/admin/post_form.html	app/admin/templates/admin/post_form.html
templates/post_view.html	app/public/templates/public/post_view.html
templates/signup_form.html	app/auth/templates/auth/signup_form.html
app/admin/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Enviar')
app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length
class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')
app/auth/models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
class User(db.Model, UserMixin):
    __tablename__ = 'blog_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    def __init__(self, name, email):
        self.name = name
        self.email = email
    def __repr__(self):
        return f'<User {self.email}>'
    ...
app/models.py
from flask import url_for
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from app import db
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text)
    def __repr__(self):
        return f'<Post {self.title}>'
    ...
app/admin/__init__.py
from flask import Blueprint
admin_bp = Blueprint('admin', __name__, template_folder='templates')
from . import routes
❗️ Se crea e inicializa el Blueprint admin_bp con nombre admin.

app/admin/routes.py
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Post
from . import admin_bp
from .forms import PostForm
@admin_bp.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@admin_bp.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()
        return redirect(url_for('public.index'))
    return render_template("admin/post_form.html", form=form)
❗️ En la vista post_form debemos prestar atención a las modificaciones de las dos últimas líneas:

Ahora el nombre de la vista que se pasa como parámetro a la función url_for incluye el nombre del Blueprint del que forma parte. En este caso public (es el primer parámetro que se le pasa al constructor de la clase Blueprint).
En esta ocasión a la función render_template se le indica el subdirectorio en el que se encuentra la plantilla post_form.html.
❗️Ambos cambios han sido aplicados respectivamente en todo el proyecto según correspondía para el resto de casos.

app/auth/__init__.py
from flask import Blueprint
auth_bp = Blueprint('auth', __name__, template_folder='templates')
from . import routes
app/auth/routes.py
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import login_manager
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User
@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    ...
    return render_template("auth/signup_form.html", form=form, error=error)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    ...
    return render_template('auth/login_form.html', form=form)
@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))
app/public/__init__.py
from flask import Blueprint
public_bp = Blueprint('public', __name__, template_folder='templates')
from . import routes
app/public/routes.py
from flask import abort, render_template
from app.models import Post
from . import public_bp
@public_bp.route("/")
def index():
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)
@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("public/post_view.html", post=post)
app/__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
login_manager = LoginManager()
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testing@localhost:5432/miniblog'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)
    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    from .public import public_bp
    app.register_blueprint(public_bp)
    return app
En este módulo se define un método factoría para crear la app, inicializar las diferentes extensiones y registrar los blueprints. A diferencia de cómo lo hacíamos hasta ahora, los métodos factoría nos permiten configurar diferentes apps a partir del mismo proyecto inicializando diferentes extensiones y registrando distintos Blueprints.

❗️¡OJO!: Al incluirla en un Blueprint, recuerda actualizar la vista login_view a auth.login.

entrypoint.py
from app import create_app
app = create_app()
Este módulo es el encargado de crear la aplicación Flask. Dado que contiene la instancia de la aplicación, será el punto de entrada del servidor.

Conclusión
En el tutorial hemos visto distintas formas de estructurar una aplicación Flask en función de las necesidades de la misma. Flask permite la división de una aplicación en módulos por medio de los Blueprints.

Como recomendación personal, la estructura que aquí te he explicado es el resultado de muchas horas de desarrollo y puesta en producción de aplicaciones. Es solo una guía que puedes tomar como base y adaptar a tus propias necesidades. Lo que sí que pienso es que, a menos que sea un proyecto de pruebas o que sea muy básico, no debes optar por la estructura básica sino por una división funcional o estructural. Esto te ayudará a ser más productivo y a trabajar mejor en equipo. Además, si tu proyecto crece, será mucho más fácil añadir nuevas funcionalidades.

En cualquier caso, si tienes alguna duda siempre puedes ponerte en contacto conmigo dejándome un mensaje al final del post, a través de mis redes sociales o enviándome un email. Estaré encantado de poder ayudarte.

🎯 Puedes descargar el código correspondiente a esta lección desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion6 -b leccion6

En el siguiente tutorial veremos cómo configurar una aplicación Flask en función del entorno de ejecución.
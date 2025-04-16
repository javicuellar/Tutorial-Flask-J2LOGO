Lección 4: Login de usuarios en Flask
Categoría: Flask
flask, medio, python, tutorial flask
login-usuarios-flask
En este punto del tutorial las cosas ya comienzan a ponerse interesantes. Ha llegado la hora de implementar uno de los aspectos clave en cualquier aplicación web: el login de usuarios. El control de acceso a nuestra aplicación debe implementarse adecuadamente, ya que, en gran medida, de él depende parte de la seguridad de nuestra aplicación. Pero no te preocupes, como verás, hacer el login de usuarios en Flask es muy sencillo.

En esta lección crearemos nuestro modelo que representa a los usuarios de la aplicación y el formulario de login. También veremos cómo hacer login en Flask y cómo proteger ciertas vistas de aquellos usuarios que no se han autenticado.

Continuaremos por donde lo dejamos en la lección anterior, en la que te expliqué cómo usar formularios en Flask. De hecho repasaremos parte de esa lección ya que tendremos que añadir el formulario de login al blog.

En fin, ya no te entretengo más y doy paso a la acción 😉

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 3 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion3 -b leccion3

Índice
A continuación te muestro el índice de esta lección:

Introducción a Flask-login
Crear el modelo User
La función para cargar el modelo
Login de usuarios
Logout
Personalizando el login
Protegiendo las vistas
Mostrando la información del usuario logueado en las plantillas
Introducción a Flask-login
Para implementar el login de usuarios en Flask haremos uso de una conocida extensión llamada Flask-login. Siempre que se pueda, no hay que reinventar la rueda y esta extensión nos facilitará mucho la vida. ¿Qué nos ofrece Flask-login? Entre otras cosas:

Almacenar el ID del usuario en la sesión y mecanismos para hacer login y logout.
Restringir el acceso a ciertas vistas únicamente a los usuarios autenticados.
Gestionar la funcionalidad Recuérdame para mantener la sesión incluso después de que el usuario cierre el navegador.
Proteger el acceso a las cookies de sesión frente a terceros.
El primer paso para usar Flask-login en nuestra aplicación será instalarla. Para ello, ejecutaremos en la consola lo siguiente:

pip install flask-login
Una vez instalada, debemos crear una instancia de la clase LoginManager, la cuál debe ser accesible desde cualquier punto de nuestra aplicación. Esta clase contiene la lógica para cargar un usuario a partir del ID guardado en la sesión o redirigir a los usuarios que no están autenticados a la página de login cuando intentan acceder a una vista protegida.

Dado que Flask-login hace uso de la sesión para la autenticación, debemos establecer la variable de configuración SECRET_KEY. Como recordarás, esto ya lo hicimos en la lección anterior.

Vamos a crear un objeto de la clase LoginManager que llamaremos login_manager. Abre el fichero run.py y justo después de instanciar la app añade lo siguiente:

...
from flask_login import LoginManager
...
app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
login_manager = LoginManager(app)
...
Con esto habremos dado el primer paso para que los usuarios puedan hacer login en nuestra aplicación Flask.

Crear el modelo User
Lo siguiente que haremos será crear la clase User. Esta clase representa a los usuarios de nuestra aplicación. Además, contiene toda la lógica para crear usuarios, guardar las contraseñas de modo seguro o verificar los passwords.

Un punto a favor de la extensión Flask-login es que te da libertad para definir tu clase para los usuarios. Esto hace posible que se pueda utilizar cualquier sistema de base de datos y que modifiquemos el modelo en función de las necesidades que vayan surgiendo. El único requisito indicado por Flask-login es que la clase usuario debe implementar las siguientes propiedades y métodos:

is_authenticated: una propiedad que es True si el usuario se ha autenticado y False en caso contrario.
is_active: una propiedad que indica si la cuenta del usuario está activa (True) o no (False). Es decisión tuya definir qué significa que una cuenta de usuario está activa. Por ejemplo, se ha verificado el email o no ha sido eliminada por un administrador. Por defecto, los usuarios de cuentas inactivas no pueden autenticarse.
is_anonymous: una propiedad que vale False para los usuarios reales y True para los usuarios anónimos.
get_id(): un método que devuelve un string (unicode en caso de Python 2) con el ID único del usuario. Si el ID del usuario fuera int o cualquier otro tipo, es tu responsabilidad convertirlo a string.
De nuevo, Flask-login ha pensado en nosotros ya que pone a nuestra disposición la clase UserMixin con una implementación por defecto para todas estas propiedades y métodos. Tan solo tenemos que heredar de ella en nuestra propia clase User.

Con esto en mente, crea un nuevo fichero llamado models.py en el directorio raíz del proyecto y añade la clase siguiente:

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class User(UserMixin):
    def __init__(self, id, name, email, password, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return '<User {}>'.format(self.email)
Cómo guardar las contraseñas
Quiero resaltar en este punto que las contraseñas de los usuarios no las guardaremos en claro. Esto sería un problema de seguridad. En su lugar, guardaremos un hash del password. Para ello, nos valdremos de la librería werkzeug.security, aunque puedes usar cualquier otra (siempre que sea segura).

Para verificar la contraseña, hemos definido el método check_password que comprueba si el hash del parámetro password coincide con el del usuario.

Listado de usuarios
Como ha sucedido en otras lecciones anteriores, todavía no guardaremos los usuarios en base de datos (lo veremos por fin en la siguiente lección 🎉). En su lugar, haremos uso de una lista de usuarios almacenada en memoria que llamaremos users (esto no es útil ya que los usuarios que guardemos se borrarán al reiniciar el servidor pero nos servirá para esta lección).

Añade lo siguiente después de la clase User:

users = []
def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None
La función get_user la utilizaremos provisionalmente para buscar un usuario por su email dentro de la lista users.

La función para cargar el modelo
¿Cómo podemos acceder en nuestro código al usuario cuyo ID se encuentra almacenado en sesión? Fácil, implementando un callback que será llamado por el método user_loader del objeto login_manager. ¿Recuerdas que definimos este objeto al principio?

El callback toma como parámetro un string con el ID del usuario que se encuentra en sesión y debe devolver el correspondiente objeto User o None si el ID no es válido. No lances una excepción si no puedes devolver un usuario a partir del ID.

Añadamos nuestro callback al final del fichero run.py:

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None
users hace referencia a la lista de usuarios que definimos en el módulo models.py. Recuerda importarla previamente antes de hacer uso de ella.

from models import users
Login de usuarios
Bueno, ya lo tenemos todo preparado para poder hacer el login 💪🏻😜

Ahora toca el turno de crear el formulario para que los usuarios de nuestro blog se puedan autenticar (para poder comentar los posts). Vamos a dividir este proceso en tres fases: crear la clase del formulario, crear la plantilla HTML e implementar la vista que realiza el login.

Clase para el formulario de login
A estas alturas ya eres todo un expert@ en la materia, por tanto no voy a entrar mucho en detalle de cómo crear una clase que representa un formulario.

Abre el fichero forms.py y añade el código siguiente al final del mismo:

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')
El campo remember_me es de tipo BooleanField. Deberás importarlo junto al resto de tipos que importamos en la lección anterior. Lo utilizaremos para dar la posibilidad al usuario de mantener la sesión incluso después de cerrar el navegador.

Plantilla HTML para el formulario
Crea una nueva página HTML llamada login_form.html dentro de la carpeta templates del proyecto.

El contenido de la misma será el siguiente:

{% extends "base_template.html" %}
{% block title %}Login{% endblock %}
{% block content %}
    <div>
        <form action="" method="post" novalidate>
            {{ form.hidden_tag() }}
            <div>
                {{ form.email.label }}
                {{ form.email }}<br>
                {% for error in form.email.errors %}
                <span style="color: red;">{{ error }}</span>
                {% endfor %}
            </div>
            <div>
                {{ form.password.label }}
                {{ form.password }}<br>
                {% for error in form.password.errors %}
                <span style="color: red;">{{ error }}</span>
                {% endfor %}
            </div>
            <div>{{ form.remember_me() }} {{ form.remember_me.label }}</div>
            <div>
                {{ form.submit() }}
            </div>
        </form>
    </div>
    <div>¿No tienes cuenta? <a href="{{ url_for('show_signup_form') }}">Regístrate</a></div>
{% endblock %}
Como puedes comprobar es muy similar a la página que definimos para el registro.

La vista para realizar el login
Por último, debemos implementar la vista que muestre el formulario de login y compruebe si las credenciales proporcionadas por el usuario son válidas o no. Añade la siguiente función al final del fichero run.py:

from werkzeug.urls import url_parse
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)
Voy a ir desgranando poco a poco lo que hace esta vista:

En primer lugar comprobamos si el usuario actual ya está autenticado. Para ello nos valemos de la instancia current_user de Flask-login. El valor de current_user será un objeto usuario si este está autenticado (el que se obtiene en el callback user_loader) o un usuario anónimo en caso contrario. Si el usuario ya está autenticado no tiene sentido que se vuelva a loguear, por lo que lo redirigimos a la página principal.
A continuación comprobamos si los datos enviados en el formulario son válidos. En ese caso, intentamos recuperar el usuario a partir del email con get_user().
Si existe un usuario con dicho email y la contraseña coincide, procedemos a autenticar al usuario llamando al método login_user de Flask-login.
Por último comprobamos si recibimos el parámetro next. Esto sucederá cuando el usuario ha intentado acceder a una página protegida pero no estaba autenticado. Por temas de seguridad, solo tendremos en cuenta dicho parámetro si la ruta es relativa. De este modo evitamos redirigir al usuario a un sitio fuera de nuestro dominio. Si no se recibe el parámetro next o este no contiene una ruta relativa, redirigimos al usuario a la página de inicio.
También he realizado unas pequeñas modificaciones en la vista que realiza el registro para ir añadiendo a los usuarios registrados a la lista users. Puedes ver los cambios a continuación:

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, name, email, password)
        users.append(user)
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("signup_form.html", form=form)
Si has seguido todos los pasos hasta aquí, ya tendrías implementado un sistema de login en Flask. Sin embargo, todavía podemos mejorar el proceso. Para saber cómo, sigue leyendo hasta el final 😊

Logout
Como en cualquier aplicación web, debemos dar la oportunidad a los usuarios de cerrar la sesión en la misma. Esto lo conseguimos añadiendo una nueva vista en el fichero run.py:

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
Personalizando el login
Si no queremos que la aplicación muestre un error 401 cuando un usuario intenta acceder a una vista protegida, hay que personalizar el objeto login_manager. En este caso, lo que haremos será indicarle cuál es la vista para realizar el login.

Añade lo siguiente después de crear el objeto login_manager:

login_manager = LoginManager(app)
login_manager.login_view = "login"
...
Ahora el usuario será redirigido a la página de login en lugar de ver el error 401.

Protegiendo las vistas
Como indiqué al inicio del tutorial, solo los usuarios administradores pueden crear entradas en el blog. Por tanto, la vista post_form debe ser accesible solo por este tipo de usuarios. Todavía es pronto para ver cómo hacer esto pero realizaremos una primera aproximación.

Un usuario administrador debe estar autenticado para poder crear entradas. La manera en que Flask-login permite proteger el acceso a las vistas solo a los usuarios autenticados es a través del decorador @login_required.

Vamos a añadirlo a la vista post_form:

@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
...
Puedes comprobar que si no estás autenticado e intentas acceder, la aplicación te redirigirá a la página de login.

Mostrando la información del usuario logueado en las plantillas
Por último nos queda jugar con la información del usuario, tanto si está registrado como si no. Vamos a crear un menú superior para el blog en el que se muestre el nombre del usuario en caso de estar autenticado o un enlace para loguearse en caso contrario.

Abre la plantilla base_template.html y añade lo siguiente:

...
<body>
<div>
    <ul class="user-info">
        <li><a href="{{ url_for('index') }}">Home</a></li>
        {% if current_user.is_anonymous %}
            <li><a href="{{ url_for('login') }}">Login</a></li>
            <li> | </li>
            <li><a href="{{ url_for('show_signup_form') }}">Registrar</a></li>
        {% else %}
            <li>{{ current_user.name }}</li>
            <li> | </li>
            <li><a href="{{ url_for('logout') }}">Logout</a></li>
        {% endif %}
    </ul>
</div>
{% block content %}{% endblock %}
</body>
...
Los estilos de la clase user-info son:

.user-info {
    list-style: none;
    margin: 0;
    padding: 0;
}
.user-info li {
    display: inline-block;
    margin: 0;
    padding: 0 10px 0 0;
}
Añádelos al final del fichero de estilos base.css.

Y ahora sí, podemos dar por terminada esta lección del tutorial. Espero que te haya gustado 😊

Conclusión
Como habrás podido comprobar, el login de usuarios es una cuestión delicada e importante y no hay que tomársela a la ligera. Por suerte, podemos hacer uso de la extensión Flask-login que nos facilita mucho las cosas, aunque eres libre de intentar hacer tu propio sistema de login siguiendo los principales aspectos comentados en esta lección.
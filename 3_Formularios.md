Lección 3: Uso de formularios en Flask
Categoría: Flask
flask, medio, python, tutorial flask
En esta lección del tutorial te mostraré cómo integrar formularios web en una aplicación Flask. Los formularios son una parte muy importante de cualquier aplicación. A través de los formularios los usuarios pueden interactuar con la aplicación enviando cualquier tipo de información al servidor. Por ejemplo, gracias a ellos, un usuario se puede autenticar en una web, puede realizar una reserva o puede añadir un producto al carro de la compra.

A lo largo de esta entrada del blog aprenderás lo sencillo que es usar formularios en Flask. Para ello, siguiendo con nuestro ejemplo del tutorial (que te recuerdo que es desarrollar un miniblog), crearemos los siguientes formularios:

Un formulario para que los usuarios invitados se puedan registrar en el blog.
Un formulario para que el administrador pueda crear nuevas entradas en el blog.
Vamos a retomar el código donde lo dejamos en la lección anterior, en la que vimos cómo usar plantillas para generar las páginas HTML. Seguramente, en este capítulo tendremos que crear alguna que otra plantilla más, pero eso no será un problema para ti 😉

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 2 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion2 -b leccion2

Índice
A continuación te muestro el índice de esta lección:

Normalmente los formularios se envían en el cuerpo de la petición
Accediendo a los datos de una petición en Flask
Procesando los formularios al desnudo
Manejando los formularios con Flask-WTF
Normalmente los formularios se envían en el cuerpo de la petición
El protocolo HTTP define una serie de métodos de petición, conocidos como «verbos HTTP», para indicar la acción que se desea realizar sobre un recurso determinado. Cada uno de estos verbos tiene una semántica diferente, siendo los más comunes los métodos GET y POST.

GET debe emplearse para solicitar un recurso, por lo tanto, las peticiones realizadas con este método solo deben recuperar datos (y no modificarlos).

En cambio POST se utiliza para enviar una entidad a un recurso específico, de manera que se envían datos al servidor donde son procesados. Es por ello que, por regla general, siempre que necesitemos enviar datos a un servidor para ser manipulados lo haremos a través del método POST (esto es una simplificación de por qué enviar los datos usando POST).

Vaya un rollo te he acabo de soltar 🤷🏻‍♂️😆 Te estarás preguntando el por qué de esta introducción. Simplemente para que tengas claros estos conceptos, ya que son necesarios a la hora de manejar formularios.

El formulario de registro de usuarios
Bueno, ha llegado el momento de ponernos con lo que más nos gusta: programar. Vamos a comenzar por implementar el formulario de registro de usuarios.

Para ello, lo primero que vamos a hacer es crear una nueva plantilla en el directorio templates. Llamaremos a esta plantilla signup_form.html y su contenido será el siguiente:

{% extends "base_template.html" %}
{% block title %}Registro de usuarios{% endblock %}
{% block content %}
    <form action="" method="post">
        <label for="name">Nombre: </label>
        <input type="text" id="name" name="name" /><br>
        <label for="email">Email: </label>
        <input type="text" id="email" name="email" /><br>
        <label for="password">Contraseña: </label>
        <input type="password" id="password" name="password" /><br>
        <input type="submit" id="send-signup" name="signup" value="Registrar" />
    </form>
{% endblock %}
Del código anterior destacaría tres cosas:

La plantilla hereda de la plantilla base de nuestro proyecto.
Para crear un formulario en HTML se usa la etiqueta form. En el atributo action se indica la URL a la que se enviarán los datos del formulario. Si este campo se deja vacío la URL será la misma desde la que se descargó el recurso. En el atributo method indicamos el método a usar al enviar el formulario. En este caso POST, como te dije en el apartado anterior.
Para procesar posteriormente los campos del formulario, se debe indicar el nombre con el que los identificará el servidor a través del atributo name.
Lo siguiente que haremos para mostrar el formulario y procesarlo será añadir una nueva vista al final del fichero run.py que estará asociada a la URL /signup/:

@app.route("/signup/")
def show_signup_form():
    return render_template("signup_form.html")
Como vemos, esta vista lo único que hace es mostrar la plantilla que contiene el formulario.

Si accedemos a la dirección http://localhost:5000/signup/, veremos el formulario en el navegador:

Formulario de registro

Si intentamos enviar el formulario pulsando sobre el botón Registrar, nos encontraremos con el siguiente error:

Method not allowed

¿Por qué? Esto es así porque en Flask, por defecto, cualquier vista solo responde ante peticiones GET. Si queremos responder ante otro tipo de peticiones, debemos indicarlo en el parámetro methods del decorador route:

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    return render_template("signup_form.html")
Ahora nuestra vista acepta peticiones POST. No obstante, por el momento, en cualquiera de los dos casos siempre se mostrará el formulario de registro.

Accediendo a los datos de una petición en Flask
Antes de seguir con una de las partes más importantes de este tutorial, procesar los datos del formulario para su manipulación, quiero introducirte el objeto request de Flask.

Básicamente, el objeto request contiene toda la información que el cliente (por ejemplo el navegador web) envía al servidor, en nuestro caso, nuestra aplicación Flask. Entre esta información se encuentran las cabeceras HTTP, los parámetros de la URL, la codificación preferida y, cómo no, los datos que se envían a través de un formulario.

Imaginemos que tenemos la siguiente URL en nuestro blog /?page=1&list=10. Como vimos, la URL / del miniblog listaba todos los post. Los parámetros page y list los podríamos utilizar para paginar el listado, de manera que en este caso estamos pidiendo la primera página y los primeros diez post. ¿Cómo procesamos esto en nuestra vista? Accediendo al atributo args del objeto request del siguiente modo:

from flask import request
@app.route("/")
def index():
    page = request.args.get('page', 1)
    list = request.args.get('list', 20)
    ...
Los campos enviados a través de un formulario se acceden por medio del atributo form del objeto request.

Procesando los formularios al desnudo
Bien, continuemos, ahora sí, procesando los datos enviados a través del formulario de registro.

Todavía los datos que obtengamos de los formularios no serán guardados en ningún sistema persistente, como puede ser una base de datos. Esto lo veremos en la Lección 5, Añadiendo una base de datos: SQLAlchemy.

Vamos a modificar la vista show_signup_form() como indico a continuación (recuerda importar el objeto request del módulo flask):

from flask import render_template, request, redirect, url_for
@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))
    return render_template("signup_form.html")
¿Qué destacaríamos del código anterior?

La primera línea de código de la vista show_signup_form() accede al atributo method del objeto request. Esto nos permite identificar si el cliente ha enviado los datos del formulario (POST) o, por el contrario, quiere mostrar el formulario de registro (GET)
Si se ha enviado el formulario, se recupera cada uno de los campos del mismo por medio del diccionario form del objeto request. Recuerda que el nombre de los campos es aquel que indicamos con el atributo name en la plantilla del formulario de registro.
Luego comprobamos si se pasó por la URL el parámetro next. Este parámetro lo usaremos para redirigir al usuario a la página que se indica en el mismo. Si no se especifica, simplemente lo redirigimos a la página de inicio.
En caso de que no se haya enviado el formulario, se devuelve como respuesta la página que muestra el formulario de registro.
Siempre que se procesa un formulario correctamente, es una buena práctica hacer un redirect para evitar envíos duplicados de datos si el usuario recarga la página o hace clic en el botón atrás del navegador.
Como vemos, el procesamiento del formulario es muy sencillo y, en la mayoría de los casos, seguirá el patrón definido aquí. Sin embargo, hemos dejado muchos cabos sueltos. Por ejemplo: ¿qué debe ocurrir si un usuario no introduce su nombre? ¿Y si el email no es en realidad un email? Ante estas situaciones debemos validar siempre los campos del formulario y, en caso de detectar algún error, se lo debemos indicar al usuario.

Como puedes comprobar, la cosa se complica y el código de nuestra vista se «ensuciaría» añadiendo todas las validaciones necesarias.

No te preocupes, la mayoría de problemas en esta vida tienen solución. La nuestra se llama WTForms. Concretamente Flask-WTF. Flask-WTF es una extensión de Flask basada en WTForms que nos ayudará con el manejo de formularios en nuestra aplicación. Las extensiones permiten ampliar las funcionalidades base que trae por defecto Flask. Existen muchas de ellas y son de gran utilidad, por ejemplo, para manejo de bases de datos SQL, para la internacionalización o para la creación de APIs. Según avancemos en el tutorial sobre Flask veremos algunas de ellas. Por el momento, nos centraremos en Flask-WTF.

Manejando los formularios con Flask-WTF
Lo primero que hay que hacer en una aplicación Flask antes de usar cualquier extensión es instalarla en el sistema, en nuestro caso, en el entorno Python del proyecto.

Para instalar la extensión Flask-WTF, activa el entorno y ejecuta lo siguiente en el terminal:

pip install Flask-WTF
pip install email-validator
Una vez instalada, debemos hacer una serie de cambios en el proyecto. Los veremos a continuación paso a paso 💪🏻

Formulario de registro usando Flask-WTF
Al usar Flask-WTF, todo formulario se representa a través de una clase. Esta clase hereda del objeto FlaskForm y en ella se definen los campos del formulario como variables de clase.

SignupForm
Vamos a crear el formulario de registro tomando como referencia el formulario que implementamos en el apartado anterior. Añade un nuevo fichero al proyecto llamado forms.py al mismo nivel que run.py:

/tutorial-flask
|_/env
|_/static
|_forms.py
|_run.py
|_...
En el fichero forms.py vamos a crear la clase SignupForm:

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')
Como te indiqué, la clase SignupForm hereda de FlaskForm. Además, cada uno de los campos del formulario se ha definido como una variable de clase de un tipo específico (los tipos de los campos están definidos en el módulo wtforms, échale un ojo para ver todos los que hay). Esto hace que posteriormente el campo se renderice correctamente en la plantilla en función del tipo con el que lo hayamos declarado. El primer parámetro que le pasamos al campo es el nombre con el que se mostrará al usuario. Opcionalmente pasamos también un listado de validadores a cada campo, por ejemplo, para comprobar que los campos obligatorios no se dejan vacíos (DataRequired()), restringir la longitud de los mismos (Lenth()) o comprobar si una cadena de texto es realmente un email (Email()). Existen muchos más validadores y puedes definir los tuyos propios, pero esto lo veremos en otra ocasión.

La plantilla para el formulario SignupForm
El siguiente paso será actualizar la plantilla signup_form.html que creamos en el apartado anterior para que haga uso de la clase SignupForm.

{% extends "base_template.html" %}
{% block title %}Registro de usuarios{% endblock %}
{% block content %}
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <div>
            {{ form.name.label }}
            {{ form.name(size=64) }}<br>
            {% for error in form.name.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </div>
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
        <div>
            {{ form.submit() }}
        </div>
    </form>
{% endblock %}
El cambio principal con respecto la versión anterior es que esta plantilla espera un objeto de la clase SignupForm, que hemos instanciado en la vista correspondiente, y lo hemos llamado form. Dicho objeto contiene los campos del formulario y sabe cómo renderizarlos. En nuestro ejemplo dejamos a Flask-WTF que renderice la etiqueta de cada campo con form.<nombre_campo>.label y que genere el código del propio campo con form.<nombre_campo>.

Además, tras insertar cada campo recorremos el diccionario errors para mostrar al usuario los posibles errores de validación que haya en el mismo.

Para evitar que el navegador valide los campos por nosotros y delegar esta tarea a nuestra clase, hemos añadido el atributo novalidate a la etiqueta del formulario.

Por último, un detalle que requiere una mención especial es la línea {{ form.hidden_tag() }}. Esto lo que hace es añadir todos los campos tipo hidden del formulario si los hubiera. Por defecto, Flask-WTF genera para todas las instancias de la clase FlaskForm un campo oculto que contiene un token y sirve para proteger nuestra aplicación contra ataques CSRF.

Para poder generar este token es necesario definir un parámetro de configuración a nivel de aplicación llamado SECRET_KEY, cuyo valor debe ser un secreto de tipo string.

Por el momento, y para no complicarnos, modifica la línea del fichero run.py en la que instancias la aplicación Flask y sustitúyela por lo siguiente:

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
En lecciones posteriores veremos qué es el diccionario config del objeto app. El valor de SECRET_KEY puede ser diferente al que te muestro arriba (recuerda que nadie lo sepa). Si quieres saber cómo generar claves secretas en Python haz clic aquí.

No te recomiendo que desactives esta funcionalidad.

La vista para procesar el formulario SignupForm
Por último, vamos a modificar la vista show_signup_form(). Realmente los cambios a realizar son muy pocos:

from forms import SignupForm
@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))
    return render_template("signup_form.html", form=form)
En este caso lo primero que hacemos es instanciar un objeto de la clase SignupForm(). Al hacer esto pueden ocurrir dos cosas en función de si la petición es GET o POST. Si el usuario simplemente ha accedido a la página que muestra el formulario de registro (GET), se crea un objeto con los campos vacíos. Por el contrario, si el usuario ha enviado el formulario (POST), se crea un objeto con los campos inicializados. El valor de estos campos es el que se envía en el cuerpo de la petición (recuerda que están en request.form).

Una vez instanciado el formulario, se llama al método validate_on_submit(). Este método comprueba por nosotros que se ha enviado el formulario y que todos sus campos son válidos. En ese caso, podemos procesar nuestro formulario sin problema (la estructura del código es la misma que en el apartado anterior). Si no, devolvemos la plantilla que muestra el formulario (y en caso de que haya errores de validación se mostrarán al usuario).

Extenso pero fácil, ¿no? Te dejo unos instantes para que reflexiones y a continuación repetiré lo mismo para el formulario que nos permitirá dar de alta nuevas entradas en el blog. En este caso no entraré mucho en detalle, dado que los pasos a seguir son los mismos que para el formulario de registro.

Formulario para dar de alta entradas en el blog
Como en el ejemplo anterior, comenzaremos por implementar el formulario para dar de alta entradas en el blog.

PostForm
Nos situaremos al final del fichero forms.py y añadiremos la clase PostForm:

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título slug', validators=[Length(max=128)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Enviar')
En este caso he usado el tipo de campo TextAreaField para tener un campo de texto apropiado con el que editar el contenido de la entrada.

La plantilla para el formulario PostForm
A continuación modificaremos la plantilla post_form.html que creamos en la lección 2 y que se encuentra en el directorio templates/admin:

{% extends "base_template.html" %}
{% block title %}
    {% if form.title.data %}
        {{ form.title.data }}
    {% else %}
        Nueva entrada
    {% endif %}
{% endblock %}
{% block content %}
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <div>
            {{ form.title.label }}
            {{ form.title(size=128) }}<br>
            {% for error in form.title.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </div>
        <div>
            {{ form.title_slug.label }}
            {{ form.title_slug(size=128) }}<br>
            {% for error in form.title_slug.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </div>
        <div>
            {{ form.content.label }}
            {{ form.content }}<br>
            {% for error in form.content.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </div>
        <div>
            {{ form.submit() }}
        </div>
    </form>
{% endblock %}
Puedes comprobar que es muy similar a la del formulario de registro.

La vista para procesar el formulario PostForm
Por último, actualizaremos la vista post_form() para procesar el formulario. En caso de que no haya ningún error, aprovecharemos para crear un post y guardarlo en la variable en memoria posts.

from forms import SignupForm, PostForm
@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data
        post = {'title': title, 'title_slug': title_slug, 'content': content}
        posts.append(post)
        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)
Como ves, he seguido la misma filosofía que al procesar el formulario de registro.

¿Quieres probar el código?
A estas alturas del tutorial ya podemos empezar a jugar con el código de la aplicación. Para que veas que todo funciona he realizado unas modificaciones de manera que veas los títulos de los posts en la página de inicio.

Actualiza la vista index() para pasarle a la plantilla la variable que contiene los posts:

@app.route("/")
def index():
    return render_template("index.html", posts=posts)
Y modifica la plantilla index.html para que muestre los títulos de cada uno de los post que hay en memoria:

{% extends "base_template.html" %}
{% block title %}Tutorial Flask: Miniblog{% endblock %}
{% block content %}
    <ul>
    {% for post in posts %}
        <li>{{ post.title }}</li>
    {% endfor %}
    </ul>
{% endblock %}
Con esto, damos por terminada esta lección del tutorial. Espero que te haya gustado 😊

Conclusión
Si has llegado hasta aquí te doy las gracias 🤗. Ha sido una lección intensa pero muy productiva. En ella hemos repasado conceptos de HTML, cómo crear un formulario y cómo procesarlo. Después, he dado una pequeña introducción al objeto request de Flask. Finalmente hemos instalado la extensión Flask-WTF para facilitarnos el manejo de formularios. Como resultado, ya podemos jugar con la aplicación gracias a los formularios de registro y edición de posts. Te espero en la siguiente lección 😉
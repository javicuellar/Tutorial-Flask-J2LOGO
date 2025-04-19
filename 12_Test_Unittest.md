Lección 12: Tests con Flask y unittest
Categoría: Flask
flask, medio, python, tutorial flask
Lección 12 Tests con Flask
A estas alturas del tutorial ya tenemos el blog en un estado bastante avanzado. Realmente, las funcionalidades desarrolladas cubren todos los requisitos definidos en la introducción. Pero todavía nos quedan cosas importantes que descubrir, como en esta lección, en la que veremos cómo implementar tests con Flask.

De hecho, los tests deberían ser una de las partes fundamentales de nuestro código. Podría haber comenzado el tutorial por aquí, ya que es una buena práctica crear primero los tests y después el código que pasa esos tests, pero no habrías entendido nada…

¿Por qué son importantes los tests? Fundamentalmente porque podemos introducir cambios en nuestro código asegurándonos, en cierta manera, de que todo sigue funcionado correctamente. Y si algún test falla, podemos detectar los errores de forma prematura sin que estos lleguen al usuario.

Por eso, en esta lección vamos a ver cómo implementar una suite de tests con Flask, continuando justo por donde lo dejamos en la lección anterior, en la que vimos cómo actualizar el esquema de base de datos con Flask-Migrate. Puedes descargar el código correspondiente a la misma como te indico a continuación:

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 11 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion11 -b leccion11

Índice
Aquí te dejo los puntos principales de esta lección:

Conceptos básicos de los tests con Flask
Configuración básica para los tests con Flask
Primer test con Flask
Implementando un test unitario con Flask
Tests y login con Flask
Conceptos básicos de los tests con Flask
Antes de implementar el conjunto de tests, repasemos una serie de conceptos básicos relacionados con los tests en Flask.

Para llevar a cabo los tests podemos usar diferentes frameworks como pytest o unittest, … Nosotros, en el tutorial, utilizaremos unittest, que pertenece a la librería estándar de Python.

❗️¡ATENCIÓN! No es propósito de esta lección explicar el módulo unittest, ni ver un uso avanzado del mismo.

Sin embargo, sí debes tener claro que en unittest, una suite de tests se implementa dentro de una clase que hereda de unittest.TestCase. Dentro de esa clase, cada método que definamos que comience por la palabra test, será considerado como un test independiente. Además, puedes usar los métodos setUp() y tearDown() para ejecutar código antes y después de cada test. En definitiva, un test tiene el siguiente aspecto:

import unittest
class TestSuite(unittest.TestCase):
    def setUp(self):
        # Código que se ejecuta antes de cada test
        ...
    def test_mi_test(self):
        # Código que se quiere probar
        ...
    def tearDown(self):
        # Código que se ejecuta después de cada test
        ...
Por otro lado, Flask nos permite simular las peticiones de un cliente (por ejemplo, un navegador), ofreciéndonos un cliente, app.test_client() (el cliente para pruebas de Werkzeug), y manejando los contextos por nosotros. En caso de que necesitemos ejecutar alguna instrucción que dependa del contexto de aplicación, como acceder a base de datos, y esta se ejecute fuera de la llamada del cliente, tendremos que crear el contexto nosotros mismos del siguiente modo:

with app.app_context():
    # Código que depende del contexto de aplicación
    # como el acceso a base de datos
Configuración básica para los tests con Flask
A la hora de ejecutar los tests, vamos a crear una aplicación del mismo modo que se crea cuando se lanza el servidor de Flask. Esta aplicación tomará los parámetros de configuración definidos en el fichero config/testing.py. Ábrelo y comprueba si su contenido es este:

from .default import *
# Parámetros para activar el modo debug
TESTING = True
DEBUG = True
APP_ENV = APP_ENV_TESTING
WTF_CSRF_ENABLED = False
Si te falta algún parámetro, añádelo de manera que tu fichero quede similar al que te muestro arriba. El significado de cada uno de los parámetros es el siguiente:

TESTING	Deshabilita la captura de errores durante el manejo de peticiones para obtener mejores informes de error en los tests
DEBUG	Activa el modo debug
APP_ENV	Nombre del entorno de ejecución. En este caso ‘testing’
WTF_CSRF_ENABLED	Lo establecemos a False para deshabilitar la protección CSRF durante los tests
Por otro lado, para los tests vamos a utilizar una base de datos diferente a la de desarrollo. Esto lo haremos debido a que cada vez que se ejecuta un test, crearemos y borraremos las tablas de la base de datos (para asegurar la correcta ejecución de los tests). De este modo, usando una base de datos diferente, podremos tener siempre nuestros datos de prueba a salvo.

La cadena de conexión a la base de datos la definiremos en el fichero instance/config-testing.py. Abre este fichero y añade la cadena de conexión (con los datos de tu propia base de datos):

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:testing@localhost:5432/miniblog_test'
❗️¡Recuerda! En el método factoría create_app(), situado en el fichero app/__init__.py, se cargan los parámetros de configuración del fichero instance/config-testing.py si el valor del parámetro TESTING es True (cosa que ocurrirá durante la ejecución de los tests).

Primer test con Flask
Pues ahora sí, ya que lo tenemos todo preparado, vamos a implementar nuestro primer test con Flask. El test será muy sencillo. Simplemente comprobaremos que al acceder a la página principal del blog cuando no hay entradas, se muestra el mensaje No hay entradas.

Lo primero que haremos será crear un paquete llamado tests en la carpeta app/. Dentro del paquete test, crea un fichero llamado test_blog_client.py.

Deberías tener una estructura similar a la siguiente:

+ miniblog
|_+ app
  |_+ tests
    |_ __init__.py
    |_ test_blog_client.py
  |_ ...
|_ ...
Ahora abre el fichero __init__.py del directorio tests y añade lo siguiente:

import unittest
from app import create_app, db
class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(settings_module="config.testing")
        self.client = self.app.test_client()
        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()
    def tearDown(self):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()
Como puedes observar, hemos creado una clase base para nuestros tests llamada BaseTestClass. Esta clase implementa el método setUp(), que se ejecuta justo antes de cada test. En él, se crea e inicializa una instancia de la aplicación (con los parámetros de test), se obtiene una referencia al cliente de Werkzeug y se crean las tablas de la base de datos. La clase BaseTestClass también implementa el método tearDown(). Básicamente, este método borra las tablas de base de datos tras finalizar cada test.

Ahora sí que lo tenemos todo listo para implementar nuestros tests. Abre el fichero test_blog_client.py y añade lo siguiente:

from . import BaseTestClass
class BlogClientTestCase(BaseTestClass):
    def test_index_with_no_posts(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'No hay entradas', res.data)
Lo que hemos hecho ha sido crear un test que comprueba que al acceder a la página principal de nuestro blog, /, nos aparece el mensaje No hay entradas.

❗️Recuerda que en cada test se vuelve a recrear la base de datos. Como no hemos creado ningún post por el momento, la página principal, que devuelve el listado de post, no devolverá ninguno y, en su lugar, mostrará un mensaje indicando este hecho.

¡Vamos a ejecutar nuestro test a ver si pasa!. Abre un terminal, sitúate en el directorio de tu proyecto, activa tu entorno virtual Python y ejecuta lo siguiente:

$> python -m unittest
¡Vaya! Nuestro test parece que ha fallado. Probablemente te encuentres con un error similar al siguiente:

Fallo al ejecutar los tests en Flask con unittest
No te preocupes, de hecho está bien que falle. Lo que ocurre es que cuando no hay posts que mostrar, nuestra página principal no indica nada al usuario. Vamos a mejorarla añadiendo el mensaje que esperamos encontrar en este test.

Abre el fichero app/public/templates/public/index.html y añade el {% else %} al bucle for. El else se ejecutará en caso de que la variable posts sea None o esté vacía:

{% for post in posts %}
    <li><a href="{{ url_for('public.show_post', slug=post.title_slug) }}">{{ post.title }}</a></li>
{% else %}
    <li>No hay entradas</li>
{% endfor %}
Vuelve a ejecutar el test:

$> python -m unittest
¡Esta vez sí, el test ha pasado satisfactoriamente! 💃🏻🎉

Implementando un test unitario con Flask
En esta sección vamos a implementar un test unitario con Flask. Digo unitario porque vamos a probar el método save() de la clase Post, aunque también es de integración porque durante la ejecución del mismo llegamos a guardar un objeto en la base de datos. El caso es que no importa si es unitario o de integración. Lo importante es que nuestro código quede probado.

El único problemilla es que para guardar un post necesitamos que exista previamente un usuario en la base de datos, ya que todo post hace referencia a un usuario. No te preocupes que lo vamos a solventar fácilmente.

Abre el fichero app/tests/__init__.py y al final del mismo añade lo siguiente:

@staticmethod
def create_user(name, email, password, is_admin):
    user = User(name, email)
    user.set_password(password)
    user.is_admin = is_admin
    user.save()
    return user
Recuerda importar la clase User al comienzo. Ahora vamos a crear un usuario administrador y un usuario invitado para que estén disponibles para todos los tests. En el mismo fichero, dentro del método setUp(), añade estas líneas al final, justo después de crear las tablas:

def setUp(self):
    ...
    # Crea un contexto de aplicación
    with self.app.app_context():
        # Crea las tablas de la base de datos
        db.create_all()
        # Creamos un usuario administrador
        BaseTestClass.create_user('admin', 'admin@xyz.com', '1111', True)
        # Creamos un usuario invitado
        BaseTestClass.create_user('guest', 'guest@xyz.com', '1111', False)
Con esto ya tendríamos disponibles ambos usuarios para utilizar en nuestros tests.

¿Por qué vamos a crear un test para el método save() de la clase Post? Porque en él se genera dinámicamente el campo title_slug de las entradas del blog. En caso de guardar dos entradas con el mismo título, lo que ocurre es que el slug de la segunda añade un sufijo numérico incremental. El resultado sería como el siguiente:

slug
slug-1
slug-2
...
¡Pues esta funcionalidad hay que probarla!

Añade un nuevo fichero llamado test_post_model.py al directorio app/tests/. Dentro de ese fichero añade el siguiente código:

import unittest
from app.auth.models import User
from app.models import Post
from . import BaseTestClass
class PostModelTestCase(BaseTestClass):
    """Suite de tests del modelo Post"""
    
    def test_title_slug(self):
        with self.app.app_context():
            admin = User.get_by_email('admin@xyz.com')
            post = Post(user_id=admin.id, title='Post de prueba', content='Lorem Ipsum')
            post.save()
            self.assertEqual('post-de-prueba', post.title_slug)
El test test_title_slug() comprueba que el campo title_slug se genera correctamente. Si ejecutas los tests, verás que pasa correctamente.

A continuación añade el test test_title_slug_duplicated(). En este test comprobamos que al guardar dos posts con el mismo título, el segundo añade el sufijo -1 al campo title_slug:

def test_title_slug_duplicated(self):
    with self.app.app_context():
        admin = User.get_by_email('admin@xyz.com')
        post = Post(user_id=admin.id, title='Prueba', content='Lorem Ipsum')
        post.save()
        post_2 = Post(user_id=admin.id, title='Prueba', content='Lorem Ipsum Lorem Ipsum')
        post_2.save()
        self.assertEqual('prueba-1', post_2.title_slug)
        post_3 = Post(user_id=admin.id, title='Prueba', content='Lorem Ipsum Lorem Ipsum')
        post_3.save()
        self.assertEqual('prueba-2', post_3.title_slug)
        posts = Post.get_all()
        self.assertEqual(3, len(posts))
Ejecuta de nuevo los test a ver qué ocurre…

Error descubierto gracias a los tests en Flask
¡Pues sí! El test falla, aunque el código del test es correcto, hace lo que indican los requisitos. Esto implica que hay un fallo en el código. ¡Hemos descubierto un bug en el código!

Efectivamente, el método save() de la clase Post esconde un bug. No se hace rollback de la base de datos cuando se captura la excepción IntegrityError y hay que hacerlo.

Abre el fichero app/models y añade el rollback en el método save() de la clase Post (añade de nuevo también el objeto a la sesión de base de datos):

def save(self):
    ...
    while not saved:
        try:
            db.session.commit()
            saved = True
        except IntegrityError:
            db.session.rollback()  # Añade esta línea
            db.session.add(self)   # y esta
            count += 1
            self.title_slug = f'{slugify(self.title)}-{count}'
Si vuelves a ejecutar los tests, esta vez sí que pasarán todos. ¡Hemos corregido un bug gracias a los tests!

Tests y login con Flask
Vamos a acabar este tutorial añadiendo unos cuántos tests más.

Test para comprobar el listado de entradas de la página principal
Abre de nuevo el fichero test_blog_client.py y añade el siguiente test:

def test_index_with_posts(self):
    with self.app.app_context():
        admin = User.get_by_email('admin@xyz.com')
        post = Post(user_id=admin.id, title='Post de prueba', content='Lorem Ipsum')
        post.save()
    res = self.client.get('/')
    self.assertEqual(200, res.status_code)
    self.assertNotIn(b'No hay entradas', res.data)
Como puedes apreciar, al comienzo del test se guarda en base de datos una nueva entrada. Esto hará que al acceder a la página principal ya no se muestre el mensaje No hay entradas.

Test para comprobar la redirección a la página de login
Otra cosa que podemos probar es si realmente un usuario que no está autenticado, es redirigido a la página de login cuando intenta acceder a una página con acceso restringido por el decorador @login_required. Añade el siguiente test a continuación del que añadimos en la sección de arriba:

def test_redirect_to_login(self):
    res = self.client.get('/admin/')
    self.assertEqual(302, res.status_code)
    self.assertIn('login', res.location)
Test para comprobar acceso no autorizado a usuarios invitados
Otro test que puede ser interesante es verificar que cuando un usuario invitado intenta acceder al panel de administración del blog, por ejemplo a la página /admin, la aplicación le devuelve un error 401 de acceso no autorizado.

Como puedes intuir, para implementar este test necesitamos un usuario que esté autenticado en la aplicación. Vamos a añadir un método login a la clase base, de manera que esté disponible para el resto de tests. Este método simulará un login de un usuario. Abre el fichero app/tests/__init__.py y añade el método login() al final de la clase:

def login(self, email, password):
    return self.client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)
Volviendo a nuestro test de acceso no autorizado, ahora ya podemos implementarlo haciendo uso del método login() anterior. Añade el siguiente test al final del fichero test_blog_client.py:

def test_unauthorized_access_to_admin(self):
    self.login('guest@xyz.com', '1111')
    res = self.client.get('/admin/')
    self.assertEqual(401, res.status_code)
    self.assertIn(b'Ooops!! No tienes permisos de acceso', res.data)
Test para comprobar acceso autorizado a un usuario administrador
El último test de ejemplo que voy a mostrarte es el caso justamente contrario al anterior. Vamos a asegurarnos de que un usuario de tipo administrador está autorizado para acceder a las páginas de administración del blog. Por ejemplo a la página /admin:

def test_authorized_access_to_admin(self):
    self.login('admin@xyz.com', '1111')
    res = self.client.get('/admin/')
    self.assertEqual(200, res.status_code)
    self.assertIn(b'Posts', res.data)
    self.assertIn(b'Usuarios', res.data)
❗️¡ATENCIÓN! Prueba ahora a lanzar todos los tests ejecutando desde el terminal el comando python -m unittest. En principio, todos los test deben pasar, lo que implica que nuestro código hace lo que debe. Cuando hagas cualquier cambio, asegúrate de volver a ejecutar los tests para comprobar que no has introducido errores.

Conclusión
¿Qué te ha parecido el tutorial? A mí, si te digo la verdad, me han entrado unas ganas tremendas de seguir haciendo tests, jaja.

Bueno, creo que con lo que hemos visto aquí tienes material suficiente para iniciarte en el mundo de los tests con Flask. ¿Te atreves a seguir añadiendo test al proyecto?

Personalmente, cuando desarrollo, suelo implementar primero los tests, ya que permiten definir concretamente los requisitos de la aplicación. Sobre testing y pruebas hay mucha literatura. No hay que probar todo, pero sí al menos las partes críticas de la aplicación. La experiencia te hará saber qué es importante y qué no. Eso sí, prueba y haz tests.

Como siempre, si tienes alguna duda, puedes ponerte en contacto conmigo dejándome un mensaje al final del post, a través de mis redes sociales o enviándome un email. Estaré encantado de poder ayudarte.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 12 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion12 -b leccion12

¡Por cierto! No te pierdas el próximo tutorial. En él descubrirás cómo procesar consultas de base de datos que devuelven grandes listados de manera más eficiente. ¡Te espero!
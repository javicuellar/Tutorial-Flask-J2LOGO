Lección 7: Parámetros de configuración de un proyecto
Categoría: Flask
flask, medio, python, tutorial flask
Lección 7 Parámetros de configuración de un proyecto
Hola amig@ Pythonista, ¿qué tal? Esta lección del tutorial me parece interesantísima y una de las principales que debes dominar si quieres desarrollar aplicaciones web o APIs como un verdadero profesional. En esta entrada del blog voy a hablarte de los parámetros de configuración de un proyecto. He creído conveniente dedicarles una lección completa ya que son una parte fundamental de toda aplicación Flask. Por eso, te animo a que no pierdas detalle a esta parte del tutorial.

💥 Fundamentalmente, en esta lección aprenderás por qué es importante parametrizar ciertos valores en lugar de usarlos directamente en el código. Además, te daré unos consejos para que separes la configuración de tu aplicación en función del entorno de ejecución. Quédate con esto último, porque no es algo que te enseñen en otros sitios con el nivel de detalle con el que lo verás aquí.

No me enrollo más 🙃 Como siempre, retomaremos el tutorial donde lo dejamos en la lección anterior. Así que, si todavía no tienes el código, lo puedes descargar como te indico a continuación.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 6 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion6 -b leccion6

Índice
Aquí te dejo los puntos principales de esta lección:

Introducción
Parámetros de configuración según el entorno de ejecución
Principales parámetros de configuración de Flask
El objeto config en Flask
Técnicas para separar los parámetros de configuración en función del entorno
El directorio Instance
Consejos prácticos
Un ejemplo práctico
Introducción
Toda aplicación web o API REST depende de una serie de valores que se pueden parametrizar. Por supuesto, esto también ocurre cuando desarrollamos un proyecto con Flask.

¿No sabes qué son los parámetros de configuración? Básicamente, los parámetros de configuración de un proyecto nos permiten definir la cadena de conexión a la base de datos, la duración de la cookie de sesión o el idioma por defecto de la aplicación, entre otros. Normalmente, en lugar de escribirlos directamente en el código, se definen en unos ficheros independientes. Otra particularidad es que son accesibles en cualquier parte del código (como si fueran variables globales).

Si revisas el método create_app que se encontraba en el fichero app/__init__.py de la Lección 6, después de crear el objeto app se definían tres parámetros: SECRET_KEY, SQLALCHEMY_DATABASE_URI y SQLALCHEMY_TRACK_MODIFICATIONS. Todos ellos son parámetros de configuración. No sé si lo recordarás pero en su momento te dije que los iba a definir en ese lugar aunque lo cambiaría en un futuro. Pues bien, el momento ha llegado y vamos a ver una forma mejor de crear dichos parámetros.

Parámetros de configuración según el entorno de ejecución
Entonces, ¿cómo y dónde se definen los parámetros de configuración? Lo normal, y lo que verás en la mayoría de tutoriales, es definir los parámetros de configuración en un fichero independiente de tu código. Esto está bien, ya que es una manera de conseguir independencia y de no escribir los parámetros directamente en el código (como hemos hecho hasta ahora). Sin embargo, no es del todo adecuado ya que dificulta el despliegue de la aplicación en distintos entornos de ejecución.

Pero yo lo que quiero es que seas un auténtic@ Pythonista, por eso te enseñaré cómo definir los parámetros de configuración para tu entorno local de desarrollo, tu entorno de pruebas y tu entorno de producción.

Para que te sea más fácil entender lo que te quiero explicar, vamos a fijarnos por el momento en el parámetro SQLALCHEMY_DATABASE_URI. Este parámetro almacena la cadena de conexión a la base de datos. Hasta ahora, habíamos definido este parámetro en las primeras líneas del método create_app:

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testing@localhost:5432/miniblog'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    login_manager.init_app(app)
    login_manager.login_view = "login"
    ...
¿Qué problema hay al hacerlo así? Pues actualmente la cadena de conexión tiene una serie de parámetros como el nombre de usuario de Postgres, la contraseña o la IP en la que se encuentra la base de datos. Se supone que todos estos parámetros son los de nuestro entorno de desarrollo local. ¿Qué ocurre si queremos desplegar el miniblog o cualquier otra aplicación en un entorno de producción y estos valores de la cadena de conexión no son los mismos?

💥BOOOOMMMMM!!!

Efectivamente, tienes un problema. La primera solución sería modificar el fichero que contiene la cadena de conexión cada vez que vayamos a pasar la aplicación a producción, pero ya te adelanto que se te olvidará alguna vez o te equivocarás al introducir un parámetro. Además, esta solución no es viable en un entorno de integración y despliegue continuos.

Entonces, ¿qué hacemos? Mi recomendación y lo que yo siempre hago es definir los parámetros de configuración en ficheros, uno por entorno, de manera que son independientes entre sí y no tengo que modificar mi código cada vez que despliego la aplicación en un entorno concreto. Más adelante, en los ejemplos, te enseñaré cómo hacerlo.

Principales parámetros de configuración de Flask
Eres libre de crear los parámetros de configuración que consideres necesarios. Otras veces, las extensiones definen sus propios parámetros que deberás establecer para que funcionen correctamente.

Por su parte, cualquier aplicación Flask también depende de una serie de parámetros que debes conocer:

ENV: Indica el entorno en el que se está ejecutando una aplicación. En principio, los únicos valores posibles son development y production. Muchas extensiones pueden cambiar su comportamiento en función de este parámetro. Flask, por ejemplo, habilita el modo DEBUG si su valor es development. ❗️No uses el valor development cuando ejecutes tu aplicación en un entorno de producción.
DEBUG: Indica si el modo debug está activo. Cuando se inicia el servidor de desarrollo que viene con Flask, cualquier excepción no controlada será mostrada de una forma más o menos amigable. Además, el servidor se reinicia si detecta cualquier cambio en el código. Por defecto, el modo debug se activa si el parámetro ENV es development. ❗️No actives el modo debug cuando ejecutes tu aplicación en un entorno de producción.
ATENCIÓN: Por el modo en que está diseñado Flask, normalmente este requiere que la configuración esté disponible cuando la aplicación arranca. Los parámetros ENV y DEBUG mencionados anteriormente son un tanto especiales, ya que si se modifica su valor después de que se inicie la aplicación, esta puede comportarse de manera inconsistente. Además, para asegurar que su valor se lee lo antes posible, la recomendación por parte de Flask es establecer sus valores a través de las variables de entorno FLASK_ENV y FLASK_DEBUG, respectivamente. Por tanto, siempre que sea posible, crearemos estas variables de entorno en lugar de usar los parámetros de configuración mencionados anteriormente.
Otros parámetros de configuración que define Flask son los siguientes:

TESTING: Habilita el modo de test. Esto hace que las excepciones no sean controladas por los manejadores de error de la aplicación y lleguen, por tanto, al código de los tests. Además, las extensiones pueden cambiar su comportamiento para facilitar las pruebas. Establece su valor a True cuando estés ejecutando tus tests.
SECRET_KEY: Es necesaria para firmar la cookie de sesión, aunque también puede ser utilizada para otros aspectos de seguridad, tanto por la propia aplicación como alguna extensión. En esta entrada del blog puedes puedes consultar cómo generar claves seguras.
El objeto config en Flask
Ya hemos visto anteriormente cómo establecer los parámetros de configuración tras crear el objeto Flask en el método create_app. También te he indicado, que una forma mejor de definir los parámetros de configuración es hacerlo en un fichero independiente. La pregunta es, ¿cómo puedo leer, añadir o modificar estos parámetros?

Si te fijas en este código que ya hemos visto, obtendrás la respuesta:

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    ...
El atributo config del objeto Flask es el lugar en el que el framework y las extensiones establecen algunos valores de configuración. Pero además, es el lugar en el que tú puedes definir tus propios parámetros de configuración.

❗️El objeto config es realmente una subclase de la clase dictionary. Por tanto, puede manipularse como un diccionario cualquiera.
Sabiendo esto, para leer el valor de un parámetro de configuración o guardar uno nuevo, simplemente accede al atributo config del objeto app en cualquier lugar de tu código.

Técnicas para separar los parámetros de configuración en función del entorno
Ya hemos visto cómo definir los parámetros de configuración en el propio código (en el método create_app). Sin embargo, como te he mencionado, esto presenta varios problemas si desplegamos la aplicación en diferentes entornos.

La práctica más habitual, y la que yo te recomiendo, es definir los parámetros en ficheros independientes, uno por entorno. A continuación veremos cómo hacerlo.

Pero antes de nada, vamos a repasar los diferentes entornos que deberías tener (aunque esto dependerá del tipo de proyecto y de los recursos de los que puedas disponer):

Local: Es tu propio entorno, tu ordenador, donde desarrollas el código. Cada uno de los programadores tiene su entorno local.
Desarrollo: Es un entorno compartido en el que todos los programadores tienen acceso. Se suele usar para probar los cambios que se están haciendo durante el desarrollo de la aplicación.
Staging: Es el entorno de preproducción. Un entorno de pruebas lo más parecido posible a producción. Generalmente es un entorno estable, sin fallos, que se suele usar para que los clientes puedan probar la aplicación de forma independiente al entorno de desarrollo.
Test: Es el entorno en el que se ejecutan los diferentes test.
Producción: Este es el entorno real donde se despliega la aplicación para su uso por parte de los clientes y usuarios.
Una vez que tenemos claro cuáles son los diferentes entornos, vamos a ver cómo podemos definir los parámetros para cada entorno.

Usando herencia
Una técnica propuesta en la documentación de Flask es usar herencia, de manera que definimos en un fichero una clase padre con los parámetros por defecto y posteriormente declaramos tantas clases hijas como entornos tengamos. Una aproximación para nuestro miniblog sería:

# Fichero de configuración config.py
class Config(object):
    SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@prod_host:port/db_name'
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@dev_host:port/db_name'
class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@staging_host:port/db_name'
class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@test_host:port/db_name'
El código anterior lo incluiríamos en un fichero llamado config.py, situado al mismo nivel que el directorio app.

Para cargar los valores en el objeto config de Flask en función del entorno, tendríamos que añadir lo siguiente en el método create_app:

def create_app(settings_module='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(settings_module)
El método from_object del objeto config carga los distintos parámetros de configuración que hayamos definido en cada una de las clases de cada entorno. Lo ideal es que el parámetro settings_module sea un valor que leamos de una variable de entorno, que llamaremos, por ejemplo, APP_SETTINGS_MODULE:

# entrypoint.py
# Por ejemplo, APP_SETTINGS_MODULE = config.ProductionConfig
import os
from app import create_app
settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)
❗️El método from_object solo tendrá en cuenta aquellas claves que encuentre en MAYÚSCULAS.
Usando ficheros independientes, uno por entorno
El método anterior está bien, no obstante, yo prefiero el que te voy a explicar a continuación que consiste en tener un fichero con parámetros por cada entorno.

De este modo tendríamos un fichero con los parámetros por defecto:

# config/default.py
SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
SQLALCHEMY_TRACK_MODIFICATIONS = False
Y luego, en cada uno de los ficheros que definen los parámetros de cada entorno, tan solo tenemos que importar todo de este fichero por defecto:

# config/prod.py
from .default import *
SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@prod_host:port/db_name'
# config/dev.py
from .default import *
SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@dev_host:port/db_name'
Al igual que usando herencia, para cargar en el objeto config los parámetros definidos en estos ficheros, usaremos el método from_object:

# app/__init__.py
def create_app(settings_module='config.development'):
    app = Flask(__name__)
    app.config.from_object(settings_module)
Y en la variable APP_SETTINGS_MODULE indicamos el módulo del que cargar los parámetros:

# entrypoint.py
# Por ejemplo, APP_SETTINGS_MODULE = config.prod
import os
from app import create_app
settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)
❗️Recuerda que el método from_object solo tiene en cuenta aquellas claves que encuentre en MAYÚSCULAS.
El directorio Instance
Llegados a este punto, tan solo me queda por darte un consejo más antes de poner en práctica todo lo que te he explicado.

En el apartado anterior te he indicado que cada uno de los desarrolladores tiene su propio entorno local que utiliza para desarrollar la aplicación. En el ejemplo, hemos definido la variable SQLALCHEMY_DATABASE_URI con los valores de la cadena de conexión. Se supone que todos estos ficheros de configuración forman parte de un sistema de control de versiones, por lo que puede suponer un problema. ¿Qué ocurre si los parámetros de la cadena de conexión a la base de datos que tienes configurada en tu equipo es distinta a la de otro desarrollador? ¿Y si estoy haciendo pruebas con una clave personal que no quiero que nadie más sepa? Por un lado no queremos que el valor de la cadena de conexión cambie cada vez que nos descarguemos el código del repositorio. Por otro lado, tampoco queremos compartir claves personales con el resto del equipo. ¿Cuál es la solución? El directorio instance.

Flask pone a nuestra disposición un directorio especial, llamado instance, que podemos utilizar para crear ficheros con parámetros de configuración que no queremos que formen parte del sistema de control de versiones. De este modo, podemos definir aquí, por ejemplo, la cadena de conexión a la base de datos local. El directorio instance se sitúa al mismo nivel que el directorio /app o /config:

# instance/config.py
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:testing@localhost:5432/miniblog'
Como puedes apreciar, he definido aquí la cadena de conexión que teníamos al inicio del tutorial en el método create_app.

Para cargar los parámetros del fichero instance/config.py en el objeto config de la aplicación, haremos lo siguiente:

# app/__init__.py
def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True)
    # Carga los parámetros de configuración según el entorno
    app.config.from_object(settings_module)
    # Carga la configuración del directorio instance
    app.config.from_pyfile('config.py', silent=True)
    ...
Del código anterior quiero resaltar tres cosas:

La primera es que al crear el objeto Flask, establecemos el parámetro instance_relative_config a True para que tenga en cuenta que el directorio /instance se encuentra al mismo nivel que el directorio /app.
La segunda es que para cargar los parámetros del directorio /instance, llamamos al método from_pyfile. El parámetro silent=True lo usaremos para que la aplicación no falle en caso de que el directorio instance no exista (en principio, solo debe existir en el entorno local).
La última es que si definimos un parámetro en el fichero /instance/config.py y el parámetro ha sido  definido con anterioridad, será sobrescrito con el valor que tenga en este fichero.
Consejos prácticos
Y antes de actualizar el miniblog con todo lo que aquí te he enseñado, te daré una serie de consejos prácticos:

Separa la configuración de tu aplicación con diferentes ficheros, uno por entorno.
Indica el fichero de configuración a utilizar con una variable de entorno.
Usa el directorio instance para definir aquellos parámetros que no deben formar parte del sistema de control de versiones.
Define las variables de entorno FLASK_ENV y FLASK_DEBUG en lugar de usar los parámetros ENV y DEBUG, respectivamente.
Recuerda que lo ideal es cargar todos los parámetros de configuración antes de arrancar la aplicación (usando por ejemplo el método create_app).
No escribas código que necesite de parámetros de configuración en tiempo de importación. Si fuera necesario, reescribe el código para que pueda usarlos en un momento posterior.
En mi caso, los valores development y production que puede tener el parámetro ENV son insuficientes. Yo suelo declarar un parámetro APP_ENV con más valores, uno por entorno. Esto me sirve por si necesito conocer desde el código de la aplicación el entorno en el que se está ejecutando.
Un ejemplo práctico
Ahora sí, veamos cómo poner en práctica todo lo aprendido con nuestro miniblog.

Lo primero de todo es modificar el método create_app que se encuentra en el fichero app/__init__.py de la misma forma en que hemos visto anteriormente:

# app/__init__.py
def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True)
    # Load the config file specified by the APP environment variable
    app.config.from_object(settings_module)
    # Load the configuration from the instance folder
    if app.config.get('TESTING', False):
        app.config.from_pyfile('config-testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    ...
El único cambio con respecto a los ejemplos anteriores es que tengo dos ficheros de configuración en el directorio instance. Uno para el entorno local y otro para ejecutar los tests en local (te lo explicaré más en profundidad en la lección correspondiente a los tests).

El siguiente cambio que tenemos que hacer es modificar el fichero entrypoint.py:

# entrypoint.py
import os
from app import create_app
settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)
❗️Recuerda definir la variable de entorno APP_SETTINGS_MODULE con el valor del entorno en el que estés ejecutando la aplicación.
Por último, crearemos los directorios config e instance y añadiremos en ellos un fichero por entorno:

# config/default.py
from os.path import abspath, dirname
# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))
SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False
# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''
# config/dev.py
from .default import *
APP_ENV = APP_ENV_DEVELOPMENT
SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@host:port/db_name'
# config/local.py
from .default import *
APP_ENV = APP_ENV_LOCAL
# config/prod.py
from .default import *
SECRET_KEY = '5e04a4955d8878191923e86fe6a0dfb24edb226c87d6c7787f35ba4698afc86e95cae409aebd47f7'
APP_ENV = APP_ENV_PRODUCTION
SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@host:port/db_name'
# config/staging.py
from .default import *
APP_ENV = APP_ENV_STAGING
SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@host:port/db_name'
# config/testing.py
from .default import *
# Parámetros para activar el modo debug
TESTING = True
DEBUG = True
APP_ENV = APP_ENV_TESTING
SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@host:port/db_name'
# instance/config.py
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:testing@localhost:5432/miniblog'
# instance/config-testing.py
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:testing@localhost:5432/miniblog_test'
Con todos estos cambios, la estructura del miniblog quedaría de la siguiente manera:

+ app
   |_ /admin
   |_ /auth
   |_ ...
   |_ __init__.py
+ config
   |_ __init__.py
   |_ default.py
   |_ dev.py
  |_ local.py
  |_ prod.py
  |_ staging.py
  |_ testing.py
+ instance
  |_ config.py
  |_ config-testing.py
+ env
+ ...
Conclusión
Esta lección ha sido muy densa pero espero que te haya servido de ayuda. En ella hemos visto los siguientes puntos:

La importancia de parametrizar ciertos valores en la aplicación.
El objeto config como el punto desde el que manejar los parámetros.
Los principales parámetros de configuración de Flask.
Cómo definir los parámetros de configuración en ficheros.
Cómo separar los parámetros de configuración en función del entorno.
El directorio instance para definir parámetros de configuración que no queremos que formen parte del sistema de control de versiones.
Como siempre, si tienes alguna duda siempre puedes ponerte en contacto conmigo dejándome un mensaje al final del post, a través de mis redes sociales o enviándome un email. Estaré encantado de poder ayudarte.

🎯 Puedes descargar el código correspondiente a esta lección desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion7 -b leccion7

En el siguiente tutorial veremos cómo gestionar y manejar errores y excepciones.
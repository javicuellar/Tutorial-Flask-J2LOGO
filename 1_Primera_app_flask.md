Lección 1: La primera aplicación Flask
Categoría: Flask
básico, flask, python, tutorial flask
Bueno, vamos a comenzar con la primera lección del tutorial en la que crearemos nuestra primera aplicación Flask.

Preparando el entorno de programación
Antes de entrar en materia, vamos a configurar nuestro entorno de programación. Voy a suponer que tienes Python instalado así como virtualenv. Si no sabes lo que es esto último, te recomiendo que leas la entrada sobre virtualenv. No obstante, para resumir, te diré que virtualenv nos permite aislar nuestra aplicación junto con todas sus dependencias de otras aplicaciones Python que tengamos en nuestro sistema, de manera que las librerías de cada una de las aplicaciones no entren en conflicto.

Realizada esta aclaración, procedamos con el primer paso que será crear el directorio “tutorial-flask”. Una vez dentro, inicializaremos nuestro entorno Python. Para ello, entramos en el terminal, nos situamos dentro del directorio «tutorial-flask» y escribimos lo siguiente:

virtualenv env
Una vez que hemos creado nuestro entorno, debemos indicarle al terminal que queremos hacer uso del mismo y no del entorno Python global del sistema. Por tanto:

Ejecutaremos el siguiente comando si estamos en Linux/Mac:

source env/bin/activate
Si estamos en Windows ejecutaremos:

env\Scripts\activate.bat
Sabremos que el entorno está activo porque el prompt comienza con la palabra «(env)», como muestra la siguiente imagen:


Tal y como te indiqué en la introducción, vamos a desarrollar un miniblog usando el framework Flask, así que el siguiente paso será instalar dicho framework junto con sus dependencias.

Para instalar Flask (versión 1.x) escribiremos en el terminal el siguiente comando:

pip install Flask
De manera que dentro de nuestro entorno «env», se instalarán el framework y las librerías que necesite.

Podemos ver todas las dependencias de nuestra aplicación si ejecutamos el siguiente comando desde el terminal:

pip freeze

Con esto ya tenemos todo listo para crear nuestra primera aplicación Flask.

Creando la primera aplicación Flask
Francamente, la primera vez que utilicé Flask me sorprendí lo fácil que era y las pocas líneas de código necesarias para crear una aplicación «Hello world!».

En nuestro caso, lo siguiente que haremos será crear un nuevo fichero que llamaremos run.py. Después lo editamos y añadimos el siguiente código:

from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'
¿Qué significa cada una de las líneas de código?

Toda aplicación Flask es una instancia WSGI de la clase Flask. Por tanto, importamos dicha clase y creamos una instancia que en este caso he llamado app. Para crear dicha instancia, debemos pasar como primer argumento el nombre del módulo o paquete de la aplicación. Para estar seguros de ello, utilizaremos la palabra reservada __name__. Esto es necesario para que Flask sepa, por ejemplo, donde encontrar las plantillas de nuestra aplicación o los ficheros estáticos.
Una característica de Flask es que tendremos métodos asociados a las distintas URLs que componen nuestra aplicación. Es en estos métodos donde ocurre toda la magia y toda la lógica que queramos implementar. Dentro del patrón MVC, esta parte del código se correspondería con el controlador. Flask se encarga de hacernos transparente el cómo a partir de una petición a una URL se ejecuta finalmente nuestra rutina. Lo único que tendremos que hacer nosotros será añadir un decorador a nuestra función. En nuestro caso, hemos llamado a nuestra función hello_world que será invocada cada vez que se haga una petición a la URL raíz de nuestra aplicación.
El decorador route de la aplicación (app) es el encargado de decirle a Flask qué URL debe ejecutar su correspondiente función.
El nombre que le demos a nuestra función será usado para generar internamente URLs a partir de dicha función (esto lo veremos más adelante).
Finalmente, la función debe devolver la respuesta que será mostrada en el navegador del usuario.
Hay que llevar cuidado con no nombrar al fichero que instancia nuestra aplicación «flask.py» ya que entraría en conflicto con el propio Flask

Probando la aplicación Flask: Lanzando el servidor interno que viene con Flask
Ya tenemos las primeras líneas de código de nuestra aplicación. El siguiente paso es de los más emocionantes e importantes 😄, probar que todo funciona.

Flask viene con un servidor interno que nos facilita mucho la fase de desarrollo. No debemos usar este servidor en un entorno de producción ya que no es este su objetivo.

En nuestro ejemplo y, dado que en estos momentos estamos en el proceso de construcción de nuestra aplicación, sí haremos uso de él.

Para lanzar nuestra aplicación haciendo uso de este servidor, podemos ejecutar el comando flask o bien   python -m.

Sin embargo, antes de ello debemos indicarle al servidor qué aplicación debe lanzar declarando la variable de entorno  FLASK_APP .

Pongamos todo en orden.

Para declarar la variable FLASK_APP debemos modificar el fichero activate de nuestro entorno Python.

En Linux/Mac se encuentra en env/bin/activate. Al final del fichero añadimos lo siguiente:

export FLASK_APP="run.py"
En Windows se encuentra en env\Scripts\activate.bat. Al final del fichero añadimos lo siguiente:

set "FLASK_APP=run.py"
Para que los cambios realizados se tengan en cuenta debemos salir del entorno Python y volver a entrar. Para salir, hay que ejecutar en el terminal deactivate.

A continuación, volvemos a activar el entorno con source env/bin/activate si estamos en Linux/Mac o env\Scripts\activate.bat si estamos en Windows.

Una vez que hemos definido dónde puede el servidor de Flask encontrar nuestra aplicación, lo lanzamos ejecutando:

flask run
O bien:

python -m flask run
Esto lanzará el servidor de pruebas:

* Serving Flask app "run.py"
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
Para comprobar que, efectivamente, nuestra aplicación funciona, podemos entrar al navegador y en la barra de direcciones introducir localhost:5000. Esto nos mostrará el mensaje «Hello world!» de nuestra función hello_world().

Por defecto, el servidor que viene con Flask está a la escucha en el puerto 5000 y solo acepta peticiones de nuestro propio ordenador.

Si queremos cambiar el puerto por cualquier motivo lo podemos hacer de dos formas distintas:

Estableciendo la variable de entorno FLASK_RUN_PORT en un puerto diferente.
Indicando el puerto al lanzar el servidor flask run --port 6000.
Para aceptar peticiones de otros ordenadores de nuestra red lanzaremos el servidor de la siguiente manera:

flask run --host 0.0.0.0
Modo debug
Flask viene con un modo debug que es muy útil usar mientras estamos desarrollando, ya que cada vez que hagamos un cambio en nuestro código reiniciará el servidor y no tendremos que hacerlo manualmente para que los cambios se tengan en cuenta.

Para activar el modo debug simplemente hay que añadir la variable de entorno FLASK_ENV y asignarle el valor development.

En Linux/Mac:

export FLASK_ENV="development"
En Windows:

set "FLASK_ENV=development"
No usar el modo debug en un entorno de producción

Activar el modo debug hace que:

Se active un depurador.
Se tengan en cuenta los cambios después de guardarlos sin tener que reiniciar manualmente el servidor.
Activa el modo debug, de manera que si se produce una excepción o error en la aplicación veremos una traza de los mismos.
En este caso, al ejecutar el servidor veremos que estamos en modo desarrollo:

* Serving Flask app "run.py" (lazy loading)
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 884-057-557
Conclusión
Y hasta aquí llega la primera lección. En ella hemos visto cómo preparar el entorno de desarrollo e instalar las dependencias necesarias. Hemos creado una primera aplicación que muestra el mensaje «Hello world!» y la hemos puesto a funcionar con el servidor que trae el propio Flask. Por último, hemos visto cómo activar el modo debug para usarlo durante la fase de desarrollo.
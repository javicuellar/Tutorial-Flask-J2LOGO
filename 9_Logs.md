Lección 9: Logs en Flask
Categoría: Flask
flask, medio, python, tutorial flask
Lección 9 Logs en Flask
Continuando la lección anterior sobre gestión y manejo de errores y excepciones, en esta lección veremos un tema que a muchos desarrolladores se les escapa: cómo usar los logs en Flask.

👉🏻 Los mensajes de log son una gran utilidad de toda aplicación, ya no solo de Flask o de las aplicaciones web en general, sino de cualquier programa. Los logs son nuestros ojos 👀 para saber qué ocurre de fondo en la aplicación, cómo la están usando los usuarios y nos pueden avisar cuando sucede un error. De esta forma podemos detectar bugs, puntos de mejora, errores en servicios externos, etc. para darles solución lo antes posible.

¿Tu código está lleno de print() para debuguear? Ya te aviso que lo estás haciendo mal. Pero no te preocupes porque en esta lección aprenderás cómo sacarle partido a los mensajes de log para eso y otras muchas cosas. ¿Te animas? ¡Vamos!

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 8 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion8 -b leccion8

Índice
Aquí te dejo los puntos principales de esta lección:

Configuración por defecto de los logs en Flask
Mejorando los logs de Flask
Envío de errores al administrador
Integrando extensiones y otros módulos
Jugando con los logs en Flask
Configuración por defecto de los logs en Flask
Flask, por defecto, usa el módulo logging de la librería estándar de Python para los mensajes de log.

¡ATENCIÓN! No es propósito de esta lección explicar el módulo logging de Python, sino mostrar buenas prácticas de uso del mismo en una aplicación Flask.

Para escribir un mensaje de log podemos usar el logger asociado al objeto app de la aplicación Flask (app.logger). Este logger toma como nombre el de la propia aplicación (app.name En nuestro caso el nombre es 'app'). Además, es el que usa Flask para mostrar sus propios mensajes de log.

Si no se define previamente una configuración para el módulo logging, al usar el objeto app.logger por primera vez se crea una configuración por defecto. Esta configuración consiste en añadir un handler (StreamHandler) al logger que suele escribir los mensajes en sys.stderr (es decir, en la consola, terminal, pantalla, …).

Primer mensaje de log en Flask
logging, handler, logger, sys.stderr, … No te asustes ni te agobies si no entiendes nada. Si quieres conocer qué significan estos términos visita la documentación oficial. Si no te apetece o ya sabes de qué estamos hablando, déjate llevar. Al final de la lección podrás escribir correctamente mensajes de log en tu aplicación siguiendo los pasos que aquí te explico.

Pero antes de nada, para ver y entender de qué estamos hablando, vamos a escribir y mostrar un mensaje de log con la configuración por defecto que nos ofrece Flask.

Abre en tu editor de código el fichero app/public/routes.py. Ahora modifica la vista index() añadiendo la siguiente línea de código current_app.logger.info('Mostrando los posts del blog') como indico a continuación:

from flask import abort, render_template, current_app
...
# Otras importaciones
@public_bp.route("/")
def index():
    current_app.logger.info('Mostrando los posts del blog')
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)
Lo que estamos haciendo con el método info del objeto logger es escribir un mensaje informativo cada vez que se ejecute la vista index().

Para verlo en acción arranca, en primer lugar, el servidor de Flask con el siguiente comando desde un terminal:

flask run
A continuación, accede desde un navegador a la URL http://localhost:5000/.

En el terminal tiene que mostrarse algo parecido a esto:

Log por defecto de Flask
Como ves, en la penúltima línea aparece el mensaje que hemos añadido en la vista.

¡Ha sido fácil! ¿No? Pues no te pierdas las siguientes secciones en las que aprenderás cómo mejorar el sistema de logging.

Mejorando los logs de Flask
En este apartado te explicaré cómo puedes configurar distintos handlers para los diferentes entornos de ejecución (desarrollo, producción, …) y cómo puedes modificar el formato de los mensajes para mostrar información adicional.

Repaso al módulo logging
Pero antes de nada voy a hacerte un pequeño repaso sobre qué es cada cosa para que así lo tengas todo más o menos claro. Digamos que para poder escribir mensajes de log con el módulo logging necesitamos definir en nuestra aplicación, al menos, un objeto logger. Este objeto es el punto de referencia para escribir los mensajes (aunque podemos definir más de un logger por aplicación como veremos un poco más adelante). A la hora de crear un objeto de tipo logger debemos especificar un nombre. Este nombre tiene una nomenclatura jerárquica que se establece en base al carácter '.'. Es decir, podemos tener un logger llamado app y otro que sea un hijo de este llamado app.public.routes. Si no se especifica ninguna configuración para el logger hijo, entonces toma por defecto la configuración del logger padre.

A su vez, a un logger se le pueden asociar manejadores (o handlers), que indican qué hacer con el mensaje y para qué nivel de log se activan. Existen handlers, como hemos visto, para mostrar los mensajes por pantalla, pero también los hay para escribirlos en un fichero o enviarlos por email.

Los mensajes de log se pueden clasificar en distintos niveles según el tipo de información que ofrecen. Los niveles más comunes son:

DEBUG: Para depurar información. Nivel de información muy detallado.
INFO: Para mensajes informativos que indican que la aplicación se está ejecutando correctamente.
WARNING: Para mensajes de advertencia cuando la aplicación, aun funcionando correctamente, detecta una situación inesperada o posible problema futuro.
ERROR: Para mensajes de error.
EXCEPTION: Para mensajes de error que se producen debido a una excepción. Se muestra la traza de la excepción.
Estos niveles tienen un orden de gravedad de menor a mayor (el orden es el que se indica en el párrafo anterior, aunque existen otros niveles). Así, cuando un handler se configura para el nivel debug, mostrará todos los mensajes de debug pero también los mensajes informativos o de error, puesto que tienen un nivel de gravedad mayor. Sin embargo, si un handler se configura con nivel error, este no procesará los mensajes que se escriben en el nivel de debug dado que son menos graves. Veremos esto más detenidamente a continuación.

Modificando la configuración del logger por defecto de Flask
Veamos todo lo anterior de forma práctica.

Abre en un editor el fichero app/__init__.py y al final del mismo añade la siguiente función:

def configure_logging(app):
    # Eliminamos los posibles manejadores, si existen, del logger por defecto
    del app.logger.handlers[:]
    # Añadimos el logger por defecto a la lista de loggers
    loggers = [app.logger, ]
    handlers = []
    # Creamos un manejador para escribir los mensajes por consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(verbose_formatter())
    handlers.append(console_handler)
    # Asociamos cada uno de los handlers a cada uno de los loggers
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)
El propósito de esta función es configurar el módulo logging. Por ello, lo primero que haremos será borrar los handlers del logger por defecto en caso de que se hayan creado previamente. A continuación, guardamos en una lista los loggers que queremos configurar. En nuestro caso, de momento, solo el logger por defecto de Flask. También inicializamos una lista de handlers. Después creamos un handler de tipo StreamHandler para escribir los mensajes por consola. A este handler le indicamos con setLevel() que tenga en cuenta todos los mensajes con un nivel de gravedad de debug en adelante y le asignamos un formateador distinto al de por defecto (lo veremos a continuación). Por último, asociamos el handler al logger de la instancia de Flask. Como puedes advertir, al logger le establecemos el atributo propagate a False. Esto quiere decir que será el último logger en comprobar la existencia de handlers y no buscará entre sus ancestros si los tuviera.

Ahora vamos a crear el formateador para nuestros mensajes que hemos llamado verbose_formatter():

def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )
Este formateador registra la fecha en que se escribe el mensaje, el nivel de gravedad, el nombre del logger que lo escribe, la función/método dónde se escribe, la línea de código y el propio texto del mensaje.

Lo último que tenemos que hacer para que todo funcione es añadir la llamada a configure_logging() dentro de la función create_app(). Lo haremos justo después de cargar los ficheros de configuración:

def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True)
    # Load the config file specified by the APP environment variable
    app.config.from_object(settings_module)
    # Load the configuration from the instance folder
    if app.config.get('TESTING', False):
        app.config.from_pyfile('config-testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)
    configure_logging(app)
    # El resto del código
    ....
¿Lo probamos? Accede de nuevo en el navegador a la URL http://localhost:5000/ y revisa el mensaje que escribimos en la vista index() del módulo app.public.routes. Tienes que tener algo parecido a esto:

Mensaje de log personalizado
Como puedes comprobar, ahora el mensaje sigue el formato que establecimos en la función verbose_formatter().

Definiendo una configuración para cada entorno de ejecución
Pues hasta aquí hemos visto lo fundamental para actualizar la configuración por defecto del módulo logging. Ahora vamos a ver cómo podemos establecer una configuración distinta de los logs en Flask para cada entorno de ejecución. Simplemente vamos a añadir unas cuantas líneas de código a la función configure_logging().

Abre el fichero app/__init__.py y actualiza la función configure_logging() como te indico a continuación:

def configure_logging(app):
    # Elimina los manejadores por defecto de la app
    del app.logger.handlers[:]
    loggers = [app.logger, ]
    handlers = []
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())
    
    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)
Lo que hemos hecho es añadir el handler console_handler al logger por defecto con una pequeña variación. Si estamos ejecutando la aplicación en el entorno de producción, solo se mostrarán los mensajes con un nivel de gravedad de info en adelante (no se mostrarán los mensajes de debug). Por el contrario, si estamos en los entornos local, test o desarrollo, sí que se mostrarán los mensajes de debug.

Envío de errores al administrador
En este apartado vas a aprender cómo utilizar un nuevo tipo de handler para que los mensajes de error te lleguen al correo electrónico.

Es muy sencillo. Lo que nos interesa es que en el entorno de producción cada vez que se escriba un mensaje de tipo error nos llegue un email. De este modo no tenemos que estar consultando con frecuencia los logs en Flask y estaremos al tanto de cualquier incidencia que ocurra en nuestra aplicación.

¡Vamos a ello! De nuevo abre el fichero app/__init__.py y añade las siguientes líneas en la función configure_logging(), justo en el sitio en el que se establece la configuración para el entorno de producción:

def configure_logging(app):
    
    # Otro código previo
    ...
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)
        mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                   app.config['DONT_REPLY_FROM_EMAIL'],
                                   app.config['ADMINS'],
                                   '[Error][{}] La aplicación falló'.format(app.config['APP_ENV']),
                                   (app.config['MAIL_USERNAME'],
                                    app.config['MAIL_PASSWORD']),
                                   ())
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)
    ...
Observa que hemos añadido un nuevo handler de tipo SMTPHandler. Debes inicializar este manejador con los parámetros de tu servidor smtp de correo, una lista de destinatarios y un asunto. Observa que a este manejador se le ha establecido el nivel de gravedad en error. Además, se le ha asignado un formatter diferente al que utilizamos para el handler StreamHandler.

Añade el nuevo formatter al final del fichero app/__init__.py:

def mail_handler_formatter():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d
            Message:
            %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
    )
Lo has adivinado, nos falta inicializar los parámetros de configuración smtp. Los añadiremos al fichero config/default.py:

# Otros parámetros
...
# Configuración del email
MAIL_SERVER = 'tu servidor smtp'
MAIL_PORT = 587
MAIL_USERNAME = 'tu correo'
MAIL_PASSWORD = 'tu contraseña'
DONT_REPLY_FROM_EMAIL = 'dirección from'
ADMINS = ('juanjo@j2logo.com', )
MAIL_USE_TLS = True
MAIL_DEBUG = False
Con estos cambios, cada vez que se escriba un mensaje con nivel error nos llegará un email con todo detalle sobre el error y/o la excepción.

Integrando extensiones y otros módulos
Si has llegado hasta aquí, ya tendrás todo listo para hacer uso del módulo logging en tu aplicación Flask. Pero antes de empezar a jugar, vamos a ver un último detalle. Hay muchas librerías y extensiones que también hacen uso del módulo logging. Revisa en su documentación si es así. ¿Cómo podemos mostrar los mensajes de log que estas escriben? Muy sencillo, añadiendo sus loggers a nuestra configuración.

Imaginemos que queremos mostrar los mensajes de base de datos que escribe la librería sqlalchemy. Para ello, añade su logger base, que se llama sqlalchemy, justo después de añadir el logger por defecto de Flask:

def configure_logging(app):
    # Elimina los manejadores por defecto de la app
    del app.logger.handlers[:]
    loggers = [app.logger, logging.getLogger('sqlalchemy')]
    handlers = []
    # Código restante
    ...
Al acceder de nuevo a la URL http://localhost:5000/ veremos que en la consola aparecen un montón de mensajes relacionados con la base de datos. Algo similar a la siguiente imagen:

Mensajes de slqalchemy
Jugando con los logs en Flask
Bueno, pues ahora sí, ya tienes a tu disposición todo lo necesario para usar los logs en Flask como un auténtico Pythonista 🐍. Vamos a jugar un poco para aclarar los conceptos que hemos visto en las secciones anteriores.

Añadiendo nuevos loggers a la jerarquía
Personalmente no me gusta usar el logger por defecto de Flask en mis aplicaciones. Principalmente porque hay ocasiones en que no sé qué módulo es el que está escribiendo el mensaje. Lo que suelo hacer es crear un logger por cada módulo en el que vaya a usar mensajes de log. Veámoslo con un ejemplo.

Vuelve a abrir el fichero app/public/routes.py y añade lo siguiente:

import logging
# Otros imports
...
logger = logging.getLogger(__name__)
@public_bp.route("/")
def index():
    current_app.logger.info('Mostrando los posts del blog')
    logger.info('Mostrando los posts del blog')
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)
Lo que he hecho ha sido importar el módulo logging en la primera línea. Después he creado un nuevo logger con logging.getLogger(), justo después del resto de imports. Por último, he añadido a la vista index() un nuevo mensaje de log de tipo info pero esta vez usando el logger que acabo de crear. Si accedemos a la URL http://localhost:5000/, ahora veremos dos mensajes de log diferentes:

Logger personalizado
El primero de ellos nos muestra el mismo mensaje que hemos visto en los ejemplos anteriores. En él podemos apreciar que el nombre del logger es app. El segundo mensaje que observamos es el que se corresponde al nuevo logger que hemos creado. Es prácticamente similar al anterior solo que esta vez el nombre del logger es app.public.routes.

Como te decía, personalmente me gusta más esta última forma de usar el módulo logging porque identifico mucho mejor de dónde procede cada mensaje. Esto es especialmente útil si tenemos varios módulos con el mismo nombre, como es nuestro caso, que tenemos varios módulos llamados routes.

Usando logs en flask con distinto nivel
Ahora vamos a ver el funcionamiento de los logs utilizando mensajes con distinto nivel.

En esta ocasión vamos a modificar la vista show_post() del módulo app.public.routes del siguiente modo:

@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    logger.info('Mostrando un post')
    logger.debug(f'Slug: {slug}')
    post = Post.get_by_slug(slug)
    if post is None:
        logger.info(f'El post {slug} no existe')
        abort(404)
    return render_template("public/post_view.html", post=post)
El ejemplo es un poco absurdo pero nos servirá para comprobar cómo funcionan los niveles de gravedad. Si accedemos ahora a uno de los post de nuestro blog que se listan en la página principal, deberíamos ver en la consola algo parecido a esto:

Ejemplo de log
Si ahora modificamos a info el nivel de gravedad que hemos asignado al handler para el entorno local, veremos que el mensaje DEBUG ya no aparece.

def configure_logging(app):
    # Código previo
    ...
    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)
    # Código restante
    ...
Ejemplo de logs en Flask sin debug
Conclusión
Pues ya hemos llegado al final del tutorial. Espero que te haya servido de ayuda. No te entretengo más. Ahora te toca poner en práctica todos los conceptos que has aprendido en el mismo. Pero antes, hagamos un resumen para recopilar todos los puntos claves de esta lección.

Si quieres mostrar mensajes por consola, no uses print(). Haz uso del módulo logging en su lugar.
El módulo logging es de gran utilidad para saber cómo utilizan los usuarios la aplicación, detectar bugs y conocer puntos de mejora.
Usa correctamente los diferentes niveles de log para clasificar los mensajes que escribes en la aplicación.
Si creas un logger por módulo será mucho más fácil identificar de dónde proviene un mensaje.
A veces resulta útil que los mensajes de error lleguen por correo al administrador para solucionar los problemas lo antes posible.
Como siempre, si tienes alguna duda siempre puedes ponerte en contacto conmigo dejándome un mensaje al final del post, a través de mis redes sociales o enviándome un email. Estaré encantado de poder ayudarte.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 9 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion9 -b leccion9

En el siguiente tutorial veremos cómo proteger las vistas de nuestro blog para que solo puedan crear posts los usuarios con rol de administrador. ¡Te espero!
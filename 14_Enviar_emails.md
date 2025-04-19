Lección 14: Enviar emails con Flask
Categoría: Flask
flask, medio, python, tutorial flask
Lección 14 Enviar emails con Flask
Que pocas lecciones nos quedan ya para terminar el tutorial de Flask. Mientras escribo estas líneas me está dando un poco de pena, pero a la vez estoy contento por todo el trabajo realizado con el tutorial y vuestros comentarios de felicitación. En fin, el blog no para y seguiré escribiendo sobre Flask y Python. Pero como te comenté en la lección anterior, en estas últimas lecciones estoy compartiendo contigo una serie de trucos y tips interesantes. Precisamente, en esta lección vamos a descubrir cómo enviar emails con Flask.

Aunque en un principio pueda parecer que el envío de correos electrónicos es una cosa complicada, nada más lejos de la realidad. Es sencillísimo. Ya lo verás.

Si andas un poco despistad@, comentarte que esta lección continúa por donde lo dejamos en la anterior, en la que vimos cómo paginar consultas de base de datos. Puedes descargar el código correspondiente a la misma como te indico a continuación:

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 13 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion13 -b leccion13

Índice
Aquí te dejo los puntos principales de esta lección:

Cómo enviar emails en Flask con Flask-Mail
Configurar Flask-Mail para enviar emails en Flask
Cómo crear un mensaje
Enviar emails de forma asíncrona
Probando el envío de emails desde el miniblog
Cómo enviar emails en Flask con Flask-Mail
Esta lección es muy corta. Ya verás como en unos pocos pasos estás enviando emails en Flask de manera muy sencilla.

Lo mejor para enviar emails con Flask es utilizar la extensión Flask-Mail. Sí, otra vez hacemos uso de una extensión para facilitarnos la vida.

La comunidad de Flask es muy activa y puedes encontrar extensiones para casi todo.

Para instalar Flask-Mail accede a un terminal, activa tu entorno virtual Python del proyecto y ejecuta lo siguiente:

$> pip install flask-mail
Configurar Flask-Mail para enviar emails en Flask
Una vez que hemos instalado Flask-Mail, debemos crear un objeto de tipo Mail al que tengamos acceso desde el resto del código. Esta clase es la responsable de enviar los mensajes, utilizando para ello los parámetros de configuración de nuestro servidor smtp de correo.

Como con otras extensiones, el objeto Mail lo crearemos e inicializaremos en el fichero app/__init__.py. A continuación, te muestro un extracto de este fichero, enseñándote solo las partes relacionadas con Flask-Mail:

from flask_mail import Mail  # 1. Importamos la clase Mail
# Resto de imports
...
...
migrate = Migrate()
mail = Mail()  # 2. Instanciamos un objeto de tipo Mail
def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True)
    
    # Inicialización de la app
    ...
    ...
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)  # 3. Inicializamos el objeto mail
    ...
Como te decía, para que el objeto Mail pueda enviar mensajes necesita conectarse a un servidor smtp de nuestra propiedad. Para ello, definiremos los siguientes parámetros de configuración en el fichero config/default.py:

MAIL_SERVER	Nombre de tu host smtp (Por ej: mail.smtp.com)
MAIL_PORT	Puerto de tu host smtp
MAIL_USERNAME	Nombre de usuario del servidor smtp
MAIL_PASSWORD	Contraseña del usuario del servidor smtp
MAIL_USE_TLS	Flag que indica si enviar los emails usando el protocolo TLS
🤔 Casualmente son los mismos parámetros que usamos para enviar emails al administrador cuando se registraba un mensaje de error en la aplicación… ¿Casualidad? Jajaja, no. Sabiendo que íbamos a usar esta extensión, aproveché para pasar los mismos parámetros en aquella ocasión al objeto SMTPHandler.

Por si no leíste esa lección, añade los parámetros al fichero config/default.py con los datos de tu servidor smtp:

# Configuración del email
MAIL_SERVER = 'tu servidor smtp'
MAIL_PORT = 587
MAIL_USERNAME = 'tu correo'
MAIL_PASSWORD = 'tu contraseña'
DONT_REPLY_FROM_EMAIL = '(Juanjo, juanjo@j2logo.com)'
ADMINS = ('juanjo@j2logo.com', )
MAIL_USE_TLS = True
❗️¡ATENCIÓN! La única pega que le encuentro a la extensión Flask-Mail es que, en principio, solo se puede configurar una cuenta smtp. No obstante, esto es más que suficiente para la mayoría de aplicaciones. Sin embargo, utilizando una misma cuenta, sí que se pueden enviar emails desde diferentes direcciones de correo.

Cómo crear un mensaje
Una vez que hemos configurado todo, ya podemos enviar emails de forma muy sencilla.

Los pasos a seguir son crear un objeto Message y llamar al método send() del objeto mail, pasando el mensaje como parámetro.

Para crear un mensaje, necesitamos indicar el asunto, la dirección de correo del emisor y las direcciones de correo a las que enviar el mensaje (como una lista):

from flask_mail import Message
msg = Message("Hola",
              sender="from@example.com",
              recipients=["to@example.com"])
También podemos especificar el nombre del emisor, pasando el nombre y la dirección de correo en una tupla. Así lo indiqué en el parámetro DONT_REPLY_FROM_EMAIL de la sección anterior:

msg = Message("Hola",
              sender=("Juanjo", "juanjo@j2logo.com"))
El contenido del mensaje lo indicamos en el atributo body, aunque también podemos crear un mensaje formateado empleando el lenguaje HTML:

msg.body = 'Bienvenid@ a j2logo'
msg.html = '<p>Bienvenid@ a <strong>j2logo</strong></p>'
Como te decía, para enviar el mensaje simplemente hay que llamar al método send() del objeto mail:

from flask_mail import Message
from app import mail
msg = Message("Hola",
              sender="from@example.com",
              recipients=["to@example.com"])
msg.body = 'Bienvenid@ a j2logo'
msg.html = '<p>Bienvenid@ a <strong>j2logo</strong></p>'
mail.send(msg)
Pues ya sabes todo lo que necesitas para enviar emails en Flask de manera sencilla. De todas formas, no te pierdas la siguiente sección en la que te voy a enseñar un último truco.

Enviar emails de forma asíncrona
El problema de enviar mensajes del modo que te he mostrado previamente, es que el envío se realiza de forma síncrona, en el mismo hilo en el que se procesa la petición web. Yo te voy a enseñar un pequeño truco para que se ejecute en un hilo diferente, de manera que el envío del email no bloquee el flujo de la petición.

Crea un nuevo paquete (directorio con un fichero __init__.py) llamado common dentro de la carpeta app. En él, crea un fichero llamado mail.py:

+ app
  |_ ...
  |_+ common
      |_ __init__.py
      |_ mail.py
Ahora pega el siguiente código en el fichero mail.py:

import logging
from smtplib import SMTPException
from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail
logger = logging.getLogger(__name__)
def _send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except SMTPException:
            logger.exception("Ocurrió un error al enviar el email")
def send_email(subject, sender, recipients, text_body,
               cc=None, bcc=None, html_body=None):
    msg = Message(subject, sender=sender, recipients=recipients, cc=cc, bcc=bcc)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    Thread(target=_send_async_email, args=(current_app._get_current_object(), msg)).start()
Como ves, en el fichero hay dos funciones: send_email() y una función privada llamada _send_async_email().

Como usuario, desde tu código cliente solo tienes que llamar a la primera. Esta se encarga de crear un mensaje a partir de los parámetros que recibe la función y de llamar a la función _send_async_email() para que se ejecute en un nuevo hilo. Realmente, el envío del mensaje se realiza en esta última.

Probando el envío de emails desde el miniblog
Pues para finalizar esta lección tan solo nos falta probar todo lo anterior. Para ello, vamos a enviar un email de bienvenida a un usuario cuando se registra.

Abre el fichero app/auth/routes.py y actualiza la vista show_signup_form() como te indico a continuación:

from flask import (render_template, redirect, url_for,
                   request, current_app)
...
from app.common.mail import send_email
# Resto de imports
...
@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    ...
    if form.validate_on_submit():
        ...
        else:
            # Creamos el usuario y lo guardamos
            ...
            # Enviamos un email de bienvenida
            send_email(subject='Bienvenid@ al miniblog',
                       sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                       recipients=[email, ],
                       text_body=f'Hola {name}, bienvenid@ al miniblog de Flask',
                       html_body=f'<p>Hola <strong>{name}</strong>, bienvenid@ al miniblog de Flask</p>')
            # Dejamos al usuario logueado
            ...
Ahora, cuando se registre un nuevo usuario, recibirá un email similar al siguiente:

Enviar emails en Flask bandeja entrada
Enviar emails en Flask contenido del mensaje
Conclusión
Como habrás podido comprobar, enviar emails en Flask es muy sencillo usando la extensión Flask-Mail. Te dejo ahora para que sigas probando las distintas opciones de la extensión y mejorando el mensaje de bienvenida.

Como siempre, si tienes alguna duda puedes ponerte en contacto conmigo dejándome un mensaje al final del post, a través de mis redes sociales o enviándome un email. Estaré encantado de poder ayudarte.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 14 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion14 -b leccion14

En el siguiente tutorial veremos cómo trabajar con fechas en Flask. Para ello, mostraremos en el blog la fecha de creación de los posts y la fecha en que se envían los comentarios. ¡Te espero!
Lección 16: Procesar ficheros en Flask
Categoría: Flask
flask, medio, python, tutorial flask
Lección 16 Procesar ficheros en Flask
En esta lección del tutorial vamos a ver los conceptos básicos sobre cómo procesar ficheros en Flask. Te voy a indicar los elementos clave para que puedas subir y guardar en tu aplicación imágenes, documentos y todo tipo de archivos para, después, mostrárselos a los usuarios.

Va a ser una lección muy, muy práctica, tras la cuál, daremos por finalizado el miniblog 😢 a falta de la lección final, en la que veremos como desplegar el proyecto en un entorno de producción real.

Como siempre, puedes descargar el código actual del proyecto, correspondiente a la lección anterior (en la que trabajamos con fechas en Flask), como te indico a continuación:

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 15 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion15 -b leccion15

Índice
Aquí te dejo los puntos principales de esta lección:

Actualizar el modelo Post para guardar una imagen de cabecera
Procesar ficheros en Flask de forma nativa
Procesar ficheros en Flask con Flask-WTF
Mostrar las imágenes en el blog
Actualizar el modelo Post para guardar una imagen de cabecera
El objetivo de esta lección es el siguiente: Mostrar una imagen de cabecera en la página de detalle de un post. Para ello, necesitamos guardar imágenes y asociar cada una al post correspondiente.

Salvo determinadas excepciones, no soy partidario de guardar ficheros en la base de datos. Prefiero guardar los archivos en el sistema de ficheros. Eso sí, en la base de datos almaceno el nombre que referencia al archivo en el sistema de ficheros.

Con esta premisa, vamos a modificar el modelo Post para añadir un campo que nos permita guardar el nombre de la imagen de cabecera. Abre el fichero app/models.py y añade el campo image_name justo después del campo created, como te muestro a continuación:

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ...
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image_name = db.Column(db.String)
    comments = ...
Dado que hemos modificado un modelo, tenemos que actualizar la base de datos para que tenga en cuenta este cambio.

Accede a un terminal, activa tu entorno virtual Python del proyecto y ejecuta el siguiente comando:

$> flask db migrate -m "añade imagen al modelo post"
Tras ello, se creará el correspondiente fichero de migración ..._añade_imagen_al_modelo_post.py en el directorio migrations/versions/.

Ahora hay que llevar a cabo la migración. Ejecuta lo siguiente desde el terminal:

$> flask db upgrade
Una vez que se haya completado la migración, ya lo tenemos todo listo para pasar a la siguiente sección.

Procesar ficheros en Flask de forma nativa
En esta sección te mostraré cómo procesar ficheros en Flask de forma nativa. Cuando se envía un formulario que contiene un fichero a una aplicación Flask, puedes acceder al fichero y sus metadatos a través del diccionario files del objeto request. Cada uno de los elementos del diccionario es de tipo FileStorage. Para guardar un fichero de este tipo, simplemente tienes que llamar a su método save(), indicando la ruta del sistema de ficheros dónde lo quieres guardar.

Veámoslo mejor con un ejemplo.

Lo primero que haremos será modificar el formulario que se utiliza para guardar un post.

❗️¡RECUERDA! Para enviar ficheros en un formulario HTML, este debe indicar en el atributo enctype el valor multipart/form-data.

Abre el formulario que se encuentra en app/admin/templates/admin/post_form.html. Añádele el atributo enctype y un campo de tipo file como te indico a continuación:

...
<form action="" method="post" enctype="multipart/form-data" novalidate>
    {{ form.hidden_tag() }}
    <div>
        {{ form.title.label }}
        {{ form.title(size=128) }}<br>
    ...
    <div>
        <label for="postImage">Imagen de cabecera:</label>
        <input type="file" id="postImage" name="post_image" accept="image/png, image/jpeg">
    </div>
    <div>
        {{ form.submit() }}
    </div>
</form>
...
Como ves, he añadido un campo de tipo file y lo he llamado post_image. Este nombre nos servirá para recuperar posteriormente el fichero al procesar la petición.

Ahora vamos a definir un parámetro de configuración para indicar el directorio en el que se guardarán las imágenes. Para ello, abre el fichero config/default.py y añade las siguientes líneas (justo después del parámetro BASE_DIR):

from os.path import abspath, dirname, join
# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))
# Media dir
MEDIA_DIR = join(BASE_DIR, 'media')
POSTS_IMAGES_DIR = join(MEDIA_DIR, 'posts')
SECRET_KEY = ...
Como puedes apreciar, las imágenes de cabecera se guardarán en el directorio media/posts dentro de la carpeta del proyecto.

El último paso consiste en procesar el fichero en Flask, de manera que guardemos la imagen en el sistema de ficheros. Para ello, modificaremos la vista post_form() que se encuentra en app/admin/routes.py:

import os
from flask request, current_app
from werkzeug.utils import secure_filename
@admin_bp.route("/admin/post/", methods=['GET', 'POST'])
@login_required
@admin_required
def post_form():
    """Crea un nuevo post"""
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        image_name = None
        # Comprueba si la petición contiene la parte del fichero
        if 'post_image' in request.files:
            file = request.files['post_image']
            # Si el usuario no selecciona un fichero, el navegador
            # enviará una parte vacía sin nombre de fichero
            if file.filename:
                image_name = secure_filename(file.filename)
                images_dir = current_app.config['POSTS_IMAGES_DIR']
                os.makedirs(images_dir, exist_ok=True)
                file_path = os.path.join(images_dir, image_name)
                file.save(file_path)
        post = Post(user_id=current_user.id, title=title, content=content)
        post.image_name = image_name
        post.save()
        logger.info(f'Guardando nuevo post {title}')
        return redirect(url_for('admin.list_posts'))
    return render_template("admin/post_form.html", form=form)
Al procesar la respuesta se comprueba si el campo del fichero, post_image, se ha enviado. En caso afirmativo, llamamos a la función secure_filename() para generar un nombre de fichero seguro y apropiado. Después, creamos el directorio media/posts si no existe. Por último, guardamos el fichero con el método save() y asignamos el nombre de la imagen al objeto post.

❗️ ¡ATENCIÓN! Si quieres usar el nombre original del archivo, recuerda llamar siempre a la función secure_filename().

Procesar ficheros en Flask con Flask-WTF
En la sección anterior hemos visto cómo procesar ficheros en Flask de forma nativa. Sin embargo, nosotros estamos usando la extensión Flask-WTF para procesar los formularios. En lo que sigue, veremos cómo procesar ficheros haciendo uso de esta extensión.

Actualiza el formulario del post
Lo primero que haremos será actualizar el formulario PostForm para añadirle un campo de tipo FileField. Abre el fichero app/admin/forms.py y modifica el formulario como te indico a continuación:

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# Resto de imports
...
class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField('Contenido')
    post_image = FileField('Imagen de cabecera', validators=[
        FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes')
    ])
    submit = SubmitField('Guardar')
...
Observa que he añadido el validador FileAllowed para permitir solo archivos de tipo jpg y png.

Actualiza la plantilla del formulario
El siguiente paso será actualizar la plantilla del formulario para añadir el campo de la imagen. Abre el archivo app/admin/templates/admin/post_form.html y copia en él lo referente al campo post_image:

...
<form action="" method="post" enctype="multipart/form-data" novalidate>
    {{ form.hidden_tag() }}
    <div>
        {{ form.title.label }}
        {{ form.title(size=128) }}<br>
    ...
    <div>
        {{ form.post_image.label }}
        {{ form.post_image }}<br>
        {% for error in form.post_image.errors %}
        <span style="color: red;">{{ error }}</span>
        {% endfor %}
    </div>
    ...
</form>
...
Actualiza la vista post_form
Finalmente, tenemos que modificar la vista post_form() que se encuentra en el fichero app/admin/routes.py:

@admin_bp.route("/admin/post/", methods=['GET', 'POST'])
@login_required
@admin_required
def post_form():
    """Crea un nuevo post"""
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        file = form.post_image.data
        image_name = None
        # Comprueba si la petición contiene la parte del fichero
        if file:
            image_name = secure_filename(file.filename)
            images_dir = current_app.config['POSTS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)
        post = Post(user_id=current_user.id, title=title, content=content)
        post.image_name = image_name
        post.save()
        logger.info(f'Guardando nuevo post {title}')
        return redirect(url_for('admin.list_posts'))
    return render_template("admin/post_form.html", form=form)
El código es muy similar al que vimos en la sección anterior. En esta ocasión, si el usuario indicó un fichero, el atributo data correspondiente será distinto de None. De nuevo, tal y como te indiqué previamente, se hace uso de la función secure_filename() para obtener un nombre de fichero seguro.

✏️ NOTA: Como ejercicio, haz los mismos cambios en la vista update_post_form.

Mostrar las imágenes en el blog
El último paso que nos queda es servir las imágenes contenidas en media/posts/ para mostrarlas en la página de detalle de cada entrada.

❗️ ¡ATENCIÓN! Debido a temas de rendimiento, los recursos estáticos (hojas de estilo, javascript, imágenes, …) deben ser servidos por un servidor web, como NGINX o Apache, o desde un CDN. Lo que aquí te voy a contar es solamente informativo y para ser usado con el servidor de pruebas que incorpora Flask. En la siguiente lección veremos cómo servir los recursos estáticos desde un servidor de producción.

Añade la siguiente vista al final del fichero entrypoint.py:

from flask import send_from_directory
@app.route('/media/posts/<filename>')
def media_posts(filename):
    dir_path = os.path.join(
        app.config['MEDIA_DIR'],
        app.config['POSTS_IMAGES_DIR'])
    return send_from_directory(dir_path, filename)
A continuación, actualiza la plantilla app/public/templates/public/post_view.html, para mostrar la imagen de cabecera en caso de que exista:

...
{% block content %}
    <h1>{{ post.title }}</h1>
    <div>
        <span class="blogDate">{{ post.created|datetime('full') }}</span>
    </div>
    {% if post.image_name %}
        <div>
            <img src="{{ url_for('media_posts', filename=post.image_name) }}" />
        </div>
    {% endif %}
    {{ post.content }}
    ...
{% endblock %}
Y… Objetivo cumplido 🎉 Prueba a crear un post con una imagen y a acceder posteriormente al mismo. El resultado debería ser algo así:

Procesar ficheros con Flask - Guardar una imagen
Con esto damos por terminada la lección 😉

Conclusión
Tal y como te advertí al comienzo, esta lección ha sido especialmente práctica. En ella hemos visto las claves para procesar formularios en Flask, tanto de forma nativa como usando Flask-WTF. También hemos repasado cómo guardar imágenes en el sistema de ficheros y cómo servirlas desde el propio servidor interno de Flask.

Sin embargo, existen puntos de mejora en este procesamiento básico de formularios. Te detallo unos cuántos a continuación:

Limitar el tamaño de la petición, tanto en el servidor web como en la propia aplicación Flask.
Enviar un fichero mostrando barras de progreso.
Servir los recursos públicos desde un servidor web y no desde la aplicación Flask.
Implementar la lógica necesaria para guardar dos ficheros que se llamen igual. Actualmente, el método save() sobreescribe los archivos.
Como siempre, si tienes alguna duda puedes ponerte en contacto conmigo dejándome un mensaje al final del post, a través de mis redes sociales o enviándome un email. Estaré encantado de poder ayudarte.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 16 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion16 -b leccion16

Después de este viaje que hemos recorrido juntos, te espero en la siguiente lección que, como sabrás, es la última de este tutorial. En ella veremos cómo desplegar la aplicación en un entorno de producción real. ¡No te la pierdas!
Lección 11: Actualizar la base de datos SQLAlchemy
Categoría: Flask
flask, medio, python, tutorial flask
Lección 11 Actualizar la base de datos SQLAlchemy
Las aplicaciones son entes vivos que están en continua evolución. Los cambios suelen ser frecuentes: nuevas funcionalidades, mejoras, corrección de errores… ¡¡¡Y todo va bien hasta que hay que actualizar la base de datos de producción!!! ¡Atención, atención! Se avecina una catástrofe… 😫

Bueno, no hay que ponerse tan dramático porque la cosa no es para tanto. Si por cualquier motivo tuvieras que hacer cambios en el esquema de tu base de datos, estás en el lugar indicado para descubrir cómo hacerlo sin que ello te suponga un dolor de cabeza.

En esta lección vamos a ver cómo los cambios en los modelos de la aplicación son inevitables: nuevos modelos, nuevos campos, … Y cómo hacer las correspondientes modificaciones en el esquema de la base de datos de una manera muy, muy sencilla. ¿A que estás deseando empezar? ¡Pues vamos a ello!

Recuerda que este tutorial es una continuación de la lección anterior, en la que vimos cómo aplicar seguridad a las vistas con el uso de decoradores. Así que si te has despistado o no has seguido todas las lecciones del tutorial, puedes descargar el código por donde lo dejamos como te indico a continuación:

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 10 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion10 -b leccion10

Índice
Aquí te dejo los puntos principales de esta lección:

Actualizar la base de datos de forma manual
Flask-Migrate para actualizar la base de datos
Instalación y uso de Flask-Migrate
Actualizando el modelo Post con Flask-migrate
Añadiendo un nuevo modelo a la base de datos
Actualizar la base de datos de forma manual
Como te adelantaba al principio de esta lección, las modificaciones en las aplicaciones son constantes. Un proyecto nunca se da por terminado (a no ser que se acabe el dinero y/o el cliente ya no te quiera pagar más 🤷🏻‍♂️).

Volviendo a nuestro miniblog, vamos a revisar el modelo Post. Sí, es cierto que es un modelo muy simple pero no olvides que esto es un tutorial. Aún así, vamos a mejorar el modelo añadiendo un nuevo campo para almacenar la fecha en que se crea cada entrada del blog.

Abre el fichero app/models.py y en la clase Post añade el campo created:

import datetime
# Otros import
...
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ...
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    def __repr__(self):
        return f'<Post {self.title}>'
    # Resto de métodos
    ...
El campo created es de tipo DateTime y, por defecto, almacenará la fecha del instante en que se guarde el post.

Ahora ejecuta el servidor de Flask e intenta acceder desde el navegador a la página principal del blog http://localhost:5000

Pues sí, ¡¡error a la vista!! La columna post.created no existe.

Error SQLAlchemy tabla no se corresponde con modelo
SQLAlchemy se queja de que no encuentra en la base de datos la columna created que sí aparece en el modelo Post.

Añadiendo el campo created a mano
Inicialmente, SQLAlchemy no nos ofrece ninguna solución más que el método create_all() para crear todas las tablas de la base de datos. Recuerda que ya ejecutamos ese método en el tutorial 5, cuando creamos la base de datos. Este método aparentemente está bien si tenemos los modelos definitivos, cosa que rara vez ocurre. Por tanto, nos toca actualizar la base de datos a mano.

Abre un shell de la base de datos que estés utilizando y ejecuta lo siguiente:

$> Alter table post add column created TIMESTAMP;
Con ello, añadiremos la columna created a la tabla post.

Y todo este jaleo para añadir un campo a un modelo. ¿Te imaginas tener que añadir 5 modelos nuevos y 3 campos a uno ya existente, cada uno en un fichero models.py distinto? ¡Se lía y bien gorda! ¿Dónde guardas los ficheros SQL con las sentencias para actualizar la base de datos? ¿Cómo sabes el orden en que se tienen que ejecutar? ¿Se guardan en el sistema de control de versiones?

Bien, pues todo esto es lo que nos viene a solucionar Flask-Migrate.

Flask-Migrate para actualizar la base de datos
Flask-Migrate es una extensión basada en Alembic que se utiliza para llevar a cabo migraciones de bases de datos cuando usas SQLAlchemy como ORM. Como veremos a continuación, esta extensión detecta los cambios realizados en nuestros modelos (nuevos modelos, nuevos campos, …) y genera unos scripts con los que fácilmente podremos llevar a cabo las actualizaciones de la base de datos. Todo de manera casi automática y sin tocar nada de código.

Mi recomendación si vas a usar SQLAlchemy o Flask-SQLAlchemy es que la utilices desde el principio, siguiendo los pasos que te mostraré ahora.

Sin embargo, antes de ver Flask-Migrate en acción, vamos a simular que partimos de cero, como si no hubiéramos hecho nada. Es decir, comenta el campo created del modelo Post y elimina la base de datos por completo 😢. Espero que solo hayas guardado datos de prueba, jaja.

De nuevo, abre el shell de tu base de datos y ejecuta las dos sentencias siguientes, una después de la otra:

$> DROP DATABASE miniblog;
$> CREATE DATABASE miniblog;
Con esto ya disponemos de una base de datos vacía.

Instalación y uso de Flask-Migrate
Lo primero que haremos para usar Flask-Migrate en nuestra aplicación es instalarlo. Activa tu entorno virtual Python y ejecuta el siguiente comando:

$> pip install flask-migrate
Una vez instalado, hay que crear una instancia del objeto Migrate en nuestra aplicación e inicializarlo correctamente. Abre el fichero app/__init__.py y añade las siguientes líneas en los lugares que indico:

from flask_migrate import Migrate
# Otros import
...
db = SQLAlchemy()
migrate = Migrate()  # Se crea un objeto de tipo Migrate
def create_app(settings_module):
    # Inicialización de los parámetros de configuración
    ...
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)
    migrate.init_app(app, db)  # Se inicializa el objeto migrate
    # Resto del código
    ...
Comandos principales de Flask-Migrate
Ahora sí, ya podemos utilizar Flask-Migrate. Pero antes, quiero indicarte que Flask-Migrate se utiliza desde una interfaz de línea de comandos. Los tres comandos principales de Flask-Migrate son:

flask db init: Crea una estructura de directorios y ficheros necesarios para la ejecución de esta extensión. Se ejecuta solo una vez, al principio.
flask db migrate: Navega entre los modelos en busca de actualizaciones y genera los ficheros de migración de base de datos con los cambios detectados.
flask db upgrade: Lleva a cabo la migración de la base de datos.
Uso de Flask-Migrate paso a paso
¿Preparad@ para la acción? No te hago esperar más. Vamos a seguir los pasos para crear las tablas de la base de datos como si partiéramos de cero.

Lo primero que necesitamos son unos modelos iniciales. Ya los tenemos: Post y User.

Lo segundo que debemos hacer es invocar al comando init. Desde un terminal ejecuta lo siguiente:

$> flask db init
Después de ejecutarlo verás que se ha creado dentro de la carpeta del proyecto un directorio llamado migrations. Este directorio debes añadirlo al sistema de control de versiones.

A continuación ejecuta el siguiente comando:

$> flask db migrate -m "Initial database"
Lo que hace este comando es generar un nuevo fichero con código python que incluye todos los cambios que hay seguir para actualizar la base de datos. Es un fichero de migración y se guarda en el directorio migrations/versions. Este directorio contiene todos los ficheros de migración de base de datos que se generan con Flask-Migrate. Dentro de él verás que tienes un fichero que se llama algo así como cb86527f8105_initial_database.py

Ábrelo y échale un vistazo. Probablemente no entiendas nada de primeras, pero te puedes hacer una idea de qué está haciendo. Es una buena práctica revisar los ficheros nuevos que se vayan generando y comprobar que todo es correcto. En este caso, podemos apreciar que hay operaciones para crear las tablas blog_user y post, correspondientes a nuestros modelos.

El último paso es llevar a cabo la migración para que se creen estas tablas. Para ello, ejecuta el tercer comando que te adelanté previamente:

$> flask db upgrade
Y… ¡MAGIA! Si lo has hecho todo correctamente, verás que se han creado las tablas blog_user y post en tu base de datos, aunque también se ha creado una tercera tabla llamada alembic_version. No borres ni modifiques esta última, ya que es utilizada por Flask-Migrate para llevar un control del estado de las migraciones.

Aunque te he desgranado los pasos de un uso simplificado de Flask-Migrate, en el mundo real no es tan bonito y sencillo cuando hay varias personas trabajando en un mismo proyecto. Dado este caso, te puedes encontrar con situaciones de conflicto entre los ficheros de migración, pero esto da para otro post…

❗️ ¡ATENCIÓN! Recuerda crear un usuario administrador en la base de datos.

Actualizando el modelo Post con Flask-migrate
Volvamos al comienzo de la lección para que puedas apreciar todo el potencial de Flask-Migrate. La idea era añadir un campo al modelo Post con la fecha en que se creaba una entrada en la base de datos. ¿Recuerdas que lo comentamos? Quita el comentario sobre el campo created. Al quitar el comentario añadimos un cambio a nuestro modelo y, por consiguiente, tiene que verse reflejado en la base de datos.

Siguiendo los mismos pasos que te indiqué en la sección anterior, vamos a generar un fichero con las instrucciones de la migración y a llevarla a cabo.

Ejecuta lo siguiente desde el terminal:

$> flask db migrate -m "Añade campo created a Post"
Esto creará un nuevo fichero de migración. El mío se llama 262155567f30_añade_campo_created_a_post.py. A ti se te ha debido crear un fichero con un nombre similar.

Si lo abres, verás que dentro del método upgrade hay una operación para añadir la columna created a la tabla post. Además, si te fijas bien, al comienzo de este fichero hay una directiva llamada Revises que apunta al id del fichero de migración anterior (el que creamos primero).

Para llevar a cabo la actualización en la base de datos, ejecuta ahora el siguiente comando:

$> flask db upgrade
Después de hacerlo verás que a la tabla post se le ha añadido la columna created. Si ahora accedes desde el navegador a la URL http://localhost:5000, no debe aparecerte ningún error.

¡Enhorabuena! 🎉🎉 Ya sabes cómo modificar y añadir nuevos modelos y llevar a cabo las migraciones en tu base de datos.

Añadiendo un nuevo modelo a la base de datos
En esta sección veremos un resumen de todo lo aprendido en esta y otras lecciones. El objetivo: Permitir a los usuarios invitados añadir comentarios a un post.

Nuevo formulario para crear comentarios
Lo primero que haremos será crear un nuevo formulario. Añade un fichero llamado forms.py en el directorio app/public con este contenido:

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
class CommentForm(FlaskForm):
    content = TextAreaField('Contenido', validators=[DataRequired(), ])
    submit = SubmitField('Comentar')
Nuevo modelo Comment
El siguiente paso será añadir un nuevo modelo para guardar en base de datos los comentarios asociados a un post. Abre el fichero app/models.py y añade al final el modelo Comment:

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='SET NULL'))
    user_name = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    def __init__(self, content, user_id=None, user_name=user_name, post_id=None):
        self.content = content
        self.user_id = user_id
        self.user_name = user_name
        self.post_id = post_id
    def __repr__(self):
        return f'<Comment {self.content}>'
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @staticmethod
    def get_by_post_id(post_id):
        return Comment.query.filter_by(post_id=post_id).all()
Además, añadiremos al modelo Post una relación llamada comments para que desde un post podamos acceder de manera sencilla a su listado de comentarios.

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ...
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan', order_by='asc(Comment.created)')
Actualizar la lógica de la vista show_post
A continuación modificamos la implementación de la vista show_post() del siguiente modo:

@public_bp.route("/p/<string:slug>/", methods=['GET', 'POST'])
def show_post(slug):
    logger.info('Mostrando un post')
    logger.debug(f'Slug: {slug}')
    post = Post.get_by_slug(slug)
    if not post:
        logger.info(f'El post {slug} no existe')
        abort(404)
    form = CommentForm()
    if current_user.is_authenticated and form.validate_on_submit():
        content = form.content.data
        comment = Comment(content=content, user_id=current_user.id,
                          user_name=current_user.name, post_id=post.id)
        comment.save()
        return redirect(url_for('public.show_post', slug=post.title_slug))
    return render_template("public/post_view.html", post=post, form=form)
Los cambios que he introducido han sido el procesamiento del formulario CommentForm, que se realiza solo en caso de que el usuario esté autenticado, y pasar dicho formulario a la plantilla.

Actualizar la plantilla post_view.html
Por último, he actualizado la plantilla app/public/templates/public/post_view.html. En ella, he añadido el formulario para añadir un comentario y, al final, un bucle for para mostrar los comentarios asociados al post.

{% extends "base_template.html" %}
{% block title %}{{ post.title }}{% endblock %}
{% block content %}
    <h1>{{ post.title }}</h1>
    {{ post.content }}
    <h2>Comentarios</h2>
    {% if current_user.is_authenticated %}
    <div>
        <form action="" method="post" novalidate>
            {{ form.hidden_tag() }}
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
    </div>
    {% endif %}
    <div id="comments">
        {% for comment in post.comments %}
            <div>
                <div>El usuario {{ comment.user_name }} comentó:</div>
                <div>{{ comment.content }}</div>
            </div>
        {% endfor %}
    </div>
{% endblock %}
Con esto llegamos al final de esta lección 😉

Conclusión
Creo que ha sido una lección muy productiva en la que has afianzado conceptos vistos en lecciones anteriores, hemos vuelto a trabajar con la base de datos y donde has descubierto el uso de Flask-Migrate para actualizar la base de datos de una manera eficiente y segura.

En resumen, los pasos para usar Flask-Migrate son:

1: Crea tus modelos iniciales.
2: Crea la base de datos
3: Ejecuta el comando init.
4: Ejecuta el comando migrate.
5: Revisa el código del fichero que contiene las instrucciones para la migración y verifica que está todo correcto.
6: Ejecuta el comando upgrade.
7: Realiza cambios en tus modelos.
8: Vuelve al PASO 4.
Como siempre, si tienes alguna duda puedes ponerte en contacto conmigo dejándome un mensaje al final del post, a través de mis redes sociales o enviándome un email. Estaré encantado de poder ayudarte.

‼️ ATENCIÓN ‼️

🎯 Puedes descargar el código correspondiente a la Lección 11 desde el siguiente repositorio de Github:

git clone https://github.com/j2logo/tutorial-flask.git
git checkout tags/leccion11 -b leccion11

En el siguiente tutorial veremos un tema súper importante: cómo implementar test unitarios y de integración con Flask. Gracias a esto, conseguiremos que nuestra aplicación sea más robusta. ¡No te la pierdas!
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import SMTPHandler
from flask_migrate import Migrate
from flask_mail import Mail         # 1. Importamos la clase Mail


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()     # Se crea un objeto de tipo Migrate
mail = Mail()  # 2. Instanciamos un objeto de tipo Mail


# Añadimos un filtro para el formateo de fechas-horas en jinja
from app.common.filters import format_datetime

def register_filters(app):
    app.jinja_env.filters['datetime'] = format_datetime



def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    # ❗️El método from_object solo tendrá en cuenta aquellas claves que encuentre en MAYÚSCULAS.

    configure_logging(app)
    
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)
    migrate.init_app(app, db)       # Se inicializa el objeto migrate
    mail.init_app(app)          # 3. Inicializamos el objeto mail

    # Registro de los filtros
    register_filters(app)
    
    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    with app.app_context():
        db.create_all() 
    
    # Custom error handlers
    register_error_handlers(app)

    return app




def register_error_handlers(app):

    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(401)
    def error_404_handler(e):
        return render_template('401.html'), 401




def configure_logging(app):
    # Eliminamos los posibles manejadores, si existen, del logger por defecto
    del app.logger.handlers[:]

    # Añadimos el logger por defecto a la lista de loggers
    loggers = [app.logger, ]
    handlers = []

    # Creamos un manejador para escribir los mensajes por consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())
    
    if app.config['APP_ENV'] == 'DES':
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == 'PRO':
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
    
    # Asociamos cada uno de los handlers a cada uno de los loggers
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)


def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
        )


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
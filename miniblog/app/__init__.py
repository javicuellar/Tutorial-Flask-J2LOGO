from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
db = SQLAlchemy()




def create_app(settings_module='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    # ❗️El método from_object solo tendrá en cuenta aquellas claves que encuentre en MAYÚSCULAS.

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)

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
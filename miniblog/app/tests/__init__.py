import unittest

from app import create_app, db
from instance.config import Config_test
from app.auth.models import User




#  Para ejecutar test, desde el directorio de la aplicación, en lugar de ejecutarla, ejecutar: python -m unittest


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app(Config_test)
        self.client = self.app.test_client()

        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()
        
            # Creamos un usuario administrador
            BaseTestClass.create_user('admin', 'admin@xyz.com', '1111', True)
            # Creamos un usuario invitado
            BaseTestClass.create_user('guest', 'guest@xyz.com', '1111', False)


    def tearDown(self):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()
    

    def login(self, email, password):
        return self.client.post('/login', data=dict(email=email, password=password), 
                                follow_redirects=True)



    @staticmethod
    def create_user(name, email, password, is_admin):
        # user = User(name, email, password, is_admin)          # No funciona, lo he hecho campo a campo
        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.is_admin = is_admin
        user.save()
        return user
from . import BaseTestClass
from app.auth.models import User
from app.models import Post




class BlogClientTestCase(BaseTestClass):

    def test_index_with_no_posts(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'No hay entradas', res.data)


    def test_index_with_posts(self):
        with self.app.app_context():
            admin = User.get_by_email('admin@xyz.com')
            post = Post(user_id=admin.id, title='Post de prueba', content='Lorem Ipsum')
            post.save()
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        self.assertNotIn(b'No hay entradas', res.data)
    

    def test_redirect_to_login(self):
        res = self.client.get('/admin/')
        self.assertEqual(302, res.status_code)
        self.assertIn('login', res.location)
    

    '''
    acceso no autorizado, haciendo uso del método login()
    '''
    def test_unauthorized_access_to_admin(self):
        self.login('guest@xyz.com', '1111')
        res = self.client.get('/admin/')
        self.assertEqual(401, res.status_code)
        self.assertIn(b'Ooops!! No tienes permisos de acceso', res.data)
    

    '''
    asegurarnos de que un usuario de tipo administrador está autorizado para acceder a las páginas de administración del blog
    '''
    def test_authorized_access_to_admin(self):
        self.login('admin@xyz.com', '1111')
        res = self.client.get('/admin/')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Posts', res.data)
        self.assertIn(b'Usuarios', res.data)
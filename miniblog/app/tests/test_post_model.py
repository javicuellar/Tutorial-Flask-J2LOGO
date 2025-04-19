import unittest

from app.auth.models import User
from app.models import Post
from . import BaseTestClass




class PostModelTestCase(BaseTestClass):
    """Suite de tests del modelo Post"""
    
    def test_title_slug(self):
        '''
        El test test_title_slug() comprueba que el campo title_slug se genera correctamente. Si ejecutas los tests, 
        verás que pasa correctamente.
        '''
        with self.app.app_context():
            admin = User.get_by_email('admin@xyz.com')
            post = Post(user_id=admin.id, title='Post de prueba', content='Lorem Ipsum')
            post.save()
            self.assertEqual('post-de-prueba', post.title_slug)


    def test_title_slug_duplicated(self):
        '''
        test test_title_slug_duplicated(). En este test comprobamos que al guardar dos posts con el mismo título, el segundo
        añade el sufijo -1 al campo title_slug
        '''
        with self.app.app_context():
            admin = User.get_by_email('admin@xyz.com')
            post = Post(user_id=admin.id, title='Prueba', content='Lorem Ipsum')
            post.save()
            
            post_2 = Post(user_id=admin.id, title='Prueba', content='Lorem Ipsum Lorem Ipsum')
            post_2.save()
            self.assertEqual('prueba-1', post_2.title_slug)
            
            post_3 = Post(user_id=admin.id, title='Prueba', content='Lorem Ipsum Lorem Ipsum')
            post_3.save()
            self.assertEqual('prueba-2', post_3.title_slug)
            
            posts = Post.get_all()
            self.assertEqual(3, len(posts))
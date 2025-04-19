import unittest



class TestSuite(unittest.TestCase):
    def setUp(self):
        # Código que se ejecuta antes de cada test
        ...

    def test_mi_test(self):
        # Código que se quiere probar
        ...

    def tearDown(self):
        # Código que se ejecuta después de cada test
        ...


with app.app_context():
    # Código que depende del contexto de aplicación
    # como el acceso a base de datos
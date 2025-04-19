# Este fichero es el punto de entrada a la aplicación. En él se crea la aplicación y se lanza el servidor de desarrollo.
from app import create_app
from instance.config import Config_des





app = create_app(Config_des)



if __name__ == '__main__':    
    app.run(port=5008)
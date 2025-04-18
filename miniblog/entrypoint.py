# Este fichero es el punto de entrada a la aplicación. En él se crea la aplicación y se lanza el servidor de desarrollo.
from app import create_app



app = create_app()




if __name__ == '__main__':    
    app.run(debug=True, port=5008)
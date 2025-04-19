# Este fichero es el punto de entrada a la aplicación. En él se crea la aplicación y se lanza el servidor de desarrollo.
from app import create_app
from instance.config import Config_des





app = create_app(Config_des)


import os
from flask import send_from_directory

@app.route('/media/posts/<filename>')
def media_posts(filename):
    dir_path = os.path.join(
        app.config['MEDIA_DIR'],
        app.config['POSTS_IMAGES_DIR'])
    return send_from_directory(dir_path, filename)




if __name__ == '__main__':    
    app.run(port=5008)
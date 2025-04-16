export FLASK_APP = "run.py"
export FLASK_RUN_PORT = 5004
#  Modo debub
export FLASK_ENV="development"
# Activar el modo debug hace que:
#   - Se active un depurador.
#   - Se tengan en cuenta los cambios después de guardarlos sin tener que reiniciar manualmente el servidor.
#   - Activa el modo debug, de manera que si se produce una excepción o error en la aplicación veremos una traza de los mismos.


flask run

#  si no se indica nada, es accesible únicamente desde el mismo PC
@  si se quiere que sea accesible desde la red local
flask run --host 0.0.0.0
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, BooleanField)
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed




class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField('Contenido')
    post_image = FileField('Imagen de cabecera', validators=[
                    FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes')
                    ])
    submit = SubmitField('Guardar')
    # submit = SubmitField('Enviar')



class UserAdminForm(FlaskForm):
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Guardar')
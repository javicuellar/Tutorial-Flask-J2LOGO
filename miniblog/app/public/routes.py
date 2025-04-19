from flask import abort, render_template, redirect, url_for,request, current_app
from werkzeug.exceptions import NotFound
from .forms import CommentForm
from flask_login import current_user

from app.models import Post, Comment
from . import public_bp

import logging

logger = logging.getLogger(__name__)        # su nombre es el del módulo


from flask_mail import Message
from app import mail




@public_bp.route("/")
def index():
    # Añadimos código para avisar que visitan la aplicación
    # El envío se hace de forma sincrona (esparamos hasta que se envía)
    msg = Message("Hola",
              sender="from@example.com",
              recipients=["javicu25@gmail.com"])

    msg.body = 'Bienvenid@ a j2logo'
    msg.html = '<p>Bienvenid@ a <strong>j2logo</strong></p>'

    mail.send(msg)
    # Se envía un mensaje asincrono al registrase (auth.routes)
    

    current_app.logger.error('Mostrando los posts del blog')
    logger.info('Mostrando los posts del blog (más detalle del módulo)')
    # posts = Post.all_paginated(2, 3)
    # return render_template("public/index.html", posts=posts.items)
    page = int(request.args.get('page', 1))         # recuperamos de la URL la página, 1 por defecto
    # post_pagination = Post.all_paginated(page, 3)   # 3 elementos por página

    # El número de elementos por página, lo recogemos de los parámetros de configuración, definidos en config.py
    per_page = current_app.config['ITEMS_PER_PAGE']
    post_pagination = Post.all_paginated(page, per_page)

    # En lugar de pasar los post, o post.items, pasamos el objeto paginación
    # modificando index.html para tratarlo
    return render_template("public/index.html", post_pagination=post_pagination, per_page=per_page)


@public_bp.route("/p/<string:slug>/", methods=["GET", "POST"])
def show_post(slug):
    # Mostrando losg de diferentes niveles
    logger.info('Mostrando un post')
    logger.debug(f'Slug: {slug}')
    
    post = Post.get_by_slug(slug)
    # if post is None:
    if not post:
        logger.info(f'El post {slug} no existe')
        # abort(404)
        raise NotFound(slug)
    
    form = CommentForm()
    if current_user.is_authenticated and form.validate_on_submit():
        content = form.content.data
        comment = Comment(content=content, user_id=current_user.id,
                          user_name=current_user.name, post_id=post.id)
        comment.save()
        return redirect(url_for('public.show_post', slug=post.title_slug))
    
    return render_template("public/post_view.html", post=post, form=form)

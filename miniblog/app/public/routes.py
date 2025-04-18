from flask import abort, render_template, redirect, url_for, current_app
from werkzeug.exceptions import NotFound
from .forms import CommentForm
from flask_login import current_user

from app.models import Post, Comment
from . import public_bp

import logging

logger = logging.getLogger(__name__)        # su nombre es el del módulo



@public_bp.route("/")
def index():
    current_app.logger.error('Mostrando los posts del blog')
    logger.info('Mostrando los posts del blog (más detalle del módulo)')
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)



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

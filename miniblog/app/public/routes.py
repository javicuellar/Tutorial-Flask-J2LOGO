from flask import abort, render_template, current_app
from werkzeug.exceptions import NotFound

from app.models import Post
from . import public_bp

import logging

logger = logging.getLogger(__name__)        # su nombre es el del módulo



@public_bp.route("/")
def index():
    current_app.logger.error('Mostrando los posts del blog')
    logger.info('Mostrando los posts del blog (más detalle del módulo)')
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)


@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    # Mostrando losg de diferentes niveles
    logger.info('Mostrando un post')
    logger.debug(f'Slug: {slug}')
    
    post = Post.get_by_slug(slug)
    if post is None:
        raise NotFound(slug)
    return render_template("public/post_view.html", post=post)

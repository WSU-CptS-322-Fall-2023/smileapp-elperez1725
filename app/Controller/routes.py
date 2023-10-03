from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from config import Config
from app import db
from app.Model.models import Post, Tag, postTags
from app.Controller.forms import PostForm, SortForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/create', methods=['GET', 'POST'])
def postsmile():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, happiness_level=form.happiness_level.data, user_id=current_user.get_id())
        for tag in form.tag.data:
            post.tags.append(tag)

       
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('routes.index'))
    return render_template('create.html', title="Smile Portal", form=form)


@bp_routes.route('/index', methods=['GET', 'POST'])
def index():
    sort_form = SortForm()
    order = Post.timestamp.desc()  

    if sort_form.validate_on_submit():
        sort_by = sort_form.sort_by.data
        if sort_by == 'date':  
            order = Post.timestamp.desc()
        elif sort_by == 'title':  
            order = Post.title.desc() 
        elif sort_by == 'likes':  
            order = Post.likes.desc() 
        elif sort_by == 'happiness':  
            order = Post.happiness_level.desc() 

    if sort_form.display_posts.data:
        posts = current_user.get_user_posts().order_by(order).all()
    else:

        posts = Post.query.order_by(order).all()


    return render_template('index.html', title="Smile Portal", posts=posts, sort_form=sort_form)


@bp_routes.route('/like/<post_id>', methods=['POST'])
def like(post_id):
    likes = Post.query.get(post_id)
    likes.likes += 1
    db.session.add(likes)
    db.session.commit()
    return redirect(url_for('routes.index'))


@bp_routes.route('/deletepost/<post_id>', methods=['POST', 'DELETE'])
def delete(post_id):
    post = Post.query.get(post_id)
    if post.user_id == current_user.id:
        for t in post.tags:
            post.tags.remove(t)
        db.session.delete(post)
        db.session.commit()

    return redirect(url_for('routes.index'))


from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from config import Config
from app.Controller.auth_forms import RegistrationForm, LoginForm
from app.Model.models import User

from app import db




bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

@bp_auth.route('/register', methods=['GET','POST'])
def register():
    print("Register route triggered!")
    form = RegistrationForm()
    if form.validate_on_submit():
        print("wodsaof")
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password1.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('routes.index'))
    else:
        ("burhhhh")
        print(form.errors)
    return render_template('register.html', form=form)

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
       return redirect(url_for('routes.index'))

    form = LoginForm()
    if form.validate_on_submit():
       
        user = User.query.filter_by(username=form.username.data).first()

        if (user is not None) and (user.check_password(form.password.data)):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('routes.index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
    
       
    
    return render_template('login.html', form=form)



@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))
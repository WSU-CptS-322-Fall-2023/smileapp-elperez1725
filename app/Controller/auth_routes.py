from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from config import Config
from app.Controller.auth_forms import RegistrationForm
from app.Model.models import User

from app import db



bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password1.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('routes.index'))
    else:
        print(form.errors)
    return render_template('register.html', form=form)

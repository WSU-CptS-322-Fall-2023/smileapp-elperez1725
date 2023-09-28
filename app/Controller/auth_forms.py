from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length,Email




class RegistrationForm(FlaskForm):
    username = StringField("Username",  validators=[DataRequired(message="Username is required")])
    email = StringField("Email", validators=[DataRequired(message="Email is required"), Email(message="Invalid email format")])
    password1 = PasswordField("Password", validators=[DataRequired(message="Password is required")])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(message="Please confirm your password"), EqualTo('password1', message='passwords do not match')])
    register = SubmitField("Register")

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional, Email

class RegisterForm(FlaskForm):
  '''Registration Form.'''

  username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=30)])
  email = StringField('Email', validators=[InputRequired(), Email(), Length(max=50)])
  first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
  last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
  '''Login Form.'''

  username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=30)])

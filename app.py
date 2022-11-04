from flask import Flask, request, render_template, redirect, flash, jsonify
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm
# from keys import key

app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY'] = 'boomerang'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def show_home():
  '''Show homepage'''
  users = User.query.all()
  return redirect('/register')

@app.route('/register')
def show_register_form():
  '''Show registration form.'''
  form = RegisterForm()

  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data

    new_user = User.register(username, password, email, first_name, last_name)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

  else:
    return render_template('newuser.html', form=form)

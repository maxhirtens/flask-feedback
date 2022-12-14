from flask import Flask, request, render_template, redirect, flash, jsonify, session
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
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

@app.route('/register', methods=['GET', 'POST'])
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
    session['username'] = new_user.username

    db.session.commit()

    return redirect(f'/users/{new_user.username}')

  else:
    return render_template('newuser.html', form=form)

@app.route('/users/<username>')
def show_user_page(username):
  '''Show user page if logged in.'''
  if username == session['username']:
    user = User.query.filter_by(username=username).first()
    return render_template('userdetails.html', user=user)
  else:
    flash('You are not authorized to see that')
    return redirect('/')

@app.route('/login', methods=["GET", "POST"])
def log_user_in():
  '''Log user in if authenticated.'''
  form = LoginForm()

  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    user = User.authenticate(username, password)
    if user:
      session['username'] = user.username
      return redirect(f'/users/{user.username}')

    else:
      return render_template('login.html', form=form)

  else:
      return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
  '''logout GET route.'''
  session.pop('username')
  return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
  '''Delete user if logged in.'''
  if username == session['username']:
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    flash('You deleted yourself')
    return redirect('/')
  else:
    flash('You are not authorized to do that')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def show_feedback_form(username):
  '''Show/submit feedback.'''
  form = FeedbackForm()

  if username != session['username']:
    flash('You are not authorized to do that')
    return redirect('/')

  if form.validate_on_submit():
    title = form.title.data
    content = form.content.data
    new_feedback = Feedback(title=title, content=content, username=username)
    db.session.add(new_feedback)
    db.session.commit()
    return redirect(f'users/{username}')

  else:
    return render_template('newfeedback.html', form=form)

@app.route('/feedback/<fbid>/update', methods=['GET', 'POST'])
def update_feedback(fbid):
  '''Update selected feedback.'''
  form = FeedbackForm()
  feedback = Feedback.query.get_or_404(fbid)

  if feedback.username != session['username']:
    flash('You are not authorized to do that')
    return redirect('/')

  if form.validate_on_submit():
    feedback.title = form.title.data
    feedback.content = form.content.data

    db.session.add(feedback)
    db.session.commit()
    return redirect(f'users/{feedback.username}')

  else:
    return render_template('updatefeedback.html', form=form, feedback=feedback)

@app.route('/feedback/<fbid>/delete', methods=['POST'])
def delete_feedback(fbid):
  '''Delete selected feedback.'''
  feedback = Feedback.query.get_or_404(fbid)

  if feedback.username != session['username']:
    flash('You are not authorized to do that')
    return redirect('/')
  else:
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'users/{feedback.username}')

"""Seed file to make sample data for db."""

from models import User, Feedback, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
tom = User.register(username='tom121', password="secret", email='test1@test.com', first_name='Tom', last_name="Doe")
dick = User.register(username='dick888', password="secret", email='test2@test.com', first_name='Dick', last_name="Doe")
harry = User.register(username='harry765', password="secret", email='test3@test.com', first_name='Harry', last_name="Doe")

# Add new objects to session, so they'll persist
db.session.add(tom)
db.session.add(dick)
db.session.add(harry)

# Commit--otherwise, this never gets saved!
db.session.commit()

# Add feedback
f1 = Feedback(title='Test 1', content='Here is some content', username='tom121')
f2 = Feedback(title='Test 2', content='Here is some more content', username='harry765')

# Add new objects to session, so they'll persist
db.session.add(f1)
db.session.add(f2)

# Commit--otherwise, this never gets saved!
db.session.commit()

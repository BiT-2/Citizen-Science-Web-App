from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import UserMixin
from datetime import datetime

app =Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique = True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	image = db.Column(db.String(20), nullable=False, default = "default.jpg")
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def get_reset_token(self, expires_secs=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_secs)
		return s.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s=Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	image_post = db.Column(db.String(20), nullable=False)
	image_recg = db.relationship('Image', backref = "image_trans", lazy = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"	

class Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	label = db.Column(db.String(50), nullable=False)
	confidence = db.Column(db.String(30), nullable = False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

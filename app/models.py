from . import db
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

class User(db.Model,UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key=True)
	account = db.Column(db.String(64),index=True,unique=True,nullable=False)
	password = db.Column(db.String(128),nullable=False)
	email = db.Column(db.String(64),unique=True,nullable=True)
	address = db.Column(db.String(64),unique=True,nullable=True)
	phone = db.Column(db.String(64),unique=True,nullable=True)
	domain = db.Column(db.String(64),unique=True,nullable=True)
	avatar = db.Column(db.String(64),nullable=True)
	posts = db.relationship('Post',backref='author',lazy='dynamic')
	comments = db.relationship('Comment',backref='author',lazy='dynamic')

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer,primary_key=True)
	body = db.Column(db.Text,nullable=False)
	timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
	author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
	picture = db.Column(db.String(64),nullable=True)
	comments = db.relationship('Comment',backref='post',lazy='dynamic')

class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer,primary_key=True)
	body = db.Column(db.Text,nullable=False)
	timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
	author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
	post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))

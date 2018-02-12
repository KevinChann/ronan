import os
#/Applications/python3/RonanProject
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'kevin chan'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	UPLOAD_AVATAR_FOLDER = os.getcwd() + '/app/static/avatar/'
	UPLOAD_PICTURE_FOLDER = os.getcwd() + '/app/static/picture/'
	POSTS_PER_PAGE = 10
	COMMENTS_PER_PAGE = 10

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	Debug = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/flaskdb'
	#SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/flaskdb'


'''
class TestingConfig
class ProductionConfig
'''

config = {
	'development' : DevelopmentConfig,
	#'testing' : TestingConfig
	#'production' :ProductionConfig
	'default' : DevelopmentConfig
}
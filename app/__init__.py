from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
#修正python3连接mysql问题
import pymysql
pymysql.install_as_MySQLdb()

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

#flask-login
login_manager = LoginManager()
login_manager.session_protection = None	#None,'basic','strong'
login_manager.login_view = 'main.login'	#blueprint-view position

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])	#加载配置
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)

	#定义路由和错误页面
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app
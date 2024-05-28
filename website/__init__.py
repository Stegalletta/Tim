from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, environ
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'iamakey'
  database_uri = str(environ.get("DATABASE_URL"))
  if database_uri.startswith("postgres://"):
      database_uri = database_uri.replace("postgres://", "postgresql://", 1)
  app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from .models import User, Note

  create_database(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))
  
  return app

def create_database(app):
    if not path.exists('website/' + 'database.uri'):
      with app.app_context():
        db.create_all()
        print('Create Database')
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from simplex.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message = "Önce giriş yapın"
login_manager.login_message_category = "danger"

from simplex.users.routes import users
from simplex.posts.routes import posts
from simplex.main.routes import main
from simplex.handler import errors

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)

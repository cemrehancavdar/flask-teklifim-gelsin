from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

postgres_local_base = ""



app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = postgres_local_base
app.config["SECRET_KEY"] = "something"

db = SQLAlchemy(app)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from project.authentication.views import auth_blueprint
from project.loan.views import app_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(app_blueprint)

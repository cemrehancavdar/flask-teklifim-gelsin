from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

postgres_local_base = "postgresql://igbmjgqxybjhty:d2355a966c9cd710af1bbc73f9b7634b32ddc3a63613c973f400c6b499a4da74@ec2-52-209-171-51.eu-west-1.compute.amazonaws.com:5432/d2kmeb77ofeojg"



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

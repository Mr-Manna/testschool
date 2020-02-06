from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_talisman import Talisman

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
app = Flask(__name__)

FLASK_DEBUG = True

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
# Setting For JWT
jwt = JWTManager(app)
# Setting for CROS
CORS(app,supports_credentials=True)
ma = Marshmallow(app)
mail = Mail(app)

app.secret_key = "my-secret-key"
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
# Setting For JWT
jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
# Setting for CROS
CORS(app,supports_credentials=True)

ma = Marshmallow(app)

talisman = Talisman(app)

# app.config['MAIL_SERVER']='smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USERNAME'] = '046c0d3e002858'
# app.config['MAIL_PASSWORD'] = '4424339fab32f7'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = False

# SECRET_KEY = 'my_secret'
# MAIL_SERVER = 'localhost'
# MAIL_PORT = '8025'
# MAIL_USE_TLS = 1
# MAIL_USERNAME = ''
# app.config["MAIL_PASSWORD"] = ''

UPLOADS = os.path.basename('uploads')
UPLOADS = '/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:psotgres@localhost/flask'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flask.db'
# main sqlite database setting
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Main.db'

# multiple sqlite database setting
app.config['SQLALCHEMY_BINDS'] = {
    'super-admins': 'sqlite:///dbs/super-admins.db',
    'student': 'sqlite:///dbs/student.db',
}

app.config['UPLOADS'] = UPLOADS

db = SQLAlchemy(app)

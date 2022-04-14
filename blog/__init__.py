from flask import Flask

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_misaka import Misaka
from flask_sqlalchemy import SQLAlchemy
#from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer, SignatureExpired
from datetime import date, datetime

from config import Config

data_globale = datetime.now().strftime("%Y-%m-%d")
print (data_globale)

app = Flask(__name__)
app.config.from_object(Config)

# Riki - Aggiunto ma forse non necessario
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# fine

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'radifnews@gmail.com'
app.config['MAIL_PASSWORD'] = 'rdf6111166'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

Misaka(app)

app.config['MYSQL_HOST'] = '109.233.124.23'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'radif_dbuser'
app.config['MYSQL_PASSWORD'] = 'c1o09m2u9t'
app.config['MYSQL_DB'] = 'radif_db'
#mysql = MySQL(app)

dbPSQL = (
    "DRIVER={PostgreSQL Unicode};"
    "DATABASE=centro-diario;"
    "UID=postgres;"
    "PWD=super;"
    "SERVER=192.168.1.16;"
    "PORT=5432;"
    )

with app.app_context():
    #if db.engine.url.drivername == 'sqlite': # Riki riomosso sqlite
    if db.engine.url.drivername == '{PostgreSQL Unicode}':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

from blog import errors, models, routes

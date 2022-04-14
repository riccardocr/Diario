from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms.form import Form

from blog import db, login_manager #, mysql


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"User('{ self.id }', '{ self.username }', '{ self.email }')"

    def set_password_hash(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(250))
    description = db.Column(db.String(240))
    body = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(120))

    def __repr__(self):
        return f"Post('{ self.id }', '{ self.title }')"

class Diario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.Date)
    anno = db.Column(db.String(4))
    mese = db.Column(db.String(2))
    va_pensieri = db.Column(db.Integer, unique=False, default=0)
    va_parole = db.Column(db.Integer, unique=False, default=0)
    va_atti = db.Column(db.Integer, unique=False, default=0)
    s_ipocrisia = db.Column(db.Integer, unique=False, default=0)
    s_menzogne = db.Column(db.Integer, unique=False, default=0)
    s_guadagni_illeciti = db.Column(db.Integer, unique=0, default=0)
    c_pensieri = db.Column(db.Integer, unique=False, default=0)
    c_parole = db.Column(db.Integer, unique=False, default=0)
    c_atti = db.Column(db.Integer, unique=False, default=0)
    u_vanità_di_conoscenza = db.Column(db.Integer, unique=False, default=0)
    u_orgoglio_di_possesso = db.Column(db.Integer, unique=False, default=0)
    u_abuso_di_potere = db.Column(db.Integer, unique=False, default=0)
    d_cibi_errati = db.Column(db.Integer, unique=False, default=0)
    d_alcool = db.Column(db.Integer, unique=False, default=0)
    d_droghe = db.Column(db.Integer, unique=False, default=0)
    Totale = db.Column(db.Integer, unique=False, default=0)
    Luce_interiore = db.Column(db.Time, unique=False, default=0)
    Suono_interiore = db.Column(db.Time, unique=False, default=0)
    fisico_e_morale = db.Column(db.Integer, unique=False, default=0)
    finanziario = db.Column(db.Integer, unique=False, default=False)
    Esperienze_di_visione_interiore = db.Column(db.Text, unique=False)
    Esperienze_di_ascolto_interiore = db.Column(db.Text, unique=False)
    Grado_di_superamento_della_coscienza_fisica = db.Column(db.Text, unique=False)
    Difficoltà_nella_meditazione = db.Column(db.Text, unique=False)
    Settori_da_migliorare = db.Column(db.Text, unique=False)
    Salvato_SN = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return f"Diario('{ self.id }', '{ self.created_at }')"


from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, BooleanField, PasswordField, StringField, SubmitField, TextAreaField, IntegerField, DateField, DateTimeField, SelectField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo
from wtforms.fields.html5 import EmailField, DateField, TimeField
from datetime import date, datetime, time
from blog import data_globale

class LoginForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired("Campo Obbligatorio!")])
    password = PasswordField('Password', 
        validators=[DataRequired("Campo Obbligatorio!")])
    remember_me = BooleanField('Ricordami')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    register_user = EmailField('Email', 
        validators=[Email(message="Please enter a valid email address")])
    register_psw   = PasswordField('Password', 
        validators=[
            Length(min=7, max=20), 
            DataRequired("Campo Obbligatorio!"),
            EqualTo("register_psw_confirm", message="Le password non corrispondono")
            ])
    register_psw_confirm = PasswordField('Conferma Password', 
        validators=[
            Length(min=7, max=20), 
            DataRequired("Campo Obbligatorio!")])
    register_nopsw = BooleanField('Password dimenticata')
    register_submit = SubmitField('Registrati')

class PostForm(FlaskForm):
    title = StringField('Titolo', 
        validators=[DataRequired("Campo Obbligatorio!"), Length(min=3, max=120, message="Assicurati che il titolo abbia tra i 3 e i 120 caratteri.")])
    description = TextAreaField('Descrizione',
        validators=[Length(max=240, message="Assicurati che il campo descrizione non superi i 240 caratteri.")])
    body = TextAreaField('Contenuto', 
        validators=[DataRequired("Campo Obbligatorio!")])
    image = FileField('Copertina Articolo', 
        validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Pubblica Post')

class GDiarioForm(FlaskForm):
#Elenco
    elenco = SelectField('Elenco', default='PARTE_PASSIVA', \
        choices=[\
            ("PARTE_PASSIVA", "PARTE PASSIVA"),\
            ("NON_VIOLENZA_E_AMORE_PER_TUTTI", "NON VIOLENZA E AMORE PER TUTTI"),\
            ("va_pensieri", "- NON VIOLENZA E AMORE in Pensieri"),\
            ("va_parole", "- NON VIOLENZA E AMORE in Parole"),\
            ("va_atti", "- NON VIOLENZA E AMORE in Atti"),\
            ("SINCERITA", "SINCERITA'"),\
            ("s_ipocrisia", "- SINCERITA' Ipocrisia"),\
            ("s_menzogne", "- SINCERITA' Menzogne"),\
            ("s_guadagni_illeciti", "- SINCERITA' Guadagni illeciti"),\
            ("CASTITA", "CASTITA'"),\
            ("c_pensieri", "- CASTITA' in Pensieri"),\
            ("c_parole", "- CASTITA' in Parole"),\
            ("c_atti", "- CASTITA' in Atti"),\
            ("UMILTA", "UMILTA'"),\
            ("u_vanità_di_conoscenza", "- UMILTA' Vanità di conoscenza"),\
            ("u_orgoglio_di_possesso", "- UMILTA' Orgoglio di possesso"),\
            ("u_abuso_di_potere", "- UMILTA' Abuso di potere"),\
            ("DIETA", "DIETA"),\
            ("d_cibi_errati", "- DIETA Cibi errati"),\
            ("d_alcool", "- DIETA Alcool"),\
            ("d_droghe", "- DIETA Droghe"),\
            ("MEDITAZIONE", "MEDITAZIONE"),\
            ("Luce_interiore", "- Luce interiore"),\
            ("Suono_interiore", "- Suono interiore"),\
            ("SERVIZIO_PRESTATO", "SERVIZIO PRESTATO"),\
            ("fisico_e_morale", "- Fisico e morale"),\
            ("finanziario", "- Finanziario"),\
        ])
#Data
    GData = DateField('Data',
        format='%Y-%m-%d',
        default=datetime.strptime(data_globale, '%Y-%m-%d'),
        validators=[DataRequired("Scegli una data")])
    mese = SelectField('Mese', default=data_globale[5:7], choices=[('01', 'Gennaio'), ('02', 'Febbraio'), ('03', 'Marzo'), ('04', 'Aprile'), ('05', 'Maggio'), ('06', 'Giugno'), ('07', 'Luglio'), ('08', 'Agosto'), ('09', 'Settembre'), ('10', 'Ottobre'), ('11', 'Novembre'), ('12', 'Dicembre') ])
    mese1 = SelectField('Mese', default=data_globale[5:7], choices=[('01', 'Gennaio'), ('02', 'Febbraio'), ('03', 'Marzo'), ('04', 'Aprile'), ('05', 'Maggio'), ('06', 'Giugno'), ('07', 'Luglio'), ('08', 'Agosto'), ('09', 'Settembre'), ('10', 'Ottobre'), ('11', 'Novembre'), ('12', 'Dicembre') ])
    an = int(data_globale[0:4])
    choices=[]
    for x in range (0,40):
        choices.append((an-x,an-x))
    anno = SelectField('Anno', default=data_globale[:4], choices=choices)
    anno1 = SelectField('Anno', default=data_globale[:4], choices=choices)
#PARTE PASSIVA (indicare il numero di errori giornalierI)
    #NON VIOLENZA E AMORE PER TUTTI
    va_pensieri = IntegerField('in pensieri', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    va_parole = IntegerField('in parole', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    va_atti = IntegerField('in atti', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    #SINCERITA'
    s_ipocrisia = IntegerField('ipocrisia', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    s_menzogne = IntegerField('menzogne', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    s_guadagni_illeciti = IntegerField('guadagni illeciti', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    #CASTITA'
    c_pensieri = IntegerField('pensieri', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    c_parole = IntegerField('parole', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    c_atti = IntegerField('atti', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    #UMILTA'
    u_vanità_di_conoscenza = IntegerField('vanità di conoscenza', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    u_orgoglio_di_possesso = IntegerField('orgoglio di possesso', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    u_abuso_di_potere = IntegerField('abuso di potere', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    #DIETA
    d_cibi_errati = IntegerField('cibi errati', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    d_alcool = IntegerField('alcool', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    d_droghe = IntegerField('droghe', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])

    Totale_P_Giorno = IntegerField(default=0)
    Totale_P_Mese  = IntegerField(default=0)
    Totale_P_Anno  = IntegerField(default=0)
    
    Totale_P_Giorno1 = IntegerField(default=0)
    Totale_P_Mese1  = IntegerField(default=0)

#PARTE ATTIVA
    #MEDITAZIONE
    Luce_interiore = TimeField('Luce_interiore', format='%H:%M', default=time(0,0,0))
    Suono_interiore = TimeField('Suono_interiore', format='%H:%M', default=time(0,0,0))
    #IntegerField('Suono interiore', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    #MEDIA
    Totale_M_Giorno = IntegerField(default=0)
    Totale_M_Mese  = IntegerField(default=0)
    Totale_M_Anno  = IntegerField(default=0)
    #SERVIZIO PRESTATO
    fisico_e_morale = IntegerField('fisico e morale', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])
    finanziario = IntegerField('finanziario', default=0, validators=[NumberRange(min=0, max=90, message="I numeri devono essere compresi tra 0 e 90")])

    Totale_S_Giorno = IntegerField(default=0)
    Totale_S_Mese  = IntegerField(default=0)
    Totale_S_Anno  = IntegerField(default=0)
#ALTRO
    Esperienze_di_visione_interiore = TextAreaField('Esperienze di visione interiore')
    Esperienze_di_ascolto_interiore = TextAreaField('Esperienze di ascolto interiore')
    Grado_di_superamento_della_coscienza_fisica = TextAreaField('Grado di superamento della coscienza fisica')
    Difficoltà_nella_meditazione = TextAreaField('Difficoltà nella meditazione')
    Settori_da_migliorare = TextAreaField('Settori da migliorare')
    submit = SubmitField('Salva')
    back = SubmitField('X')
    Salvato_SN = IntegerField(default=0)

class Cerca(FlaskForm):
    trova = StringField('Filtra i dati', 
        validators=[DataRequired("Inserisci qualcosa")])
    submit = SubmitField('Cerca')


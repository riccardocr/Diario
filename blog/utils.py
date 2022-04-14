import os
import random
import re
import string
import unicodedata
from datetime import date

from flask import current_app
from PIL import Image
from flask.helpers import flash

from blog import app

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits
STRING_LENGTH = 6

def generate_random_string(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
    return "".join(random.choice(chars) for _ in range(length))

def slugify(value):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def title_slugifier(post_title):
    slug = slugify(post_title) + "-" + generate_random_string()
    return slug

def save_picture(form_data):
    filename = form_data.filename
    picture_name = generate_random_string() + "-" + filename
    picture_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, picture_name)

    image = Image.open(form_data)
    image.save(picture_path)

    return picture_name

def test(btn,ii):
    if btn=='-' : ii-=1
    elif btn=='+': ii+=1
    return ii

def totali(diario):

    tot = { 'PARTE_PASSIVA':0,\
                'NON_VIOLENZA_E_AMORE_PER_TUTTI':0, 'va_pensieri':0, 'va_parole':0, 'va_atti':0,\
                'SINCERITA':0, 's_ipocrisia':0, 's_menzogne':0, 's_guadagni_illeciti':0,\
                'CASTITA':0, 'c_pensieri':0, 'c_parole':0, 'c_atti':0,\
                'UMILTA':0, 'u_vanità_di_conoscenza':0, 'u_orgoglio_di_possesso':0, 'u_abuso_di_potere':0,\
                'DIETA':0, 'd_cibi_errati':0, 'd_alcool':0, 'd_droghe':0,\
                'MEDITAZIONE':'', 'Luce_interiore':0, 'Suono_interiore':0,\
                'MEDITAZIONE_h:m':'', 'Luce_interiore-media':0, 'Suono_interiore-media':0,\
                'SERVIZIO_PRESTATO':0,  'fisico_e_morale':0, 'finanziario':0,\
                'Esperienze_di_visione_interiore':'',\
                'Esperienze_di_ascolto_interiore':'',\
                'Grado_di_superamento_della_coscienza_fisica':'',\
                'Difficoltà_nella_meditazione':'',\
                'Settori_da_migliorare':''}

    for x in diario:
        tot['va_pensieri']            += + x.va_pensieri
        tot['va_parole']              += + x.va_parole
        tot['va_atti']                += + x.va_atti
        tot['s_ipocrisia']            += + x.s_ipocrisia
        tot['s_menzogne']             += + x.s_menzogne
        tot['s_guadagni_illeciti']    += + x.s_guadagni_illeciti
        tot['c_pensieri']             += + x.c_pensieri
        tot['c_parole']               += + x.c_parole
        tot['c_atti']                 += + x.c_atti
        tot['u_vanità_di_conoscenza'] += + x.u_vanità_di_conoscenza
        tot['u_orgoglio_di_possesso'] += + x.u_orgoglio_di_possesso
        tot['u_abuso_di_potere']      += + x.u_abuso_di_potere
        tot['d_cibi_errati']          += + x.d_cibi_errati
        tot['d_alcool']               += + x.d_alcool
        tot['d_droghe']               += + x.d_droghe
        #if x.created_at.year == anno and x.created_at.month == mese:
        tot['NON_VIOLENZA_E_AMORE_PER_TUTTI'] += + x.va_pensieri + x.va_parole + x.va_atti
        tot['SINCERITA'] += + x.s_ipocrisia + x.s_menzogne + x.s_guadagni_illeciti
        tot['CASTITA'] += + x.c_pensieri + x.c_parole + x.c_atti
        tot['UMILTA'] += + x.u_vanità_di_conoscenza + x.u_orgoglio_di_possesso + x.u_abuso_di_potere
        tot['DIETA'] += + x.d_cibi_errati + x.d_alcool + x.d_droghe


        h = int(x.Luce_interiore.hour)*60
        m = int(x.Luce_interiore.minute)
        tot['Luce_interiore'] += + h + m

        h = int(x.Suono_interiore.hour)*60
        m = int(x.Suono_interiore.minute)        
        tot['Suono_interiore'] += + h + m
     
        tot['fisico_e_morale'] += + x.fisico_e_morale
        tot['finanziario']     += + x.finanziario

        if x.Esperienze_di_visione_interiore:
            tot['Esperienze_di_visione_interiore'] = tot['Esperienze_di_visione_interiore'] + x.Esperienze_di_visione_interiore
        if x.Esperienze_di_ascolto_interiore:
            tot['Esperienze_di_ascolto_interiore'] = tot['Esperienze_di_ascolto_interiore'] + x.Esperienze_di_ascolto_interiore
        if x.Grado_di_superamento_della_coscienza_fisica:
            tot['Grado_di_superamento_della_coscienza_fisica'] = tot['Grado_di_superamento_della_coscienza_fisica'] + x.Grado_di_superamento_della_coscienza_fisica
        if x.Difficoltà_nella_meditazione:
            tot['Difficoltà_nella_meditazione'] = tot['Difficoltà_nella_meditazione'] + x.Difficoltà_nella_meditazione
        if x.Settori_da_migliorare:
            tot['Settori_da_migliorare'] = tot['Settori_da_migliorare'] + x.Settori_da_migliorare

    tot['PARTE_PASSIVA'] = tot['NON_VIOLENZA_E_AMORE_PER_TUTTI'] + tot['SINCERITA'] + tot['CASTITA'] + tot['UMILTA'] + tot['DIETA']

    MEDITAZIONE = tot['Luce_interiore'] + tot['Suono_interiore']
    h = int(MEDITAZIONE/60)
    m = int(MEDITAZIONE-h*60)
    tot['MEDITAZIONE'] = MEDITAZIONE #str(h).zfill(2)+":"+str(m).zfill(2)
    tot['MEDITAZIONE_h:m'] = str(h).zfill(2)+":"+str(m).zfill(2)

    tot['SERVIZIO_PRESTATO'] = tot['fisico_e_morale'] + tot['finanziario']
    #print('++++++++++++tot',tot)
    return tot 

def Converte_Min_in_Ore(Min):
    h = int(Min/60)
    m = int(Min-h*60)
    return str(h).zfill(2)+":"+str(m).zfill(2)

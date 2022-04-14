import re, os
from flask import abort, flash, redirect, render_template, request, url_for, Response, make_response
from flask_login import current_user, login_user, logout_user, login_required

from blog import app, db, dbPSQL, data_globale # mysql
from blog.forms import LoginForm, PostForm, Cerca, RegisterForm, GDiarioForm
from blog.models import Diario, Post, User
from blog.utils import save_picture, title_slugifier, test, totali, Converte_Min_in_Ore
#from blog import db_pyodbc
from datetime import datetime, date, timedelta
from calendar import monthrange
import time, locale
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle, PageBreak, Frame, Spacer
from reportlab.lib.pagesizes import A4, landscape

from reportlab.platypus.doctemplate import Indenter
from reportlab.platypus.tables import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

@app.route("/")
def homepage():
    page_number = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page_number, 6, True)

    if posts.has_next:
        next_page = url_for('homepage', page=posts.next_num)
    else:
        next_page = None

    if posts.has_prev:
        previous_page = url_for('homepage', page=posts.prev_num)
    else:
        previous_page = None 

    return render_template("homepage.html", posts=posts, current_page=page_number,
                           next_page=next_page, previous_page=previous_page)

@app.route("/posts/<string:post_slug>")
def post_detail(post_slug):
    post_instance = Post.query.filter_by(slug=post_slug).first_or_404()
    return render_template("post_detail.html", post=post_instance)

@app.route("/create-post", methods=["POST"])
@login_required
def post_create():
    form = PostForm()
    if form.validate_on_submit():
        slug = title_slugifier(form.title.data)
        new_post = Post(title=form.title.data, body=form.body.data, slug=slug,
                        description=form.description.data, author=current_user)

        if form.image.data:
            try:
                image = save_picture(form.image.data)
                new_post.image = image
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash("C'è stato un problema con l'upload dell'immagine. Cambia immagine e riprova.")    
                return redirect(url_for('post_update', post_id=new_post.id))

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post_detail', post_slug=slug))
    return render_template("post_editor.html", form=form)

@app.route("/create-gdiario", methods=["GET", "POST"])
@login_required
def gdiario_create():
    form = GDiarioForm()
    global data_globale
    GData=data_globale
    print ("******* GDiario_create ********", "data_globale= ", data_globale)
    diari = Diario.query.filter_by(user_id=current_user.id, created_at=GData).first()

    return render_template("gdiario_editor.html", form=form)


@app.route("/create-gupdate/<string:user_id>+<string:GData>", methods=["GET", "POST"])
@login_required
def gdiario_update(user_id, GData):
    print ("******************** Diario Update ***************")
    global data_globale
    form = GDiarioForm()
    user_id=user_id
    GData=GData
    data_globale = GData
    form.GData.data = datetime.strptime(GData, '%Y-%m-%d')
    print ("form.GData.data", form.GData.data, "data_globale", data_globale)

    if form.validate_on_submit():
        print ("Si form Validazione")
    else:
        print ("No form validazione")
    
    if form.back.data:
        print ("back")
        return redirect(url_for('g_homepage', update='True'))
        
    #if form.va_pensieri.data: 
    #    print ("ok", datetime.now())

    #print ("form.GData.data ", form.GData.data, type(form.GData.data))

    diari = Diario.query.filter_by(user_id=current_user.id, created_at=GData).first()

    if diari:
        #print ("diari")
        if form.submit.data:
            print("Salvo", diari.Salvato_SN )
            '''
            if form.va_pensieri_dw.data: 
                print("DATA_dw=", GData)
                todo = int(request.form.get("va_pensieri"))
                a=test('-', todo)
                diari.va_pensieri=a
                db.session.commit()
            '''
            diari.Salvato_SN = 1
            diari.anno = data_globale[:4]
            diari.mese = data_globale[5:7]
            diari.va_pensieri = form.va_pensieri.data
            diari.va_parole = form.va_parole.data
            diari.va_atti = form.va_atti.data
            diari.s_ipocrisia = form.s_ipocrisia.data
            diari.s_menzogne = form.s_menzogne.data
            diari.s_guadagni_illeciti = form.s_guadagni_illeciti.data
            diari.c_pensieri = form.c_pensieri.data
            diari.c_parole = form.c_parole.data
            diari.c_atti = form.c_atti.data
            diari.u_vanità_di_conoscenza = form.u_vanità_di_conoscenza.data
            diari.u_orgoglio_di_possesso = form.u_orgoglio_di_possesso.data
            diari.u_abuso_di_potere = form.u_abuso_di_potere.data
            diari.d_cibi_errati = form.d_cibi_errati.data
            diari.d_alcool = form.d_alcool.data
            diari.d_droghe = form.d_droghe.data
            #diari.Totale = form.Totale.data
            diari.Luce_interiore = form.Luce_interiore.data
            diari.Suono_interiore = form.Suono_interiore.data
            diari.fisico_e_morale = form.fisico_e_morale.data
            diari.finanziario = form.finanziario.data
            diari.Esperienze_di_visione_interiore = form.Esperienze_di_visione_interiore.data
            diari.Esperienze_di_ascolto_interiore = form.Esperienze_di_ascolto_interiore.data
            diari.Grado_di_superamento_della_coscienza_fisica = form.Grado_di_superamento_della_coscienza_fisica.data
            diari.Difficoltà_nella_meditazione = form.Difficoltà_nella_meditazione.data
            diari.Settori_da_migliorare = form.Settori_da_migliorare.data

            db.session.commit()
            return redirect(url_for('g_homepage', update='True'))

        form.va_pensieri.data = diari.va_pensieri
        form.va_parole.data = diari.va_parole
        form.va_atti.data = diari.va_atti 
        form.s_ipocrisia.data = diari.s_ipocrisia
        form.s_menzogne.data = diari.s_menzogne
        form.s_guadagni_illeciti.data = diari.s_guadagni_illeciti
        form.c_pensieri.data = diari.c_pensieri
        form.c_parole.data = diari.c_parole
        form.c_atti.data  = diari.c_atti
        form.u_vanità_di_conoscenza.data = diari.u_vanità_di_conoscenza
        form.u_orgoglio_di_possesso.data = diari.u_orgoglio_di_possesso
        form.u_abuso_di_potere.data = diari.u_abuso_di_potere
        form.d_cibi_errati.data = diari.d_cibi_errati
        form.d_alcool.data  = diari.d_alcool
        form.d_droghe.data  = diari.d_droghe
        
        form.Luce_interiore.data = diari.Luce_interiore
        form.Suono_interiore.data = diari.Suono_interiore
        form.fisico_e_morale.data = diari.fisico_e_morale
        form.finanziario.data = diari.finanziario
        form.Esperienze_di_visione_interiore.data = diari.Esperienze_di_visione_interiore
        form.Esperienze_di_ascolto_interiore.data = diari.Esperienze_di_ascolto_interiore
        form.Grado_di_superamento_della_coscienza_fisica.data = diari.Grado_di_superamento_della_coscienza_fisica
        form.Difficoltà_nella_meditazione.data = diari.Difficoltà_nella_meditazione
        form.Settori_da_migliorare.data = diari.Settori_da_migliorare

        va_tot = int(form.va_pensieri.data) + int(form.va_parole.data) + int(form.va_atti.data)
        s_tot = int(form.s_ipocrisia.data) + int(form.s_menzogne.data) + int(form.s_guadagni_illeciti.data)
        c_tot = int(form.c_pensieri.data) + int(form.c_parole.data) + int(form.c_atti.data)
        u_tot = int(form.u_vanità_di_conoscenza.data) + int(form.u_orgoglio_di_possesso.data) + int(form.u_abuso_di_potere.data)
        d_tot = int(form.d_cibi_errati.data) + int(form.d_alcool.data) + int(form.d_droghe.data)

        form.Totale_P_Giorno.data = va_tot + s_tot + c_tot + u_tot + d_tot

        t = Diario.query.filter(
            Diario.user_id    == current_user.id, 
            Diario.created_at == data_globale
            ).order_by(Diario.created_at).all()
        print (totali(t))
        form.Totale_P_Giorno.data = totali(t)['PARTE_PASSIVA']
        form.Totale_M_Giorno.data = str(int(totali(t)['MEDITAZIONE']/60)).zfill(2)+":"+str(totali(t)['MEDITAZIONE']-int(totali(t)['MEDITAZIONE']/60)*60).zfill(2)
        form.Totale_S_Giorno.data = totali(t)['SERVIZIO_PRESTATO']

        #print("+++ totali +++",type(totali(t)[0]), totali(t)[0]['va_pensieri'])
    else:
        new_gdiario = Diario(
            user_id = current_user.id,
            created_at = form.GData.data,
            va_pensieri = form.va_pensieri.data, 
            va_parole = form.va_parole.data,
            va_atti = form.va_atti.data,
            s_ipocrisia = form.s_ipocrisia.data,
            s_menzogne = form.s_menzogne.data,
            s_guadagni_illeciti = form.s_guadagni_illeciti.data,
            c_pensieri = form.c_pensieri.data,
            c_parole = form.c_parole.data,
            c_atti = form.c_atti.data,
            u_vanità_di_conoscenza = form.u_vanità_di_conoscenza.data,
            u_orgoglio_di_possesso = form.u_orgoglio_di_possesso.data,
            u_abuso_di_potere = form.u_abuso_di_potere.data,
            d_cibi_errati = form.d_cibi_errati.data,
            d_alcool = form.d_alcool.data,
            d_droghe = form.d_droghe.data,
            #Totale = form.Totale.data,
            Luce_interiore = form.Luce_interiore.data,
            Suono_interiore = form.Suono_interiore.data,
            fisico_e_morale = form.fisico_e_morale.data,
            finanziario = form.finanziario.data,
            Esperienze_di_visione_interiore = form.Esperienze_di_visione_interiore.data,
            Esperienze_di_ascolto_interiore = form.Esperienze_di_ascolto_interiore.data,
            Grado_di_superamento_della_coscienza_fisica = form.Grado_di_superamento_della_coscienza_fisica.data,
            Difficoltà_nella_meditazione = form.Difficoltà_nella_meditazione.data,
            Settori_da_migliorare = form.Settori_da_migliorare.data)

        db.session.add(new_gdiario)
        db.session.commit()

    print("///// data_globale", type(data_globale), data_globale[:7])
    t = Diario.query.filter(
        Diario.user_id    == current_user.id, 
        Diario.anno == data_globale[:4],
        Diario.mese == data_globale[5:7]
        ).order_by(Diario.created_at).all()
    
    form.Totale_P_Mese.data = totali(t)['PARTE_PASSIVA']
    
    print(data_globale)
    if str(datetime.now().month).zfill(2) == data_globale[5:7]:
        giorni_range = datetime.now().day
    else:
        giorni_range = monthrange(int(data_globale[:4]), int(data_globale[5:7]))[1]
    #print ("giorni_range", giorni_range,)
    media = int(totali(t)['MEDITAZIONE']/int(giorni_range))

    form.Totale_M_Mese.data = str(int(media/60)).zfill(2)+":"+str(media-int(media/60)*60).zfill(2)
    
    form.Totale_S_Mese.data = totali(t)['SERVIZIO_PRESTATO']
       

        #return redirect(url_for('gdiario_update', form=form))

    #print ("data_globale ", data_globale, type(data_globale))
    return render_template("gdiario_editor.html", form=form)

@app.route("/posts/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def post_update(post_id):
    post_instance = Post.query.get_or_404(post_id)
    if post_instance.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post_instance.title = form.title.data
        post_instance.description = form.description.data
        post_instance.body = form.body.data

        if form.image.data:
            try:
                image = save_picture(form.image.data)
                post_instance.image = image
            except Exception:
                db.session.commit()
                flash("C'è stato un problema con l'upload dell'immagine. Cambia immagine e riprova.")    
                return redirect(url_for('post_update', post_id=post_instance.id))

        db.session.commit()
        return redirect(url_for('post_detail', post_slug=post_instance.slug))
    elif request.method == "GET":
        form.title.data = post_instance.title
        form.description.data = post_instance.description
        form.body.data = post_instance.body
    
    post_image = post_instance.image or None
    return render_template("post_editor.html", form=form, post_image=post_image)

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
@login_required
def post_delete(post_id):
    post_instance = Post.query.get_or_404(post_id)
    if post_instance.author != current_user:
        abort(403)
    db.session.delete(post_instance)
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route("/about")
def about():
    return render_template("about_page.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    '''
    trova = Cerca()
    posts = Post.query.filter(Post.title.contains(str(trova.trova.data))).order_by(Post.title)
    cur = mysql.connection.cursor()
    cur.execute("select name from clerk where name like'%"+str(trova.trova.data)+"%'")
    sel = cur.fetchall()

    Sql1 = "select descrizion from anamaga where descrizion like '%"+str(trova.trova.data)+"%'"
    Rows=''
    Qry=1
    '''
    #psql = db_pyodbc.fnODBC(Sql1, Rows, dbPSQL, Qry)
    #flash(psql)
    #if request.method == "POST":
        #details = request.form
        #firstName = details['fname']
        #lastName = details['lname']
        #cur = mysql.connection.cursor()
        #cur.execute("select * from list;")
        #mysql.connection.commit()
        #cur.close()
    #return render_template("contact_page.html", trova=trova, posts=posts, sel=sel, psql=psql)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('username e password non combaciano!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('g_homepage', update='False'))

    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.register_user.data).first()
        if user:
            flash('utente già esistente')
            return render_template('register.html', form = form)
        new_user = User(
            username = form.register_user.data, 
            email = form.register_user.data, 
            password = User.set_password_hash(form.register_psw.data), 
            created_at = datetime.now())
            #password = hashed_password )

        # saving user object into data base with hashed password
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered', 'success')
        # if registration successful, then redirecting to login Api
        return redirect(url_for('login'))
    else:
        # se il metodo è GET, quindi esegui il rendering del modulo di registrazione
        return render_template('register.html', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route("/g_homepage/<string:update>", methods=["GET", "POST"])
@login_required
def g_homepage(update):
    locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
    update = update
    global data_globale
    form = GDiarioForm()

    if form.validate_on_submit():
        Stampa()

    if update == 'True':
        form.GData.data = datetime.strptime(data_globale, '%Y-%m-%d')
        form.mese.data = data_globale[5:7]
        form.anno.data = data_globale[0:4]
    else:
        if form.anno.data and form.mese.data:
            data_globale = form.anno.data + '-' + form.mese.data + '-01'
            form.GData.data = datetime.strptime(data_globale, '%Y-%m-%d')

    Dt = {"id":[], "user_id":[], "data":[], "giorno":[], "btn_on":[]}
    try:
        diario = Diario.query.filter(
            Diario.user_id == current_user.id, 
            Diario.anno == data_globale[:4], 
            Diario.mese == data_globale[5:7]
            ).order_by(Diario.created_at).all()
        my_date = date(form.GData.data.year, form.GData.data.month, 1)

        for d in range(0 , 31):
            data2 = my_date + timedelta(days=d)
            if my_date.month == data2.month:   
                diario_giorno = Diario.query.filter_by(user_id = current_user.id, created_at = data2 ).first()
                Dt["id"].append(d+1)
                Dt["user_id"].append(current_user.id)
                Dt["data"].append(data2)
                Dt["giorno"].append(data2.strftime("%a"))

                if diario_giorno and diario_giorno.Salvato_SN==1:
                    Dt["btn_on"].append(1)
                else: 
                    Dt["btn_on"].append(0)
            else:
                break
        #return redirect(url_for('g_homepage', post_id=post_instance.id))
    except BaseException as e:
        print ("errore: ", str(e))
        data2 = 0

    return render_template("ghomepage.html", form=form, diario=diario, Dt=Dt)

@app.route("/storico", methods=["GET", "POST"])
@login_required
def storico():
    locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

    global data_globale
    form = GDiarioForm()

    #value = dict(form.elenco.choices).get(form.elenco.data)
    elenco = request.form.get('elenco')
    if elenco == None: elenco = "PARTE_PASSIVA"

    t = Diario.query.filter(
        Diario.user_id    == current_user.id, 
        Diario.anno == form.anno.data,
        Diario.mese == form.mese.data
        ).order_by(Diario.created_at).all()
    print ('-- form.elenco --',(elenco)) #print('-- form.elenco --',form.elenco.choices[0][0]) #print (request.form.elenco.get('mese'))
    try:
        form.Totale_P_Mese.data = totali(t)[elenco]
    except Exception:
        form.Totale_P_Mese.data=''

    t = Diario.query.filter(
        Diario.user_id    == current_user.id, 
        Diario.anno == form.anno1.data,
        Diario.mese == form.mese1.data
        ).order_by(Diario.created_at).all()
    print ('-- form.elenco --',type(request.form.get('elenco'))) #print('-- form.elenco --',form.elenco.choices[0][0]) #print (request.form.elenco.get('mese'))
    try:
        form.Totale_P_Mese1.data =  totali(t)[elenco]
    except Exception:
        form.Totale_P_Mese1.data=''

    mese=[]
    for m in range (1,13):
        t = Diario.query.filter(
        Diario.user_id    == current_user.id, 
        Diario.anno == form.anno.data,
        Diario.mese == str(m).zfill(2)
        ).order_by(Diario.created_at).all()

        try:
            mese.append(totali(t)[elenco])
        except Exception:
            mese=[]

    mese1=[]
    for m in range (1,13):
        t = Diario.query.filter(
        Diario.user_id    == current_user.id, 
        Diario.anno == form.anno1.data,
        Diario.mese == str(m).zfill(2)
        ).order_by(Diario.created_at).all()

        try:
            mese1.append(totali(t)[elenco])
        except Exception:
            mese1=[]

    giorno=[]
    Ascisse=[]
    my_date = form.anno.data+'-'+ form.mese.data+'-'
    giorni_range = monthrange(int(form.anno.data), int(form.mese.data))
    for d in range (giorni_range[0],giorni_range[1]+1):
        Ascisse.append(d)
        data2 = my_date + str(d).zfill(2)
        t = Diario.query.filter(
        Diario.user_id    == current_user.id, 
        Diario.created_at == data2,
        ).order_by(Diario.created_at).all()
        print(data2,t)
        try:
            giorno.append(totali(t)[elenco])
        except Exception:
            giorno=[]

    giorno1=[]
    my_date = form.anno1.data+'-'+ form.mese1.data+'-'
    giorni_range = monthrange(int(form.anno.data), int(form.mese.data))
    for d in range (giorni_range[0],giorni_range[1]+1):
        data2 = my_date + str(d).zfill(2)
        t = Diario.query.filter(
        Diario.user_id    == current_user.id, 
        Diario.created_at == data2,
        ).order_by(Diario.created_at).all()
        print(data2,t)
        try:
            giorno1.append(totali(t)[elenco])
        except Exception:
            giorno1=[]

    #print ("mese",mese,type(mese),"mese1",mese1,type(mese1))
    print ("giorno",giorno,type(giorno))

    return render_template("storico.html", form=form, mese=mese, mese1=mese1, giorno=giorno,  giorno1=giorno1, Ascisse=Ascisse)

def Stampa():
    '''
    # --------- I report ------
    fileName="test.pdf"
    documentTitle = "Titolo"
    image ="blog\static\img\min_m.png"
    title = "Diario"
    subTitle ="Nome Cognome"
    textLines = ["Testo corpo ....", "wwww","rrrr","tttt "]

    pdf = canvas.Canvas(fileName)
    
    pdf.drawInlineImage(image, 50, 730)

    pdf.setTitle(documentTitle)
    pdf.setFillColorRGB(0, 0, 255)
    pdf.setFont("Courier-Bold", 24)
    pdf.drawString(270, 770, title)

    pdf.line(30, 710, 550, 710)

    text= pdf.beginText(40,680)
    text.setFont("Courier", 18)
    text.setFillColor(colors.red)
    for line in textLines:
        text.textLine(line)
    
    pdf.drawText(text)
    pdf.save()
    '''
    # --------- II report ------
    form = GDiarioForm()

    def FiltroSql(user, anno, mese, giorno):
        if giorno=='00':
            diario = Diario.query.filter(
            Diario.user_id    == current_user.id, 
            Diario.anno == anno,
            Diario.mese == mese
            ).order_by(Diario.created_at).all()
        else:
            #Dt=anno+"-"+mese+"-"+giorno
            Dt=datetime.strptime(anno+"-"+mese+"-"+giorno, '%Y-%m-%d').date()
            #print("Dt.............................",Dt)
            diario = Diario.query.filter(
            Diario.user_id    == current_user.id, 
            Diario.created_at == Dt
            ).order_by(Diario.created_at).all()
        return diario

    Story = []
    elenco1 =[\
            ("va_pensieri"),\
            ("va_parole"),\
            ("va_atti"),\
            ("s_ipocrisia"),\
            ("s_menzogne"),\
            ("s_guadagni_illeciti"),\
            ("c_pensieri"),\
            ("c_parole"),\
            ("c_atti"),\
            ("u_vanità_di_conoscenza"),\
            ("u_orgoglio_di_possesso"),\
            ("u_abuso_di_potere"),\
            ("d_cibi_errati"),\
            ("d_alcool"),\
            ("d_droghe")]
    elenco2 =[\
            ("Luce_interiore"),\
            ("Suono_interiore")]
    elenco3 =[\
            ("fisico_e_morale"),\
            ("finanziario")]

    styles = getSampleStyleSheet()

    styleT = styles["Heading3"]
    styleT.fontName = "Helvetica"
    styleT.textColor = "blue"
    styleT.align = "center"

    doc = SimpleDocTemplate("phello.pdf", pagesize=landscape(A4), 
        leftMargin=0.2*cm, rightMargin=0.2*cm, topMargin=0.2*cm, bottomMargin=0.2*cm)
    
    #Titolo=[Paragraph('Diario',styleT)]
    DimCol = [0.7*cm]
    DimRow = [0.5*cm]
    TabellaTit=TableStyle([('GRID',(0,0),(-1,-1),0.25,"grey"),
                    ('BACKGROUND',(0,0),(16,0), colors.green),
                    ('BACKGROUND',(17,0),(-1,0), colors.navy),
                    ('TEXTCOLOR',(0,0),(-1,0), colors.white),
                    ('FONTNAME',(0,0),(-1,0), 'Helvetica-Bold'),
                    ('BACKGROUND',(0,0),(0,-1), colors.lightgrey),
                    ('SPAN',(1,0),(16,0)),
                    ('SPAN',(17,0),(21,0)),
                    ('FONTSIZE',(1,0),(-1,0),12),
                    ('SPAN',(1,1),(3,1)),
                    ('BACKGROUND',(1,1),(3,2),'#F3F3F3'),
                    ('FONTSIZE',(1,1),(3,1),7),
                    ('FONT',(17,1),(18,1),'Helvetica', 8),
                    ('FONT',(20,1),(21,1),'Helvetica', 8),
                    ('SPAN',(4,1),(6,1)),
                    ('BACKGROUND',(4,1),(6,2),'#D9D9D9'),
                    ('SPAN',(7,1),(9,1)),
                    ('BACKGROUND',(7,1),(9,2),'#F3F3F3'),
                    ('SPAN',(10,1),(12,1)),
                    ('BACKGROUND',(10,1),(12,2),'#D9D9D9'),
                    ('SPAN',(13,1),(15,1)),
                    ('BACKGROUND',(13,1),(15,2),'#F3F3F3'),
                    ('SPAN',(17,1),(18,1)),
                    ('BACKGROUND',(17,1),(18,2),colors.yellow),
                    ('SPAN',(20,1),(21,1)),
                    ('BACKGROUND',(20,1),(21,2),'#B4A7D6'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                	('VALIGN',(0,0),(-1,-1),'TOP'),
                    ('FONT', (0,1), (-1,-1), 'Helvetica'),
                    ('BACKGROUND',(16,1),(16,-1), colors.lightgrey),
                    ('BACKGROUND',(19,1),(19,-1), colors.lightgrey),
                    ('FONT', (1,2), (-1,2), 'Helvetica', 7),
                    ('GRID', (19,1),(19,1),1,"grey")
                    ])
    Tabella=([('GRID',(0,0),(-1,-1),0.25,"grey"),
                    ('BACKGROUND',(0,0),(0,-1), colors.lightgrey),
                    ('BACKGROUND',(16,0),(16,-1), colors.lightgrey),
                    ('BACKGROUND',(19,0),(19,-1), colors.lightgrey),
                    ('ALIGN',(0,0),(-1,-1), 'RIGHT'),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('FONT', (0,0), (-1,-1), 'Helvetica'),
                    ('FONTSIZE', (1,0), (-1,-1), 8)
                    ])
    TabellaPiede=TableStyle([('GRID',(0,0),(-1,-1),0.25,"grey"),
                    ('BACKGROUND',(0,0),(0,-1), colors.lightgrey),
                    ('BACKGROUND',(1,0),(-1,0), colors.lightgrey),
                    ('ALIGN',(1,0),(-1,0), 'RIGHT'),
                    ('SPAN',(0,1),(0,3)),           
                    ('SPAN',(1,1),(4,1)),
                    ('SPAN',(5,1),(8,1)),
                    ('SPAN',(9,1),(13,1)),
                    ('SPAN',(14,1),(17,1)),
                    ('SPAN',(18,1),(21,1)),
                    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                	('VALIGN',(0,0),(-1,-1),'TOP'),
                    ('FONT', (0,0), (-1,-1), 'Helvetica'),
                    ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,0), 8),
                    ('FONTSIZE', (9,1), (10,1), 9),
                    ('SPAN',(1,2),(4,3)),
                    ('SPAN',(5,2),(8,3)),
                    ('SPAN',(9,2),(13,3)),
                    ('SPAN',(14,2),(17,3)),
                    ('SPAN',(18,2),(21,3)),
                    ('BACKGROUND',(1,2),(21,3), '#FFF2CC'),
                    ('GRID', (19,0),(19,0),1,"grey")
                    ])
    dataTit=[]
    data=[]
    dataPiede=[]
    dataTit.append(['Diario','PARTE PASSIVA',  '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'PARTE ATTIVA' '', '', '', ''])
    dataTit.append([form.anno.data,'NON VIOLENZA E\nAMORE PER TUTTI', '', '', 'SINCERITA', '', '', 'CASTITA', '', '', 'UMILTA', '', '', 'DIETA', '', '', 'Totale', 'MEDITAZIONE', '', 'MEDIA', 'SERVIZIO\nPRESTATO', ''])
    dataTit.append([str(dict(form.mese.choices).get(form.mese.data))[:3],'in\nPensieri', 'in\nParole', 'in\nAtti', 'Ipocrisia', 'Menzogne', 'Guadagni\nIlleciti', 'in\nPensieri', 'in\nParole', 'in\nAtti', 'Vanità di\nConoscenza', 'Orgoglio di\nPossesso', 'Abuso di\nPotere', 'Cibi\nErrati', 'Alcool', 'Droghe', 'n.', 'Luce\nInteriore', 'Suono\nInteriore', 'ORE', 'Fisico e\nMorale', 'Finanziario'])

    t=[]
    style=Tabella
    Ultimo_giorno = monthrange(int(form.anno.data), int(form.mese.data))[1]+1
    print("Ultimo_giorno",Ultimo_giorno)
    for g in range (1, Ultimo_giorno):
        data1=[g]
        diario=FiltroSql(current_user.id, form.anno.data, form.mese.data, str(g).zfill(2))
        if diario != []:
            for s in elenco1:
                data1.append(totali(diario)[s])
            data1.append(totali(diario)['PARTE_PASSIVA'])
            for s in elenco2:
                data1.append(Converte_Min_in_Ore(totali(diario)[s]))
            data1.append(totali(diario)['MEDITAZIONE_h:m'])
            for s in elenco3:
                data1.append(totali(diario)[s])
        else:
            data1=([g,'', '', '', '','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        for x in range(len(data1)): 
            if data1[x]==0 :
                data1[x]=''
        data.append(data1)
        print(g,")",data1)

        if g % 2 == 0: bg_color = colors.whitesmoke
        else: bg_color = colors.lightgrey
        Tabella.insert(1,('BACKGROUND', (0, g), (-1, g), bg_color))

    diario=FiltroSql(current_user.id, form.anno.data, form.mese.data,'00')

    data1=['Totale']
    for s in elenco1:
        data1.append(totali(diario)[s])
    data1.append(totali(diario)['PARTE_PASSIVA'])
    for s in elenco2:
        data1.append(Converte_Min_in_Ore(totali(diario)[s]))
    #--- Media
    print (datetime.now().year,datetime.now().month,int(form.anno.data),int(form.mese.data),datetime.now().day)
    if datetime.now().year==int(form.anno.data) and int(form.mese.data)==datetime.now().month:
        gg = datetime.now().day
    else: 
        gg = Ultimo_giorno
    MEDITAZIONE = totali(diario)['MEDITAZIONE']/gg
    h = int(MEDITAZIONE/60)
    m = int(MEDITAZIONE-h*60)
    Media = str(h).zfill(2)+":"+str(m).zfill(2)
    data1.append(Media)

    for s in elenco3:
        data1.append(totali(diario)[s])
    dataPiede.append(data1)
    dataPiede.append(['','Esperienze di visione interiore', '', '', '','Esperienze di ascolto interiore', '', '', '', 'Grado di superamento della coscienza fisica', '', '', '', '', 'Difficoltà nella meditazione', '', '', '', 'Settori da migliorare', '', '', ''])
    dataPiede.append([ '', Paragraph(totali(diario)['Esperienze_di_visione_interiore'][:110]), '', '', '',Paragraph(totali(diario)['Esperienze_di_ascolto_interiore'][:110]), '', '', '', Paragraph(totali(diario)['Grado_di_superamento_della_coscienza_fisica'][:110]), '', '', '', '', Paragraph(totali(diario)['Difficoltà_nella_meditazione'][:110]), '', '', '', Paragraph(totali(diario)['Settori_da_migliorare'][:110]), '', '', ''])
    dataPiede.append(['','', '', '', '','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

    Story=[Table(dataTit, colWidths=1.3*cm, rowHeights=[0.7*cm,0.9*cm,0.8*cm], style=TabellaTit), 
        Table(data, colWidths=1.3*cm, rowHeights=0.47*cm, style=TableStyle(Tabella)), 
        Table(dataPiede, colWidths=1.3*cm, rowHeights=[0.5*cm,0.7*cm,1*cm,1*cm], style=TabellaPiede)]

    doc.build(Story)
    os.startfile('phello.pdf')
    return 'ok'

    

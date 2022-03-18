from email import message
from click import style
from flask import Flask, redirect,render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flaskweb'
db = SQLAlchemy(app)

class contacts(db.Model):
    '''
    sno, name,  email, msg, date email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Message = db.Column(db.String(700), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    read_status=db.Column(db.Integer, nullable=False)

@app.route("/")
def hello():
    return render_template('index.html') #as shown in the code below

@app.route("/home")
def home():
    return render_template('index.html')#Homepage

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('msg')
        if ((name=="" or email=="" or message=="") or ("@" not in email)):
            error="Field Can't be empty and email address must be valid"
            error_flag=1
            return render_template('contact.html', error=error,error_flag=error_flag)
        entry = contacts(Name=name, Message = message, date= datetime.now(),Email = email, read_status=0 )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')

@app.route("/about")
def about():
    name_var="Abhishek"
    return render_template('about.html', name=name_var)#About Us

# @app.route("/inbox", methods = ['GET', 'POST'])
# def inbox():
#     messages=contacts.query.filter_by().all()[::-1][0:15]
#     return render_template('inbox.html', messages=messages)
# app.run(debug=True)

@app.route("/inbox/<string:page_no>/", methods = ['GET', 'POST'])
def inbox(page_no):
    page_in_int=int(page_no)
    k=15*(page_in_int)
    last_page=(len(contacts.query.filter_by().all())-1)//15
    messages=contacts.query.filter_by().all()[::-1][k:k+15]
    return render_template('inbox.html', messages=messages, page_no=page_in_int, last_page=last_page)

@app.route("/open_message/<string:sno>/", methods = ['GET', 'POST'])
def open_message(sno):
    messages=contacts.query.filter_by(sno=sno).first()
    messages.read_status=1
    db.session.commit()
    return render_template('open_message.html', messages=messages)

@app.route("/delete/<string:sno>/", methods = ['GET', 'POST'])
def delete(sno):
    messages=contacts.query.filter_by(sno=sno).first()
    db.session.delete(messages)
    db.session.commit()
    return redirect("/inbox/0")

app.run(debug=True)

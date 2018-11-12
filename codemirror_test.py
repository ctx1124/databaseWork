from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms import TextAreaField
from wtforms.fields import SubmitField
from flask_codemirror import CodeMirror
from flask import Flask,render_template
from flask import request,redirect, url_for,flash
import pymysql
from flask import current_app,g
import traceback
import sys
from flask_bootstrap import Bootstrap
from datetime import datetime

SECRET_KEY = 'secret!'
# mandatory
CODEMIRROR_LANGUAGES = ['sql']
# optional
CODEMIRROR_THEME = '3024-night'
CODEMIRROR_ADDONS = (
     ('hint','sql-hint'),
)
CODEMIRROR_VERSION='5.40.2'

app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)
bootstrap = Bootstrap()
bootstrap.init_app(app)

class MyForm(FlaskForm):
    source_code = CodeMirrorField(language='sql',
                                config={'lineNumbers' : 'true'})
    submit = SubmitField('执行')

@app.route('/',methods={'GET','POST'})
def index():
    return render_template('index.html')

@app.route('/data', methods = ['GET', 'POST'])
def data():
    form = MyForm()
    name = {}
    data = {}
    error = current_app.error
    if request.method=='POST':
        text = form.source_code.data
        form.source_code.data=""
        print(text)
        db = current_app.db
        try:
            cursor = db.cursor()
            cursor.execute(text)
            db.commit()
            #print(cursor.execute(text))
            data = cursor.fetchall()
            if(cursor.description):
                name=cursor.description
            #flash("database connect sucess")
            #print(cursor.messages)
            #print(data)
            now = datetime.now()
            error=error+str(now)+"\n"+text+"\n命令成功执行"+"\n"
            current_app.error=error
            return render_template('connect.html', form=form,name=name,data=data,error=error)
        except:
            db.rollback()
            now = datetime.now()
            error= error+str(now)+"\n"+text+"\n"+traceback.format_exc()+"\n"
            print(error)
            #traceback.print_exc()
            return render_template('connect.html', form=form,name=name,data=data,error=error)

    return render_template('connect.html', form=form,name=name,data=data,error=error)

@app.route('/connect', methods = ['POST', 'GET'])
def connect():
    connect_err=""
    localhost = request.args.get('localhost')
    user = request.args.get('user') 
    password = request.args.get('password') 
    database = request.args.get('database')
    if localhost !=None and user != None and password !=None and database != None:
        print(localhost)
        try:
            db = pymysql.connect(localhost,user,password,database)
            print('success')
            
        except:
            connect_err=traceback.format_exc()
            #connect_err=sys.exc_info()
            flash(connect_err)
            #return redirect(url_for('data'))
            return render_template('login.html',connect_err=connect_err)
        flash('database connected')
        current_app.db = db
        current_app.error="connected success\n"
        return redirect(url_for('data'))
        
    return render_template('login.html',connect_err=connect_err)    


if __name__=="__main__":
    app.run(host="127.0.0.1")
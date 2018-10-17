from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField
from flask_codemirror import CodeMirror
from flask import Flask,render_template
from flask import request,redirect, url_for,flash
import pymysql
from flask import current_app

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

class MyForm(FlaskForm):
    source_code = CodeMirrorField(language='sql',
                                config={'lineNumbers' : 'true'})
    submit = SubmitField('Submit')

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = MyForm()
    ''''db = current_app.db
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")

    data = cursor.fetchall()
    flash("database connect sucess")
    print(data)'''
    if request.method=='POST':
        text = form.source_code.data
        print(text)
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)

@app.route('/connect', methods = ['POST', 'GET'])
def connect():
    localhost = request.args.get('localhost')
    user = request.args.get('user') 
    password = request.args.get('password') 
    database = request.args.get('database')
    if localhost !=None and user != None and password !=None and database != None:
        print(localhost)
        db = pymysql.connect(localhost,user,password,database)
        current_app.db = db
        flash('database connected')
        return redirect(url_for('index'))
        
    return render_template('login.html')    


if __name__=="__main__":
    app.run(host="127.0.0.1")
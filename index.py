from flask import Flask, render_template,redirect,request,flash
from flask_wtf import FlaskForm
from flask_mysqldb import MySQL,MySQLdb
# pip install flask-mysql
from Config import MySqlDBConnection, token_required
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import urllib.request
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AppaBaba#2050'
app.config['MYSQL_DB'] = 'EmployerDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
# mysql = MySqlDBConnection(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'Super'
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = 'static/files'

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','doc','gif','txt','odt'])

# class UploadFileFrom(Flask):
#     file = FileField("File", validators=[InputRequired()])
#     SubmitField = SubmitField("Upload File")

# @app.route('/', methods=['GET', 'POST'])
# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     form = UploadFileFrom()
#     if form.validate_on_submit():
#         file = form.file.data
#         file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
#         return "File Has Been Upladed"
#     return render_template("index.html", form=form)

def allowed_file(filename):
    return '.' in filename and filename.rsplite('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/upload", methods=["POST","GET"])
def upload():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        now = datetime.now()
        if request.method == 'POST':
            files = request.files.getlist('files[]')
            print(files)
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    print(filename,'@@@@@@@@@@@@@@@@@')
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                    # cur.execute("INSERT INTO images (file_name, upload_on) VALUES [filename ,now]")
                    cur.execute("INSERT INTO images (file_name,upload_on) VALUES ('"+filename+"','"+now+"')")
                    mysql.connection.commit()
                print('file')
            cur.close()    
            flash('File(s) success uploaded')
        return redirect('/')    


if __name__ == "__main__":
    app.run(debug=True, port=8777)

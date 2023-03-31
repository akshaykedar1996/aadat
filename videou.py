from flask import Flask, request, render_template, json, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from Config import MySqlDBConnection, token_required
import Config
from wtforms import FileField, SubmitField
import os
from datetime import datetime
import urllib.request
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AppaBaba#2050'
app.config['MYSQL_DB'] = 'EmployerDB'

mysql = MySQL(app)
mysql = MySqlDBConnection(app)
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['SECRET_KEY'] = 'Super'
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = 'static/video'


@app.route('/index')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM example")
    data = cur.fetchall()
  #   return str(data)
  #   cur.close()
    return render_template('show.html')


@app.route('/')
def upload():
    return render_template('home.html')




@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
    try:
        # check if the post request has the file part
        if request.method == 'POST':
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO example (file) VALUES (%s)", (filename,))
            mysql.connection.commit()
            cursor.close()
            return 'video_file Uploaded successfully'
            # return   jsonify({"message": "file Uploaded successfully.", "status": "success"})
    except Exception as e:

        return 'file Uploaded failed'



if __name__ == "__main__":
    app.run(debug=True, port=7777)
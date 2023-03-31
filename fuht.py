from flask import Flask, request, render_template, Blueprint, redirect, flash, url_for
from flask_mysqldb import MySQL
from Config import MySqlDBConnection, token_required
# import Config

upload = Blueprint("upload", __name__)
app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'AppaBaba#2050'
# app.config['MYSQL_DB'] = 'EmployerDB'
mysql = MySQL(app)
mysql = MySqlDBConnection(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@upload.route('/')
def index():
      cur = mysql.connection.cursor()
      cur.execute("SELECT * FROM Upload")
      data = cur.fetchall()
      cur.close()

      return render_template('index.html',Upload= data)


@upload.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        # file_data = file.read()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Upload (file) VALUES ('"+(file)+"')")
        mysql.connection.commit()
        # cur.close()
        return redirect(url_for('index'))
    return redirect(url_for('index'))
    

if __name__ == "__main__":
    app.run(debug=True , port=8999)

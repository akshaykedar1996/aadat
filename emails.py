from flask import Flask, request, render_template
from flask_mail import Mail, Message
from random import randint
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from Config import MySqlDBConnection

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AppaBaba#2050'
app.config['MYSQL_DB'] = 'FaskToken'
app.config['UPLOAD_FOLDER'] = 'static/file'

mysql = MySQL(app)
mysql = MySqlDBConnection(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'akshaykedar1996@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ak@7030140328'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/')
def index():
    return render_template('email_form.html')

@app.route('/verify', methods=['POST'])
def verify():
    email = request.form['email']
    otp = randint(100000, 999999)
    msg = Message(subject='OTP', sender='your-email@gmail.com', recipients=[email])
    msg.body = f'Your OTP is {otp}.'
    mail.send(msg)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO otp(email, otp) VALUES(%s, %s)", (email, otp))
    mysql.connection.commit()
    cur.close()
    return render_template('otp_form.html', email=email)

@app.route('/validate', methods=['POST'])
def validate():
    email = request.form['email']
    user_otp = request.form['otp']
    cur = mysql.connection.cursor()
    cur.execute("SELECT otp FROM otp WHERE email = %s", [email])
    data = cur.fetchone()
    if data is not None:
        otp = data[0]
        if str(otp) == user_otp:
            cur.execute("DELETE FROM otp WHERE email = %s", [email])
            mysql.connection.commit()
            cur.close()
            return render_template('success.html')
    cur.close()
    return render_template('failure.html')

if __name__ == '__main__':
    app.run(debug=True, port=6666)

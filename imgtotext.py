# Create a Flask app and define a route to upload the image:
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from PIL import Image
import pytesseract

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AppaBaba#2050'
app.config['MYSQL_DB'] = 'FaskToken'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image = request.files['image']
        image.save(image.filename)
        text = pytesseract.image_to_string(Image.open(image.filename))
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO images (image, text) VALUES (%s, %s)', (image.read(), text))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('display'))
    return render_template('upload.html')


# Create a route to display the uploaded image and its corresponding text:
@app.route('/display')
def display():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM images ORDER BY id DESC LIMIT 1')
    data = cursor.fetchone()
    cursor.close()
    return render_template('display.html', image=data[1], text=data[2])


if __name__ == '__main__':
    app.run(debug = True ,port=8888)
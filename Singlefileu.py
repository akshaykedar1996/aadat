from flask import Flask, request,render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AppaBaba#2050'
app.config['MYSQL_DB'] = 'file_upload_db'
mysql = MySQL(app)


mysql = MySQL(app)
 
# @app.route('/form')
# def form():
#     return render_template('form.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    # if request.method == 'GET':
    #     return "Login via the login Form"
     
    if request.method == 'POST':
        file = request.files['file']
        # filename = file.filename
        # file_path = '/path/to/save/file/' + filename
        file.save(file)
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Upload (file) VALUES ('"+file+"')")
        mysql.connection.commit()
        cursor.close()
        return render_template('upload.html')
        # return f"Done!!"



if __name__ == "__main__":
    app.run(debug=True , port=7777)

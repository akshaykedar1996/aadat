import json
from flask import Flask, jsonify, Blueprint, request
from flask_mysqldb import MySQL
from flask_restful import Api, Resource
from Config import MySqlDBConnection, token_required

upload = Blueprint("upload", __name__ )
app = Flask(__name__)
mysql = MySqlDBConnection(app)


# Get all categories
@upload.route('/get-upload')
def get_upload():
    upload = upload.query.all()
    return jsonify([c.__dict__ for c in upload])



@upload.route('/get-uploadinfo', methods=['GET'])
def getuploadinfo():  
    try:
        cur = mysql.connection.cursor()
        # cur = mysql.cursor()
        cur.execute("SELECT * FROM Upload")
        data = cur.fetchall()
        response = jsonify({"message": "get-File successfully.","status":"success", "data": data})  
    except Exception as e:
        print(e,"error kkkkkkkkkkk")
        response = jsonify({"message": "get-File failed","status":"failed"})  
    return response



@upload.route('/get-uploadProfile', methods=['POST'])
def upload_file():
    response = jsonify({"message": "File uploaded successfully.","status":"success"})  
    try:
        file = request.files['file']
        file.save('/path/to/save/file')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Upload (file) VALUES ('"+file+"')")
        mysql.connection.commit()
        cur.close()
        response = jsonify({"message": "File uploaded successfully","status":"success"})  
    except Exception as e:
        print("File upload failed:", str(e)) # print the error message to the console
        response = jsonify({"message": "File uploaded failed","status":"failed"})  
    return response

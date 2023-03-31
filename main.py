import json
from flask import Flask, jsonify, request, redirect,url_for
from flask_restful import Api, Resource
from flask_mysqldb import MySQL
import Config
# from FileUpload import upload
from Singlefileu import upload
from flask_cors import CORS, cross_origin



app = Flask(__name__)
app.config['SECRET_KEY'] = 'upload'
# CORS(app, resources={r"/*": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'

mysql = Config.MySqlDBConnection(app)

# app.register_blueprint(upload,url_prefix='/upload')
app.register_blueprint(upload,url_prefix='/upload')


if __name__ == "__main__":
    app.run(debug=True , port=8888)

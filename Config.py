from flask import Flask, jsonify, request
from flask_restful import Api
from flask_mysqldb import MySQL
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

DB_NAME = 'EmployerDB'
DB_PASSWD = 'AppaBaba#2050'
# DB_PASSWD = 'AppaBaba#2050'
HOST = 'localhost'
USER = 'root'
AUTHKEY = 'premus2023'


def MySqlDBConnection(app):
    api = Api(app)
    app.config['MYSQL_HOST'] = HOST
    app.config['MYSQL_USER'] = USER
    app.config['MYSQL_PASSWORD'] = DB_PASSWD
    app.config['MYSQL_DB'] = DB_NAME
    
    return MySQL(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # ffff = jwt.encode(
        #             {},
        #             AUTHKEY,
        #             algorithm="HS256"
        #         )
        # print(ffff,"tttttttttttt")
        token = request.headers.get('Authorization')        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:            
            data = jwt.decode(token, AUTHKEY, algorithms=['HS256'])
            print(data)
        except Exception as e:
            print(str(e),"dddddddddddddddddddddddddd")
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

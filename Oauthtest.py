# Step 1: Install Required Libraries
# Install the required libraries including Flask, Flask-RESTful, Flask-JWT-Extended, and mysql-connector-python.
# pip install flask flask-restful flask-jwt-extended mysql-connector-python

# Step 2: Set Up the Database
# Set up a MySQL database and create a table for storing user information. Here is an example SQL query to create a users table:
# CREATE TABLE `users` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `username` varchar(255) NOT NULL,
#   `password` varchar(255) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


# Step 3: Create Flask App
# Create a Flask app and set up JWT and MySQL database connections. Here is an example code:

from flask import Flask,request
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
import mysql.connector
from flask import Flask
from flask import jsonify
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
api = Api(app)
jwt = JWTManager(app)
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='AppaBaba#2050',
    database='EmployerDB'
)
cursor = db.cursor()


# Step 4: Create Auth Endpoints
# Create endpoints for registering and logging in users. Here is an example code:

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
        result = cursor.fetchone()
        if result:
            return {'message': 'Username already exists'}, 400
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        db.commit()
        return {'message': 'User registered successfully'}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        result = cursor.fetchone()
        if result is None:
            return {'message': 'Invalid credentials'}, 401
        access_token = create_access_token(identity=result[0])
        return {'access_token': access_token}, 200

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')


# Step 5: Create Chatbot Endpoint
# Create an endpoint for the chatbot. Here is an example code:
class Chatbot(Resource):
    @jwt_required
    def post(self):
        # process chatbot request here
        return {'message': 'Hello World!'}, 200

api.add_resource(Chatbot, '/chatbot')



if __name__ == "__main__":
    app.run(debug=True, port=7777)


# Step 6: Run the App
# Run the Flask app using the following command:    

# python3 Oauthtest.py

import numpy as np
import pickle
import json
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, request, Response
from flask.json import jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@127.0.0.1:3306/asd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

model = pickle.load(open('ada_model.pkl', 'rb'))

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __init__(self,email,password,name):
        self.email = email
        self.password = password
        self.name = name

class Questions(db.Model):
    userid = db.Column(db.Integer, primary_key = True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    q8 = db.Column(db.Integer)
    q9 = db.Column(db.Integer)
    q10 = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    jaundice = db.Column(db.Integer)
    family = db.Column(db.Integer)
    who = db.Column(db.Integer)
    res = db.Column(db.Integer)


    def __init__(self, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, age, gender, jaundice, family, who,res):
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q6 = q6
        self.q7 = q7
        self.q8 = q8
        self.q9 = q9
        self.q10 = q10
        self.age = age
        self.gender = gender
        self.jaundice = jaundice
        self.family = family
        self.who = who
        self.res = res

@app.route('/hello')
def home():
    message = "Hello World, I'm Ratan"
    return Response(json.dumps(message), status=200, mimetype='application/json')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "GET":
        message = "Success"
        return Response(json.dumps(message), status=200, mimetype='application/json')
    
    if request.method == "POST":
        request_data = json.loads(request.data)
        print(request_data)
        return Response(json.dumps(request_data), status=201, mimetype='application/json')

@app.route('/login',methods=["POST"])
def login():
    if request.method == "POST":
        request_data = json.loads(request.data)
        print(request_data)
        return Response(json.dumps(request_data), status=201, mimetype='application/json')


@app.route('/predict',methods=["POST"])
def predict():
    if request.method == "POST":
        request_data = json.loads(request.data)
        print(request_data)
        questions = []
        for i,j in request_data.items():
            questions.append(j)
        features = [0 if int(x)<0 else 1 for x in questions[:10]] + [int(x) for x in questions[10:]]
        final_features = [np.array(features)]
        prediction = model.predict(final_features)
        print(final_features)
        print(prediction)    
        return Response(json.dumps(features), status=201, mimetype='application/json')         
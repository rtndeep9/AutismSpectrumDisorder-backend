import numpy as np
import pickle
import json
from flask_sqlalchemy import SQLAlchemy



from flask import Flask, request, Response,jsonify
from flask.json import jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy.orm import backref

app = Flask(__name__)
cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@127.0.0.1:3306/asd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

model = pickle.load(open('ada_model.pkl', 'rb'))

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    questions = db.relationship('Questions',backref="owner")

    def __init__(self,email,password,name):
        self.email = email
        self.password = password
        self.name = name

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
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
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    jaundice = db.Column(db.Integer)
    family = db.Column(db.Integer)
    who = db.Column(db.Integer)
    res = db.Column(db.Integer)
    contact = db.Column(db.String(10))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))


    def __init__(self, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, name,age, gender, jaundice, family, who,res,contact,owner):
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
        self.name = name
        self.age = age
        self.gender = gender
        self.jaundice = jaundice
        self.family = family
        self.who = who
        self.res = res
        self.contact = contact
        self.owner_id = owner

class Patients(db.Model):
    __tablename__='patients'
    pid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    result = db.Column(db.Integer)
    contact = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('doctor.doc_id'))

    def __init__(self,name,age,gender,result,contact,owner):
        self.name = name,
        self.age = age,
        self.gender = gender,
        self.result = result,
        self.contact = contact,
        self.owner_id = owner


class Doctor(db.Model):
    __tablename__ = 'doctor'
    doc_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    designation = db.Column(db.String(10))
    experience = db.Column(db.Integer)
    contact = db.Column(db.String(10))
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    patients = db.relationship('Patients',backref="owner")

    def __init__(self,name,desig,exp,contact,email,password):
        self.name=name,
        self.designation = desig,
        self.experience = exp,
        self.contact = contact,
        self.email = email,
        self.password = password


_details = None

#User
@app.route('/hello')
def home():
    message = "Hello World, I'm Ratan"
    return Response(json.dumps(message), status=200, mimetype='application/json')

@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        request_data = json.loads(request.data)
        _name = request_data['username']
        _email = request_data['email']
        _password = request_data['password']
        _checkPassword = request_data['checkPassword']
        print(request_data)

        if _name and _email and _password and request.method == 'POST':
            user = User.query.filter_by(email=_email).first()
            if user:
                message = "User Already Exists"
                return Response(json.dumps(message), status=500, mimetype='application/json')
            elif _checkPassword != _password:
                message = "Password Mismatch"
                return Response(json.dumps(message), status=500, mimetype='application/json')
            else:
                adduser = User(_email,_password,_name)
                db.session.add(adduser)
                db.session.commit()
                message = "User successfully registered "
                return Response(json.dumps(message), status=200, mimetype='application/json')
        else:
            message = "All fields are required"
            return Response(json.dumps(message), status=500, mimetype='application/json')

@app.route('/login',methods=["POST"])
def login():
    # global _email
    if request.method == "POST":
        request_data = json.loads(request.data)
        print(request_data)
        _email = request_data['email']
        _password = request_data['password']
       
       
        if _email and _password:
            user = User.query.filter_by(email=_email,password=_password).first()
            if user:
                return Response(json.dumps(request_data['email']), status=201, mimetype='application/json')
            else:
                message = "Invalid Credentials"
                return Response(json.dumps(message), status=500, mimetype='application/json')
        else:
            message = "All fields are required"
            return Response(json.dumps(message), status=500, mimetype='application/json')
        
@app.route('/details',methods=["POST"])
def getDetails():
    global _details
    if request.method == "POST":
        request_data = json.loads(request.data)
        print(request_data)
        _details = list(request_data.values())
        print(_details)
        message = "Success"   
        return Response(json.dumps(message), status=201, mimetype='application/json')

@app.route('/predict',methods=["POST"])
def predict():
    global _details
    if request.method == "POST":
        request_data = json.loads(request.data)
        print(request_data)
       
        questions = list(request_data.values())
        _email = request_data['email']        
        
        features = [0 if int(x)<0 else 1 for x in questions[:10]] + [int(x) for x in _details[1:6]]
        final_features = [np.array(features)]
        prediction = model.predict(final_features)

        print(features)
        print(prediction)

        result = True if prediction[0] == 1 else False
        

        user = User.query.filter_by(email=_email).first()

        q1 = features[0]
        q2 = features[1]
        q3 = features[2]
        q4 = features[3]
        q5 = features[4]
        q6 = features[5]
        q7 = features[6]
        q8 = features[7]
        q9 = features[8]
        q10 = features[9]
        name = _details[0]
        age = features[11]
        gender = features[10]
        jaundice = features[12]
        family = features[13]
        who = features[14]
        contact = _details[-1]

        mydata = Questions(q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,name,age,gender,jaundice,family,who,result,contact,user.user_id)
        print(mydata)
        db.session.add(mydata)
        db.session.commit()
        _details = None
        return Response(json.dumps(result), status=201, mimetype='application/json')

@app.route('/result',methods=['POST'])
def result():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        _email = request_data['email']
        user = User.query.filter_by(email=_email).first()
        query = Questions.query.filter_by(owner_id=user.user_id)
        results = query.order_by(Questions.id.desc()).first()
        res = json.dumps({
            "name":results.name,
            "result":results.res,
            "gender":results.gender,
            "age":results.age,
            "contact":results.contact
        })
        
        return Response(res, status=200, mimetype='application/json')

@app.route('/doctors',methods=['GET'])
def doctors():
    if request.method == "GET":
        alldoctors = Doctor.query.all()
        result = [d.__dict__ for d in alldoctors]
        for i in range(len(result)):
            result[i].pop('_sa_instance_state')
        print(result)
        message = "Success"
        return Response(json.dumps(result), status=200, mimetype='application/json')

@app.route('/addpatient',methods=['POST'])
def addPatient():
    if request.method == "POST":
        request_data = json.loads(request.data)
        print(request_data)
        _name = request_data['name']
        _age = request_data['age']
        _gender = request_data['gender']
        _result = request_data['result']
        _contact = request_data['contact']
        _email = request_data['email']        
   
        user = Doctor.query.filter_by(email=_email).first()
        patientData = Patients(_name,_age,_gender,_result,_contact,user.doc_id)
        db.session.add(patientData)
        db.session.commit()
        result = {
            "message":"Successfully added"
        }
        return Response(json.dumps(result), status=201, mimetype='application/json')

#Doctor
@app.route('/doctor-register',methods=['POST'])
def docRegister():
    if request.method == "POST":
        request_data = json.loads(request.data)
        _name = request_data['name']
        _designation = request_data['designation']
        _experience = request_data['experience']
        _contact = request_data['contact']
        _email = request_data['email']
        _password = request_data['password']
        _checkPassword = request_data['checkPassword']
        print(request_data)

        if request.method == 'POST':
            user = Doctor.query.filter_by(email=_email).first()
            if user:
                message = "User Already Exists"
                return Response(json.dumps(message), status=500, mimetype='application/json')
            elif _checkPassword != _password:
                message = "Password Mismatch"
                return Response(json.dumps(message), status=500, mimetype='application/json')
            else:
                adduser = Doctor(_name,_designation,_experience,_contact,_email,_password)
                db.session.add(adduser)
                db.session.commit()
                message = "User successfully registered "
                return Response(json.dumps(message), status=200, mimetype='application/json')
        else:
            message = "All fields are required"
            return Response(json.dumps(message), status=500, mimetype='application/json')

@app.route('/doctor-login',methods=['POST'])
def docLogin():
    if request.method == "POST":
        request_data = json.loads(request.data)
        print(request_data)
        _email = request_data['email']
        _password = request_data['password']
        print(request_data)
       
        if _email and _password:
            user = Doctor.query.filter_by(email=_email,password=_password).first()
            if user:
                res = {
                    "doctor":request_data['email'],
                }
                return Response(json.dumps(res), status=201, mimetype='application/json')
            else:
                message = "Invalid Credentials"
                return Response(json.dumps(message), status=500, mimetype='application/json')
        else:
            message = "All fields are required"
            return Response(json.dumps(message), status=500, mimetype='application/json')

@app.route('/mypatients',methods=['POST'])
def myPatients():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        _email = request_data['email']
        doctor = Doctor.query.filter_by(email=_email).first()
        patients = Patients.query.filter_by(owner_id=doctor.doc_id).all()
        result = [d.__dict__ for d in patients]
        for i in range(len(result)):
            result[i].pop('_sa_instance_state')
        print(result)
        message = "Success"
        return Response(json.dumps(result), status=200, mimetype='application/json')



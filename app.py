from flask import Flask
from flask import request
import dcapi
app = Flask(__name__)

@app.route('/')
def square_of_distrust():
    return 'Welcome to the Square of Distrust!'

@app.route('/createReview', methods=['POST'])
def createReview():
    rating = request.form['rating']
    lat = request.form['lat']
    lon = request.form['lon']
    comments = request.form['comments']
    userId = request.form['userId']
    message = dcapi.postReview(rating, lat, lon, comments, userId)
    return message


@app.route('/register', methods=['POST'])
def register():
    userId = request.form['userId']
    email = request.form['email']
    password = request.form['password']
    success = dcapi.register(userId, email, password)
    if success == False:
        return {'status' : 'error', 'message' : 'Something went wrong, please try again!'}
    else:
        return {'status' : 'ok', 'message' : 'Registration successful!', 'userId' : userId}

@app.route('/login', methods=['POST'])
def login():
    userId = request.form['userId']
    password = request.form['password']
    success = dcapi.login(userId, password)
    if success == False:
        return {'status' : 'error', 'message' : 'Login was not successful! Please make sure your email or password is correct'}
    else:
        return {'status' : 'ok', 'message' : 'Login successful!', 'userId' : userId}


@app.route('/updateGunLaws')
def uploadGunLaws():
    dcapi.postGunLaws()
    return 'update'

@app.route('/updateCrimes')
def test_db():
    dcapi.updateCrimes(40.520911, -74.461223, .1)
    return 'updateCrimes'

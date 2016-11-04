from flask import Flask
import spotcrime
app = Flask(__name__)

@app.route('/')
def square_of_distrust():
    return 'Welcome to the Square of Distrust!'

@app.route('/test')
def test_db():
    spotcrime.getCrimeData(40.520911, -74.461223, .01)
    return 'test'

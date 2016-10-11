import requests
import dbhelper

baseURL = "http://api.spotcrime.com/crimes.json"
key = "."

#USE THIS TO UPDATE OUR DATABASE NOT FOR CLIENT-SIDE DATA
def getCrimeData(lat, lon, radius):
    payload = {'key' : key, 'lat' : lat, 'lon' : lon, 'radius' : radius}
    r = requests.get(baseURL, params=payload)
    crimes = r.crimes
    for crime in crimes:
        #the type of the crime
        cType = crime.type
        #date of the crime with time in string format "MM/DD/YY HH:SS AM/PM"
        date = crime.date
        #latitude
        latitude = crime.lat
        #longitude
        longitude = crime.lon
        #TODO: add in method here (create in separate module) that uploads this data to DB if it isnt there already

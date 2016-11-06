import requests
import dcapi

baseURL = "http://api.spotcrime.com/crimes.json"
key = "."

#USE THIS TO UPDATE OUR DATABASE NOT FOR CLIENT-SIDE DATA
def getCrimeData(lat, lon, radius):
    payload = {'key' : key, 'lat' : lat, 'lon' : lon, 'radius' : radius}
    r = requests.get(baseURL, params=payload)
    data = r.json()
    crimes = data['crimes']
    count = 0
    return crimes

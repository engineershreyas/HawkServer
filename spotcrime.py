import requests
import dcapi

baseURL = "https://api.spotcrime.com/crimes.json"
key = "privatekeyforspotcrimepublicusers-commercialuse-877.410.1607"

#USE THIS TO UPDATE OUR DATABASE NOT FOR CLIENT-SIDE DATA
def getCrimeData(lat, lon, radius):
    payload = {'key' : key, 'lat' : lat, 'lon' : lon, 'callback' : '', 'radius' : radius, '_' : '1481078110370'}
    r = requests.get(baseURL, params=payload)
    data = r.json()
    crimes = data['crimes']
    count = 0
    return crimes

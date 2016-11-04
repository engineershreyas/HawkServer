import dbhelper
import geocoder



def putCrimeIfNecessary(cType, date, lat, lon):
    cId = generateId(date, lat, lon)
    sqlCommand = "SELECT * FROM crimes t WHERE t.cId = " + wrapApos(cId)
    result  = dbhelper.doOperation(sqlCommand, True, 1)
    if result == None:
        putCrime(cId, cType, date, lat, lon)

def putCrime(cId, cType, date, lat, lon):
    cityState = getCityState(lat, lon)
    geo = str(lat) + "," + str(lon)
    sqlCommand = "INSERT INTO crimes VALUES (" + wrapApos(cId) + ", " + wrapApos(cType) + ", " + wrapApos(date) + ", " + wrapApos(geo) + ", " + wrapApos(cityState) + ")"
    dbhelper.doOperation(sqlCommand, False, 0)

def wrapApos(word):
    return "\'" + word + "\'"

#helper method to create id for crime
def generateId(date,lat,lon):
    dateNoSpaces = date.replace(" ","")
    dateNoSlashes = dateNoSpaces.replace("/","")
    dateNoColons = dateNoSlashes.replace(":","")
    dateNoPM = dateNoColons.replace("PM","")
    dateNoAM = dateNoPM.replace("AM","")
    l = []
    l.append(dateNoAM)
    latStr = str(lat)
    lonStr = str(lon)
    l.append(latStr)
    l.append(lonStr)
    cId = ''.join(l)
    cId = cId.replace("-", "")
    cId = cId.replace(".","")
    return cId

#helper method to get city state
def getCityState(lat, lon):
    latD = float(lat)
    lonD = float(lon)
    g = geocoder.google([latD, lonD], method='reverse')
    city = g.city
    state = g.state
    cityState = city + "," + state
    return cityState

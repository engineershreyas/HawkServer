import dbhelper
import geocoder

#TODO: put in tablename
tableName = ""

def putCrimeIfNecessary(cType, date, lat, lon):
    cId = generateId(date, lat, lon)
    sqlCommand = "SELECT * FROM " + tablename  + " t WHERE t.cId = `%(cId)`"
    args = {'cId' : cId}
    result  = dbhelper.doOperation(sqlCommand, args, True, 1)
    if result == None:
        putCrime(cId, cType, date, lat, lon)

def putCrime(cId, cType, date, lat, lon):
    sqlCommand = "INSERT INTO " + tableName + " ( cId, cType, geo, datetime, citystate ) VALUES (`%(cId)`, `%(cType)`, `%(geo)`, `%(datetime)`, `%(citystate)`)"
    cityState = getCityState(lat, lon)
    geo = lat + "," + lon
    args = {'cId' : cId, 'datetime' : date, 'geo' : geo, 'cType' : cType, 'citystate' : cityState}
    dbhelper.doOperation(sqlCommand, args, False, 0)

#helper method to create id for crime
def generateId(date,lat,lon):
    dateNoSpaces = date.replace(" ","")
    dateNoSlashes = dateNoSpaces.replace("/","")
    dateNoColons = dateNoSlashes.replace(":","")
    l = []
    l.append(dateNoColons)
    l.append(lat)
    l.append(lon)
    cId = ''.join(l)
    return cId

#helper method to get city state
def getCityState(lat, lon):
    latD = float(lat)
    lonD = float(lon)
    g = geocoder.google([latD, lonD], method='reverse')
    city = g.city
    state = g.state
    cityState = city + state
    return cityState

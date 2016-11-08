import dbhelper
import geocoder
import spotcrime
import bcrypt
import gunlaws
import json
from math import asin, acos, sin, cos


"""User Related Methods"""
def register(userId, email, password):
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if not checkIfUserExists(userId, email):
        sqlCommand = "INSERT INTO users VALUES (" + wrapApos(userId) + ", " + wrapApos(email) + ", " + wrapApos(hashed) + ")"
        result = dbhelper.doOperation(sqlCommand, False, 0)
        return result['status'] == 'ok'

def login(userId, password):
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    sqlCommand = "SELECT hashed FROM users WHERE userId = " + wrapApos(userId)
    result = dbhelper.doOperation(sqlCommand, True, 1)
    if result == None:
        return False
    else:
        if result['hashed'] == hashed:
            return True
        return False

def checkIfUserExists(userId, email):
    sqlCommand = "SELECT * FROM users WHERE userId = " + wrapApos(userId) + " OR " + " email = " + wrapApos(email)
    result = dbhelper.doOperation(sqlCommand, True, 1)
    return result != None

""" Gun Law Related Methods """
def postGunLaws():
    glaws = gunlaws.getGunLaws()
    states = gunlaws.getStates()
    deleteSqlCommand = "TRUNCATE states"
    dbhelper.doOperation(deleteSqlCommand, False, 0)
    for state in states:
        glaw = glaws[state]
        sqlCommand = "INSERT INTO states VALUES (" + wrapApos(state) + ", " + wrapApos(glaw) + ")"
        result = dbhelper.doOperation(sqlCommand, False, 0)
        if result['status'] != 'ok':
            dbhelper.doOperation(deleteSqlCommand, False, 0)
            print "Something wrong with inserting gunlaws, please check data"
            break


"""Crime Related Methods"""

def updateCrimes(lat, lon, radius):
    crimes = spotcrime.getCrimeData(lat, lon, radius)
    count = 0
    for crime in crimes:
        #the type of the crime
        cType = crime['type']
        #date of the crime with time in string format "MM/DD/YY HH:SS AM/PM"
        date = crime['date']
        #latitude
        latitude = crime['lat']
        #longitude
        longitude = crime['lon']
        count = count + 1
        success = putCrimeIfNecessary(cType, date, latitude, longitude)
        if success == False:
            print "Insert failed with data: " + json.dumps(crime)
    print str(count) + " crimes found"

def putCrimeIfNecessary(cType, date, lat, lon):
    cId = generateId(date, lat, lon)
    sqlCommand = "SELECT * FROM crimes t WHERE t.cId = " + wrapApos(cId)
    result  = dbhelper.doOperation(sqlCommand, True, 1)
    if result == None:
        return putCrime(cId, cType, date, lat, lon)

def putCrime(cId, cType, date, lat, lon):
    cityState = getCityState(lat, lon)
    sqlCommand = "INSERT INTO crimes VALUES (" + wrapApos(cId) + ", " + wrapApos(cType) + ", " + wrapApos(date) + ", " + wrapApos(cityState) + "," + degreesToRadians(float(lat)) + "," + degreesToRadians(float(lon)) + ")"
    result = dbhelper.doOperation(sqlCommand, False, 0)
    if result['status'] == 'error':
        return False
    else:
        return True

#get crimes by geocoordinates and radius (in miles)
def getCrimes(lat, lon, radius):
    kilometers = radius * 1600
    angularRadius = kilometers / 6371
    latr = degreesToRadians(lat)
    lonr = degreesToRadians(lon)
    latmin = latr - angularRadius
    latmax = latr + angularRadius
    latt = asin(sin(latr)/cos(angularRadius))
    delta = asin(sin(angularRadius)/cos(latr))
    lonmin = lonr - delta
    lonmax = lonr + delta
    sqlCommand = "SELECT * FROM crimes WHERE (lat >= " + latmin  + "AND lat <=  " +  latmax + " ) AND (lon >= " + lonmin + "AND lon <= " lonmax + ") AND (ACOS(SIN(" + latr + ") * SIN(lat) + COS(" + latr + ") * COS(lat) * COS(lon - (" + lonr  + "))) <= " + angularRadius
    results = dbhelper.doOperation(sqlCommand, True, -1)
    return results

"""Safety Review Related Methods"""
def postReview(rating, lat, lon, comments, userId):
    rId = 0
    cityState = getCityState(lat, lon)
    city = cityState.split(",")[0]
    retrieveSqlCommand = "SELECT score, numOfReviews FROM cities WHERE name = " + wrapApos(city)
    cityInfo = dbhelper.doOperation(retrieveSqlCommand, True, 1)
    score = float(cityInfo['score'])
    numOfReviews = int(cityInfo['numOfReviews'])
    totalScore = score * numOfReviews
    numOfReviews = numOfReviews + 1;
    totalScore = (totalScore + rating) / float(numOfReviews)
    updateSqlCommand = "UPDATE cities SET score = " + totalScore + ", numOfReviews = " + numOfReviews + " WHERE name = " + city
    message = None
    res = dbhelper.doOperation(updateSqlCommand, False, 0)
    if res['status'] == 'error':
        print 'Updating cities failed'
        message = {'status' : 'error', 'message' : 'Posting review failed, please try again!'}
        return message
    latr = degreesToRadians(float(lat))
    lonr = degreesToRadians(float(lon))
    insertSqlCommand = "INSERT INTO reviews VALUES (" + rId + ", " + rating + ", " + wrapApos(cityState) + ", " + wrapApos(comments) + ", " + wrapApos(userId) + + "," + latr + "," + lonr + ")"
    res = dbhelper.doOperation(insertSqlCommand, False, 0)
    if res['status'] == 'error':
        message = {'status' : 'error', 'message' : 'Posting review failed, please try again!'}
        return message
    rId = getReviewCount() - 1
    return {'status' : 'success', 'rId' : rId}

def getReviewCount():
    sqlCommand = "SELECT * FROM reviews"
    result = dbhelper.doOperation(sqlCommand, True, -1)
    return len(result)

"""HELPER METHODS"""

def degreesToRadians(degrees):
    return degrees * .0174533

#helper method to wrap variable in single apostrophes for sql statements s
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
    print city
    print state
    cityState = city + "," + state
    return cityState

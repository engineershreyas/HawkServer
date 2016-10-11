import pymysql.cursors

#database host
host = None
#username for host
username = None
#password for host
password = None
#database name
db = None
#charset
charset = 'utf8mb4'
#cursor class
cursorclass = pymysql.cursors.DictCursor


"""
sqlCommand - the SQL command (in MySQL) to do what you want to do
args - a dict representing args for sqlCommand, can be None
retrieve - a boolean denoting if this is a retrieval operation or NOT
size - number of results to be returned, will be ignored if retrieve is False, put 0 to get all results
"""
def doOperation(sqlCommand, args, retrieve, size):
    connection = pymysql.connect(host=host,
                                 user=username,
                                 password=password,
                                 db=db,
                                 charset=charset,
                                 cursorclass=cursorclass)
    result = None
    try:
        with connection.cursor() as cursor:
            if retrieve == True:
                cursor.execute(sqlCommand, args)
                if size <= 0:
                    result = cursor.fetchall()
                elif size == 1:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchmany(size)
        if retrieve == False:
            connection.commit()
    finally:
        connection.close()
        return result

import pymysql.cursors

#database host
host = 'localhost'
#username for host
username = 'root'
#password for host
password = 'shreyas'
#database name
db = 'hawk'
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
def doOperation(sqlCommand, retrieve, size):
    connection = pymysql.connect(host=host,
                                 user=username,
                                 password=password,
                                 database=db,
                                 autocommit=True,
                                 charset=charset,
                                 cursorclass=cursorclass)
    result = None
    try:
        with connection.cursor() as cursor:
            print sqlCommand
            cursor.execute(sqlCommand)
            if retrieve == True:
                if size <= 0:
                    result = cursor.fetchall()
                elif size == 1:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchmany(size)
        connection.commit()
    finally:
        connection.close()
        return result

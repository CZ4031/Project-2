# Imports
from cgi import test
from cgitb import text
import psycopg2
import json

# Connect to Postgre database
def validateConnect(username, password, database_name):
    connection = None
    try:
        connection = psycopg2.connect(database=database_name, user=username, password=password)
        verify = True

        # Write login information into json file
        loginInfo = {
            "username" : username,
            "password" : password,
            "database" : database_name
        }
        json_object = json.dumps(loginInfo, indent=4)
        with open("loginInfo.json", "w") as outputfile:
            outputfile.write(json_object)
    except (Exception, psycopg2.DatabaseError):
        verify = False
    
    return verify

def connect():
    """Connect using credentials"""
    connection = None
    loginInfo = json.load(open('loginInfo.json', "r"))
    username = loginInfo['username']
    password = loginInfo['password']
    database_name = loginInfo['database']
    try:
         connection = psycopg2.connect(database=database_name, user=username, password = password)
         # Create a cursor
         cursor = connection.cursor()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return cursor

def executeQuery(query):
    optimalQEP = "EXPLAIN (ANALYSE, VERBOSE, COSTS, FORMAT JSON)" + query

    try:
        cursor = connect()
        cursor.execute(optimalQEP)
        explain_query = cursor.fetchall()
        executed = True
    except(Exception, psycopg2.DatabaseError) as error:
        explain_query = "Please check your sql statement: \n" + text
        executed = False
    finally: 
        cursor.close()

    # write explain details into json file
    with open('optimalQueryPlan.json', 'w') as output_file:
        json.dump(explain_query, output_file, ensure_ascii = False, indent = 2)

    return executed
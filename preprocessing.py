# Imports

# Need to run the following installations
# pip install psycopg2
# pip install python-decouple
from cgi import test
from cgitb import text
import psycopg2
from decouple import config
import json

class SetUp():
    # , host, port_num, database_name, username, password
    def __init__(self):
        # Setting up connection
        self.connection = None
        try:
            self.connection = psycopg2.connect(host = config("HOST"), port = config("PORT") ,database= config("DATABASE"), user= config("USER"), password= config("PASSWORD"))
            self.verify = True
            if(self.verify):
                self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError):
            self.verify = False

    def executeQuery(self, query):
        optimalQEP = "EXPLAIN (ANALYSE, VERBOSE, COSTS, FORMAT JSON)" + query

        try:
            cursor = self.cursor
            cursor.execute(optimalQEP)
            explain_query = cursor.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            explain_query = "Please check your sql statement: \n" + text
        finally: 
            cursor.close()

        # write explain details into json file
        with open('chosenQueryPlan.json', 'w') as output_file:
            chosenQueryPlan = (json.dump(explain_query, output_file, ensure_ascii = False, indent = 4))

        return chosenQueryPlan

         # # Connect to Postgre database
    # def validateConnect(username, password, database_name):
    #     connection = None
    #     try:
    #         connection = psycopg2.connect(database=database_name, user=username, password=password)
    #         verify = True

    #         # Write login information into json file
    #         loginInfo = {
    #             "username" : username,
    #             "password" : password,
    #             "database" : database_name
    #         }
    #         json_object = json.dumps(loginInfo, indent=4)
    #         with open("loginInfo.json", "w") as outputfile:
    #             outputfile.write(json_object)
    #     except (Exception, psycopg2.DatabaseError):
    #         verify = False
        
    #     return verify

    # def connect():
    #     """Connect using credentials"""
    #     connection = None
    #     loginInfo = json.load(open('loginInfo.json', "r"))
    #     username = loginInfo['username']
    #     password = loginInfo['password']
    #     database_name = loginInfo['database']
    #     try:
    #         connection = psycopg2.connect(database=database_name, user=username, password = password)
    #         # Create a cursor
    #         cursor = connection.cursor()
    #     except(Exception, psycopg2.DatabaseError) as error:
    #         print(error)
    #     finally:
    #         return cursor
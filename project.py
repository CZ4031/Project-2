from preprocessing import *

if __name__ == "__main__":
    # username = "postgres"
    # password = ""
    # database_name = "TPC-H"
    print("Welcome to CZ4003 database")
    connect = SetUp()
    query = "SELECT * FROM customer"
    result = connect.executeQuery(query)
    print(result)

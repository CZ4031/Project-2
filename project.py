from preprocessing import validateConnect, executeQuery

if __name__ == "__main__":
    username = "postgres"
    password = "Dragonslayer1999"
    database_name = "TPC-H"
    print("Welcome to CZ4003 database")
    # result = validateConnect(username, password, database_name)
    query = "SELECT * FROM customer"
    result = executeQuery(query)
    print(result)
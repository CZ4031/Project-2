# Imports

# Need to run the following installations
# pip install psycopg2
# pip install python-decouple
from cgi import test
from cgitb import text
import psycopg2
from decouple import config
import json

class PlanNode():

    # Construct a node
    def __init__(self) -> None:
        self.parent = None
        self.children = []
        self.attributes = {}
    
    def print_tree(self):
        queue = []
        queue.append(self)
        while len(queue) != 0:
            childlength = len(queue)
            # Add appropriate children ndoes
            for i in range(childlength):
                node = queue.pop(0)
                if node != None:
                    print(node.attributes['Node Type'] + "->cost: ", node.attributes['Total Cost'] , end='\n')
                for child in node.children:
                    queue.append(child)

    def check_for_join(self):
        queue = []
        queue.append(self)
        joins_used = {}
        while len(queue)!=0:
            childlength = len(queue)
            for i in range(childlength):
                node = queue.pop(0)
                if "Join" in node.attributes['Node Type'] or "Loop" in node.attributes['Node Type']:
                    joins_used[node.attributes['Node Type']] = int(node.attributes['Total Cost'])
                for child in node.children:
                    queue.append(child)
        return joins_used


class SetUp():
    # Attributes
    off_config = {
        # Joins
        "Hash Join" : "set enable_hashjoin=off",
        "Merge Join" : "set enable_mergejoin=off",
        "Nested Loop" : "set enable_nestloop=off",
        # Scans
        "Seq Scan" : "set enable_seqscan=off",
        "Index Scan" : "set enable_indexscan=off",
        "Bitmap Scan": "set enable_bitmapscan=off",
        "Index Only Scan": "set enable_indexonlyscan=off",
        "Tid Scan": "set enable_tidscan=off",
        # Sort
        "Sort" : "set enable_sort=off",
        #Others
        "Hash Agg": "set enable_hashagg=off",
        "Material": "set enable_material=off",
    }

    on_config = {
        # Joins
        "Hash Join" : "set enable_hashjoin=on",
        "Merge Join" : "set enable_mergejoin=on",
        "Nested Loop" : "set enable_nestloop=on",
        # Scans
        "Seq Scan" : "set enable_seqscan=on",
        "Index Scan" : "set enable_indexscan=on",
        "Bitmap Scan": "set enable_bitmapscan=on",
        "Index Only Scan": "set enable_indexonlyscan=on",
        "Tid Scan": "set enable_tidscan=on",
        # Sort
        "Sort" : "set enable_sort=on",
        #Others
        "Hash Agg": "set enable_hashagg=on",
        "Material": "set enable_material=on",
    }

    query_plans = {
        "chosen_plan": "",
        "alternative_plans": []
    }



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

    def executeQuery(self, query, off=[]):
        optimalQEP = "EXPLAIN (ANALYSE, VERBOSE, COSTS, FORMAT JSON)" + query

        try:
            # set cursor variable
            cursor = self.cursor
            #Setting off for alternate query plans
            for condition in off:
                #print(self.off_config[condition])
                # 5s timeout
                cursor.execute("set statement_timeout = 5000")
                cursor.execute(self.off_config[condition])
            
            cursor.execute(optimalQEP)
            
            explain_query = cursor.fetchall()

            # Setting config back on to set up for next alternate query plan
            for condition in off:
                #print(self.on_config[condition])
                cursor.execute(self.on_config[condition])
            # write explain details into json file
            with open('chosenQueryPlan.json', 'w') as output_file:
                chosenQueryPlan = (json.dump(explain_query, output_file, ensure_ascii = False, indent = 4))

            return explain_query[0][0][0]['Plan']
        except(Exception, psycopg2.DatabaseError) as error:
                
                # Check how to seperate errors
                print("Your error is: ", error)
                # print("Your query is: ", query)
                #explain_query = "Please check your sql statement: \n" + query
                self.connection.rollback()
                return "error"
       

    def add_attributes(self, plan, node):
        """
        Get current plan and insert the corresponding attributes into the current node 
        """
        for key,val in plan.items():
            if key != "Plans":
                node.attributes[key] = val

    def add_node(self, plan,node):
        """
        Recursive create nodes based on the number of "Plans" of current node (Each "Plans" corresponds to an additional child node)
        """
        # Break condition when no further nodes need to be created
        if "Plans" not in plan:
            return
        for plan in plan["Plans"]:
            # Create PlanNode
            child = PlanNode()
            child.parent = node
            self.add_attributes(plan,child)
            self.add_node(plan,child)
            node.children.append(child)

    def build_tree(self, plan):
        """
        Build the query plan tree
        """
        root = PlanNode()
        self.add_attributes(plan, root)
        self.add_node(plan,root)
        return root

   
    def getAllQueryPlans(self, query):

        #Original plan
        plan = self.executeQuery(query)
        root = self.build_tree(plan)
        print("original join: ",root.check_for_join())
        self.query_plans["chosen_plan"] = root
        #connect.query_plans["chosen_plan"].print_tree()

        #Alternate plans (Max: 11)
        #Checking for AEP for Joins 
        #Full Merge Join
        plan = self.executeQuery(query, ["Nested Loop", "Hash Join"])
        if(plan != "error"):
            alternate_root = self.build_tree(plan)
            #print("Merge join: ",root.check_for_join_type())
            self.query_plans["alternative_plans"].append(alternate_root)

        #Full hash join
        plan = self.executeQuery(query, ['Nested Loop', "Merge Join"])
        if(plan != "error"):
            alternate_root = self.build_tree(plan)
            #print("Hash join: ",root.check_for_join_type())
            self.query_plans["alternative_plans"].append(alternate_root)

        #Full nested loop join
        plan = self.executeQuery(query, ['Merge Join', "Hash Join"])
        if(plan != "error"):
            alternate_root = self.build_tree(plan)
            #print("NL join: ",root.check_for_join_type())
            self.query_plans["alternative_plans"].append(alternate_root)

        #Checking for AEP for Scans
        #Seq scan 
        plan = self.executeQuery(query, ["Index Scan", "Bitmap Scan", "Index Only Scan", "Tid Scan"])
        if(plan != "error"):
            alternate_root = self.build_tree(plan)
            #print("NL join: ",root.check_for_join_type())
            self.query_plans["alternative_plans"].append(alternate_root)

        # Index Scan
        plan = self.executeQuery(query, ["Seq Scan", "Bitmap Scan", "Index Only Scan", "Tid Scan"])
        if(plan != "error"):
            alternate_root = self.build_tree(plan)
            #print("NL join: ",root.check_for_join_type())
            self.query_plans["alternative_plans"].append(alternate_root)

        # Bitmap Scan
        plan = self.executeQuery(query, ["Seq Scan", "Index Scan", "Index Only Scan", "Tid Scan"])
        if(plan != "error"):
            alternate_root = self.build_tree(plan)
            #print("NL join: ",root.check_for_join_type())
            self.query_plans["alternative_plans"].append(alternate_root)
        
        # Index Only Scan
        plan = self.executeQuery(query, ["Seq Scan", "Index Scan", "Bitmap Scan", "Tid Scan"])
        if(plan != "error"):
            alternate_root = self.build_tree(plan)
            #print("NL join: ",root.check_for_join_type())
            self.query_plans["alternative_plans"].append(alternate_root)

        # Tid Only Scan
        plan = self.executeQuery(query, ["Seq Scan", "Index Scan", "Bitmap Scan", "Index Only Scan"])
        if(plan != "error"):
            alternate_root = self.build_tree(plan)
            #print("NL join: ",root.check_for_join_type())
            self.query_plans["alternative_plans"].append(alternate_root)

        # Checking for AEP for Sort
        # Sort
        plan = self.executeQuery(query, ["Sort"])
        if(plan != "error"):
            alternate_root = self.build_tree(plan)
            #print("NL join: ",root.check_for_join_type())
            self.query_plans["alternative_plans"].append(alternate_root)

        # Checking for AEP for Others
        # No Hash Agg
        plan = self.executeQuery(query, ["Hash Agg"])
        if(plan != "error"):
            alternate_root = self.build_tree(plan)
            #print("NL join: ",root.check_for_join_type())
            self.query_plans["alternative_plans"].append(alternate_root)

        # No Material
        plan = self.executeQuery(query, ["Material"])
        if(plan != "error"):
            alternate_root = self.build_tree(plan)
            #print("NL join: ",root.check_for_join_type())
            self.query_plans["alternative_plans"].append(alternate_root)

        # Final print
        print("length: ", len(self.query_plans['alternative_plans']))










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
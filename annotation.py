from preprocessing import *
from cgi import test
from cgitb import text
import psycopg2
from decouple import config
import json


class Annotation:
	def traverseTree(self):
		return True

	def generateAnnotation(self, node):
		for attribute in node.attributes:
			# Start if else
			attribute = attribute.lower()
			annotation = ""
			if attribute.contains("scan"):
				if attribute.contains().contains("index"):
					annotation = "Index scan used"
				elif attribute.contains("sequential"):
					annotation = "Sequential scan used"
				else:
					annotation = "Hash scan used"
				node.annotations.append(annotation)

			## need to format all the below cases, for now is static
			elif attribute.contains("Hash Join"):
					annotation = "Hash join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n" 
					node.annotations.append(annotation)

			elif attribute.contains("Hash"):
					annotation = "Perform hashing on table XX, to get resulting table BB.\n" 
					node.annotations.append(annotation)

			elif attribute.contains("Merge Join"):
					annotation = "Merge join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n" 
					node.annotations.append(annotation)

			elif attribute.contains("Nested Loop"):
					annotation = "Nested Loop join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n" 
					node.annotations.append(annotation)

			elif attribute.contains("Aggregate"):
					annotation = "Perform aggregate on table XX, to get resulting table BB.\n" 
					node.annotations.append(annotation)

			elif attribute.contains("Sort"):
					annotation = "Sort table XX in an decremental manner according to key YY, to get resulting table BB.\n" 
					node.annotations.append(annotation)

			elif attribute.contains("Incremental Sort"):
					annotation = "Sort table XX in an incremental manner according to key YY, to get resulting table BB.\n" 
					node.annotations.append(annotation)

			elif attribute.contains("Sort"):
					annotation = "Sort table XX according to key YY, to get resulting table BB.\n" 
					node.annotations.append(annotation)

			elif attribute.contains("Unique"):
					annotation = "Duplicates are removed from table AA.\n" 
					node.annotations.append(annotation)

			elif attribute.contains("Gather"):
					annotation = "Gather operation is performed on table AA, to get resulting table BB.\n" 
					node.annotations.append(annotation)

			elif attribute.contains("Gather Merge"):
					annotation = "Gather Merge operation is performed.\n" 
					node.annotations.append(annotation)

			elif attribute.contains("Append"):
					annotation = "Append table XX to table YY, to get resulting table BB.\n" 
					node.annotations.append(annotation)					
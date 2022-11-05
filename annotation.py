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
			elif attribute.contains("join"):
				if attribute.contains("index"):
					node.annotations.append("Hello world")
				elif attribute.contains("sequential"):
					node.annotations.append()
				else:
					node.annotations.append()


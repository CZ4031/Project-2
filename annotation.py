class Annotation:
	def traverseTree(self, root):
		if not root:
			return
		
		self.generateAnnotation(root)

		if root.children:
			for child in root.children:
				self.traverseTree(child)

	def comparison(self, node):
		if len(node.alternate_plans) != 0:
			for altScan in node.alternate_plans:
				annotation = f"Compared to {node.attributes['Node Type']}, {altScan} is {node.alternate_plans.get(altScan):.2f} " \
								f"times as expensive.\n"
				node.annotations += annotation
		else:
			annotation = f"{node.attributes['Node Type']} is used across all AQPs."
			node.annotations += annotation

	def generateAnnotation(self, node):
		nodeType = node.attributes['Node Type']
		annotation = ""

		# For scans
		if nodeType == "Bitmap Index Scan":
			annotation = "Bitmap index scan is used as multiple indices are constructed for this table.\n"
			node.annotations += annotation
			self.comparison(node)

		if nodeType == "Bitmap Heap Scan":
			annotation = "Bitmap heap scan is used as multiple indices as constructed. A heap is used to " \
							"sort the indices and quickly cut down the number of tuples scanned.\n "
			node.annotations += annotation
			self.comparison(node)

		if nodeType == "Sequential Scan":
			annotation = "Sequential scan is used to read the table as there is no index.\n"
			node.annotations += annotation
			self.comparison(node)

		# For joins
		if nodeType == "Hash Join":
			annotation = "Hash join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n"
			node.annotations += annotation
			self.comparison(node)

		if nodeType == "Merge Join":
			annotation = "Merge join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n"
			node.annotations += annotation
			self.comparison(node)

		if nodeType == "Nested Loop":
			annotation = "Nested Loop join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n"
			node.annotations += annotation
			self.comparison(node)

		# All other operators
		if nodeType == "Hash":
			annotation = "Perform hashing on table.\n"
			node.annotations += annotation

		if nodeType == "Aggregate":
			strategy = node.attributes['Strategy']
			if strategy == "Sorted":
				annotation = f"The Aggregate operation will sort the tuples based on the keys {node.attributes['Group Key']}.\n"
				# if "Filter" in plans[i]:
				# 	annotated += 'The result is then filtered by [{}]. '.format(plans[i]['Filter'])
			if strategy == "Plain":
				annotation = "The Aggregate operation will be performed.\n"
			if strategy == "Hashed":
				annotation = f"The Aggregate operation will hash the rows based on keys {node.attributes['Group Key']}. The selected rows are then returned.\n "
			node.annotations += annotation

		if nodeType == "Sort":
			annotation = f"Sort the table based on the key {node.attributes['Sort Key']}.\n"
			if "INC" in node.attributes['Sort Key']:
				annotation += 'in an incremental manner.\n'
			if "DESC" in node.attributes['Sort Key']:
				annotation += 'in a decremental manner.\n'
			node.annotations += annotation

		if nodeType == "Unique":
			annotation = "Duplicates are removed from the table.\n"
			node.annotations += annotation

		if nodeType == "Gather":
			annotation = "Gather operation is performed on the table.\n"
			node.annotations += annotation

		if nodeType == "Gather Merge":
			annotation = "Gather Merge operation is performed.\n"
			node.annotations += annotation

		if nodeType == "Append":
			annotation = "Append Tables.\n"
			node.annotations += annotation

		# i dont think theres select and project...?
		if nodeType == "Select":
			annotation = "Tuples fulfilling the conditions are selected.\n"
			node.annotations += annotation

		if nodeType == "Project":
			annotation = "Unnecessary elements are removed and the remaining elements are projected.\n"
			node.annotations += annotation

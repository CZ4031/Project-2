class Annotation:
	def traverseTree(self, root):
		if not root:
			return
		
		self.generateAnnotation(root)

		if root.children:
			for child in root.children:
				self.traverseTree(child)

	def comparison(self, node):
		if not node.alternate_scan_dict:
			for altScan in node.alternate_scan_dict:
				annotation = f"Compared to {altScan}, {node.attributes['Node Type']} is {node.alternate_scan_dict.get(altScan)} " \
								f"times faster.\n"
				node.annotations.append(annotation)

	def generateAnnotation(self, node):
		nodeType = node.attributes['Node Type']

		# For scans
		if nodeType == "Bitmap Index Scan":
			annotation = "Bitmap index scan is used as multiple indices are constructed for this table.\n"
			node.annotations.append(annotation)
			self.comparison(node)

		if nodeType == "Bitmap Heap Scan":
			annotation = "Bitmap heap scan is used as multiple indices as constructed. A heap is used to " \
							"sort the indices and quickly cut down the number of tuples scanned.\n "
			node.annotations.append(annotation)
			self.comparison(node)

		if nodeType == "Sequential Scan":
			annotation = "Sequential scan is used to read the table as there is no index.\n"
			node.annotations.append(annotation)
			self.comparison(node)

		# For joins
		if nodeType == "Hash Join":
			annotation = "Hash join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n"
			node.annotations.append(annotation)
			self.comparison(node)

		if nodeType == "Merge Join":
			annotation = "Merge join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n"
			node.annotations.append(annotation)
			self.comparison(node)

		if nodeType == "Nested Loop":
			annotation = "Nested Loop join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n"
			node.annotations.append(annotation)
			self.comparison(node)

		# All other operators
		if nodeType == "Hash":
			annotation = "Perform hashing on table.\n"
			node.annotations.append(annotation)

		if nodeType == "Aggregate":
			strategy = node.attributes['Strategy']
			if strategy == "Sorted":
				annotation = "The Aggregate operation will sort the tuples based on the keys [{}].\n".format(node["Group Key"])
				# if "Filter" in plans[i]:
				# 	annotated += 'The result is then filtered by [{}]. '.format(plans[i]['Filter'])
			if strategy == "Plain":
				annotation = "The Aggregate operation will be performed.\n"
			if strategy == "Hashed":
				annotation = "The Aggregate operation will hash the rows based on keys [{}]. The selected rows are then returned.\n".format(node["Group Key"])
			node.annotations.append(annotation)

		if nodeType == "Sort":
			annotation = "Sort the table based on the key {}.\n".format(node['Sort Key'])
			if "INC" in node["Sort Key"]:
				annotation += 'in an incremental manner.\n'
			if "DESC" in node["Sort Key"]:
				annotation += 'in a decremental manner.\n'
			node.annotations.append(annotation)

		if nodeType == "Unique":
			annotation = "Duplicates are removed from the table.\n"
			node.annotations.append(annotation)

		if nodeType == "Gather":
			annotation = "Gather operation is performed on the table.\n"
			node.annotations.append(annotation)

		if nodeType == "Gather Merge":
			annotation = "Gather Merge operation is performed.\n"
			node.annotations.append(annotation)

		if nodeType == "Append":
			annotation = "Append Tables.\n"
			node.annotations.append(annotation)

		# i dont think theres select and project...?
		if nodeType == "Select":
			annotation = "Tuples fulfilling the conditions are selected.\n"
			node.annotations.append(annotation)

		if nodeType == "Project":
			annotation = "Unnecessary elements are removed and the remaining elements are projected.\n"
			node.annotations.append(annotation)

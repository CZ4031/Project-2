class Annotation:
	def traverseTree(self, root):
		if not root:
			return
		
		self.generateAnnotation(root)

		if root.children:
			for child in root.children:
				self.traverseTree(child)

	def generateAnnotation(self, node):
		for attribute in node.attributes:
			attributeStr = attribute.lower()
			annotation = ""
			# Add basic explanations for scans
			if attributeStr.contains("scan"):
				if attributeStr.contains("bitmap"):
					if attributeStr.contains("index"):
						annotation = "Bitmap index scan is used as multiple indices are constructed for this table.\n"
					else:
						annotation = "Bitmap heap scan is used as multiple indices as constructed. A heap is used to " \
									 "sort the indices and quickly cut down the number of tuples scanned.\n "
				elif attributeStr.contains("index"):
					annotation = "Index scan is used to read the table as an index is constructed.\n"
				elif attributeStr.contains("hash"):
					annotation = "Hash scan is used to read the table as there are many unique values on the attribute " \
								 "used to generate the index.\n"
				else:
					annotation = "Sequential scan is used to read the table as there is no index.\n"
				node.annotations.append(annotation)

				# Add comparison
				if not node.alternate_scan_dict:
					for altScan in node.alternate_scan_dict:
						annotation = f"Compared to {altScan}, {attribute} is {node.alternate_scan_dict.get(altScan)} " \
									 f"times faster.\n"
						node.annotations.append(annotation)

			# need to format all the below cases, for now is static
			# Add explanations for joins
			elif attributeStr.contains("join"):
				if attribute.contains("Hash"):
					annotation = "Hash join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n" 

				elif attribute.contains("Merge"):
					annotation = "Merge join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n"

				elif attribute.contains("Nested Loop"):
					annotation = "Nested Loop join is done on tables XX and YY on the conditions AA, to get resulting table BB.\n"
				node.annotations.append(annotation)

				# Add comparison
				if not node.alternate_scan_dict:
					for altScan in node.alternate_scan_dict:
						annotation = f"Compared to {altScan}, {attribute} is {node.alternate_scan_dict.get(altScan)} " \
									 f"times faster.\n"
						node.annotations.append(annotation)

			# All other operators
			else:
				if attribute.contains("Hash"):
					annotation = "Perform hashing on table.\n"
					node.annotations.append(annotation)

				elif attribute.contains("Aggregate"):
					annotation = "Perform aggregate on the table.\n"
					node.annotations.append(annotation)

				elif attribute.contains("Sort"):
					annotation = "Sort table in an decremental manner.\n"
					node.annotations.append(annotation)

				elif attribute.contains("Incremental Sort"):
					annotation = "Sort table in an incremental manner.\n"
					node.annotations.append(annotation)

				elif attribute.contains("Unique"):
					annotation = "Duplicates are removed from the table.\n"
					node.annotations.append(annotation)

				elif attribute.contains("Gather"):
					annotation = "Gather operation is performed on the table.\n"

				elif attribute.contains("Gather Merge"):
					annotation = "Gather Merge operation is performed.\n"
					node.annotations.append(annotation)

				elif attribute.contains("Append"):
					annotation = "Append tables.\n"

				elif attributeStr.contains("select"):
					annotation = "Tuples fulfilling the conditions are selected.\n"

				elif attributeStr.contains("project"):
					annotation = "Unnecessary elements are removed and the remaining elements are projected."

				node.annotations.append(annotation)

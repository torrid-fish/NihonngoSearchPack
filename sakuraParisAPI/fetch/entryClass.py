class Entry:
	def __init__ (self, heading, definition, page, offset, accent):
		self._heading = heading
		self._definition = definition
		self._accent = accent
		self._page = page
		self._offset = offset

	def getHeading(self):
		return self._heading

	def getDefinition(self):
		return self._definition
	
	def getAccent(self):
		return self._accent

	def getPage(self):
		return self._page

	def getOffset(self):
		return self._offset
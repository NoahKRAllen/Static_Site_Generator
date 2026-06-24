class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError("Not yet implemented")

	def props_to_html(self):
		if self.props == None or self.props == "":
			return ""
		return_string = ""
		first_prop = True
		for attr in self.props:
			if attr is None:
				continue
			if not first_prop:
				return_string += " "
			else:
				first_prop = False
			return_string += (f"{attr}=\"{self.props[attr]}\"")
		return return_string

	def __eq__(self, other):
		return(
			self.tag == other.tag and
			self.value == other.value and
			self.children == other.children and
			self.props == other.props)

	def __repr__(self):
		return f"HTML Node(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__
		self.tag = tag
		self.value = value
		self.props = props

	def to_html(self):
		if self.value == None:
			raise ValueError("All leaf nodes require a value")
		if self.tag == None or self.tag == "":
			return self.value
		if self.props == None:
			return f"<{self.tag}>{self.value}</{self.tag}>"
		return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
	def __eq__(self, other):
		return(
			self.tag == other.tag and
			self.value == other.value and
			self.props == other.props)

	def __repr__(self):
		return f"Leaf Node(Tag: {self.tag}, Value: {self.value}, Props: {self.props})"


class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__
		self.tag = tag
		self.children = children
		self.props = props

	def to_html(self):
		if not self.tag:
			raise ValueError("All parent nodes require a tag")
		if not self.children:
			raise ValueError("All parent nodes require children")
		html_string = f"<{self.tag}"
		if self.props:
			html_string += " "
			html_string += f"{self.props_to_html()}"
		html_string += ">"
		for child in self.children:
			html_string += child.to_html()
		html_string += f"</{self.tag}>"
		return html_string

	def __eq__(self, other):
		return(
			self.tag == other.tag and
			self.children == other.children and
			self.props == other.props)

	def __repr__(self):
		return f"Parent Node(Tag: {self.tag}, Children: {self.children}, Props: {self.props}"

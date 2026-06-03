
class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImpletementedError("Not yet implemented")

	def props_to_html(self):
		if self.props == None or self.props == "":
			return ""
		return_string = ""
		for attr in self.props:
			if attr is None:
				continue
			return_string += (f'{attr}="{self.props[attr]}" ')
		return return_string

	def __repr__(self):
		return f"HTML Node(Tag:{self.tag},Value:{self.value},Children:{self.children},Props:{self.props})" 

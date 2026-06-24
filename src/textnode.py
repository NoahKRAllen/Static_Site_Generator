from enum import Enum
from htmlnode import LeafNode
class TextType(Enum):
	TEXT = ""
	BOLD = "** **"
	ITALIC = "_ _"
	CODE = "` `"
	LINK = "[]()"
	IMAGE = "![]()"

class TextNode:

	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		return(
			self.text == other.text and
			self.text_type == other.text_type and
			self.url == other.url)
	def __repr__(self):
		return f"Text Node({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
	if text_node.text_type not in TextType:
		raise Exception("Non-valid text type")
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
		case _:
			raise Exception("Non-valid text type in match statement")
	return 0

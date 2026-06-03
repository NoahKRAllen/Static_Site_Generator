import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_noteq(self):
		node = TextNode("This is a text node", TextType.BOLD, "BLANK")
		node2 = TextNode("This is a node", TextType.CODE, "URL")
		self.assertNotEqual(node, node2)

	def test_urlnone(self):
		node = TextNode("This is a text node", TextType.LINK, None)
		node2 = TextNode("This is a text node", TextType.LINK)
		self.assertEqual(node, node2)

	def test_stringnotequal(self):
		node = TextNode("This is a text node", TextType.TEXT)
		node2 = TextNode("This isn't a text node", TextType.TEXT)
		self.assertNotEqual(node, node2)

	def test_urlequal(self):
		node = TextNode("", TextType.LINK, "URL")
		node2 = TextNode("", TextType.LINK, "URL")
		self.assertEqual(node, node2)

	def test_typenone(self):
		node = TextNode("Text node", TextType.TEXT)
		node2 = TextNode("Text node", None)
		self.assertNotEqual(node, node2)


if __name__ == "__main__":
	unittest.main()

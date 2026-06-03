import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node = HTMLNode("Tag", "Value", "Children", "Props")
		node2 = HTMLNode("Tag", "Value", "Children", "Props")
		self.assertEqual(node, node2)

	def test_noteq(self):
		node = HTMLNode("Tag", "Value", "Children", "Props")
		node2 = HTMLNode("Tagged", "Value", "Children", "Props")
		self.assertNotEqual(node, node2)

	def test_nones(self):
		node = HTMLNode()
		node2 = HTMLNode(None, None, None, None)
		self.assertEqual(node, node2)

	def test_props_to_html_equal(self):
		node = HTMLNode(None, None, None, {"href": "https://www.grubhub.com", "target": "_blank"})
		node_props = node.props_to_html()
		node2 = HTMLNode(None, None, None, {"href": "https://www.grubhub.com", "target": "_blank"})
		node2_props = node2.props_to_html()
		self.assertEqual(node_props, node2_props)

	def test_props_to_html_None(self):
		node = HTMLNode(None, None, None, None)
		node_props = node.props_to_html()
		node2 = HTMLNode()
		node2_props = node2.props_to_html()
		self.assertEqual(node_props, node2_props)

	def test_props_to_html_not_equal(self):
		node = HTMLNode(None, None, None, {"href": "https://www.grubhub.com", "target": "_blank"})
		node_props = node.props_to_html()
		node2 = HTMLNode(None, None, None, {"href": "https://www.subhub.com", "target": "_blank"})
		node2_props = node2.props_to_html()
		self.assertNotEqual(node_props, node2_props)

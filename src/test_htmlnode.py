import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
import textnode

class TestHTMLNode(unittest.TestCase):
	#HTML Node Tests
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
		self.assertEqual(node_props, "href=\"https://www.grubhub.com\" target=\"_blank\"")

	def test__props_to_html(self):
		node = HTMLNode(None, None, None, {"href": "https://www.grubhub.com", "target": "_blank"})
		node_props = node.props_to_html()
		self.assertEqual(node_props, "href=\"https://www.grubhub.com\" target=\"_blank\"")

	def test_props_to_html_None(self):
		node = HTMLNode(None, None, None, None)
		node_props = node.props_to_html()
		self.assertEqual(node_props, "")

	def test_props_to_html_not_equal(self):
		node = HTMLNode(None, None, None, {"href": "https://www.grubhub.com", "target": "_blank"})
		node_props = node.props_to_html()
		self.assertNotEqual(node_props, "href=\"https://www.subhub.com\" target=\"_blank\"")

class TestLeafNode(unittest.TestCase):
	#Leaf Node Tests
	def test_leaf_to_html_p(self):
		node = LeafNode("a", "Leaf")
		self.assertEqual(node.to_html(), "<a>Leaf</a>")

	def test_leaf_props_to_html(self):
		node = LeafNode("a", "Leaf", {"link": "_blank"})
		self.assertEqual(node.to_html(), "<a link=\"_blank\">Leaf</a>")

	def test_leaf_node_none(self):
		node = LeafNode("a", "Leaf", None)
		node2 = LeafNode("a", "Leaf")
		self.assertEqual(node, node2)

	def test_leaf_node_no_tag(self):
		node = LeafNode(None, "Leaf").to_html()
		self.assertEqual(node, "Leaf")

class TestParentNode(unittest.TestCase):
	#Parent Node Tests
	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(),	"<div><span><b>grandchild</b></span></div>")

	def test_to_html_multiple_children(self):
		child_node_1 = LeafNode("span", "child1")
		child_node_2 = LeafNode("span", "child2")
		parent_node = ParentNode("div", [child_node_1, child_node_2])
		self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>")

	def test_to_html_multiple_parent_same_child(self):
		grandchild_node = LeafNode("a", "child")
		child_node_1 = ParentNode("span", [grandchild_node])
		child_node_2 = ParentNode("b", [grandchild_node])
		parent_node = ParentNode("div", [child_node_1, child_node_2])
		self.assertEqual(parent_node.to_html(),	"<div><span><a>child</a></span><b><a>child</a></b></div>")

	def test_to_html_parent_props(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("a", [child_node], {"href": "https://www.grubhub.com"})
		self.assertEqual(parent_node.to_html(),	"<a href=\"https://www.grubhub.com\"><span>child</span></a>")

	def test_to_html_multiple_parent_props(self):
		grandchild_node_1 = LeafNode("div", "first_leaf")
		grandchild_node_2 = LeafNode("div", "second_leaf")
		child_node_1 = ParentNode("span", [grandchild_node_1], {"href": "https://www.grubhub.com"})
		child_node_2 = ParentNode("span", [grandchild_node_2], {"target": "_blank"})
		parent_node = ParentNode("div", [child_node_1, child_node_2], {"final": "space"})
		self.assertEqual(parent_node.to_html(), "<div final=\"space\"><span href=\"https://www.grubhub.com\"><div>first_leaf</div></span><span target=\"_blank\"><div>second_leaf</div></span></div>")

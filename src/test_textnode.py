import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline import (
	split_nodes_delimiter, extract_markdown_images, extract_markdown_urls, split_nodes_image, split_nodes_url, text_to_textnodes, markdown_to_html_node, extract_title
)
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

class TestTextNodeToHTMLNode(unittest.TestCase):
	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_bold(self):
		node = TextNode("This is a bold text node", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a bold text node")

	def test_italic(self):
		node = TextNode("This is an italic text node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is an italic text node")

	def test_code(self):
		node = TextNode("This is a code text node", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is a code text node")

	def test_link(self):
		node = TextNode("This is a link node", TextType.LINK, "https://www.grubhub.com")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "This is a link node")
		self.assertEqual(html_node.props, {"href" : "https://www.grubhub.com"})

	def test_image(self):
		node = TextNode("This is an image node", TextType.IMAGE, "d:/desktop/pictureofacateating")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.props, {"src":"d:/desktop/pictureofacateating", "alt":"This is an image node"})

class TestSplitNode(unittest.TestCase):
	def test_base_split(self):
		node = TextNode("This is a **text** node", TextType.TEXT)
		split_node = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(split_node, [TextNode("This is a ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" node", TextType.TEXT)])

	def test_multi_split(self):
		node = TextNode("This is a **multiple** split **node**", TextType.TEXT)
		split_node = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(split_node,
			[TextNode("This is a ", TextType.TEXT), TextNode("multiple", TextType.BOLD), TextNode(" split ", TextType.TEXT), TextNode("node", TextType.BOLD)])

	def test_multiple_nodes(self):
		node_1 = TextNode("This is a text **node**", TextType.TEXT)
		node_2 = TextNode("This is also a text **node**", TextType.TEXT)
		split_node = split_nodes_delimiter([node_1, node_2], "**", TextType.BOLD)
		self.assertEqual(split_node,
			[TextNode("This is a text ", TextType.TEXT), TextNode("node", TextType.BOLD),
				TextNode("This is also a text ", TextType.TEXT), TextNode("node", TextType.BOLD)])
	def test_multi_delimiters(self):
		node = TextNode("This is a `text` **node**", TextType.TEXT)
		split_node = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(split_node, [TextNode("This is a ", TextType.TEXT), TextNode("text", TextType.CODE), TextNode(" **node**", TextType.TEXT)])
		split_node = split_nodes_delimiter(split_node, "**", TextType.BOLD)
		self.assertEqual(split_node, [TextNode("This is a ", TextType.TEXT), TextNode("text", TextType.CODE), TextNode(" ", TextType.TEXT), TextNode("node", TextType.BOLD)])

	def test_wrong_texttype(self):
		node = TextNode("This is a code node", TextType.CODE)
		split_node = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(split_node, [node])

	def test_start_with_delimiter(self):
		node = TextNode("**This is** a text node", TextType.TEXT)
		split_node = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(split_node, [TextNode("This is", TextType.BOLD), TextNode(" a text node", TextType.TEXT)])

	def test_empty_list(self):
		split_node = split_nodes_delimiter([], "**", TextType.BOLD)
		self.assertEqual(split_node, [])

	def test_invalid_markdown(self):
		with self.assertRaises(Exception):
			node = TextNode("This is a text **node", TextType.TEXT)
			split_node = split_nodes_delimiter([node], "**", TextType.BOLD)

	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_urls(self):
		matches = extract_markdown_urls("This is text with a [link](https://www.grubhub.com)")
		self.assertListEqual([("link", "https://www.grubhub.com")], matches)

	def test_incorrect_regex(self):
		matches = extract_markdown_images(
			"This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertNotEqual(["image", "https://i.imgur.com/zjjcJKZ.png"], matches)

	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
			],
			new_nodes,
		)

	def test_split_images_wrong(self):
		node = TextNode("This is a text with no image", TextType.TEXT)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is a text with no image", TextType.TEXT)
			],
			new_nodes,
		)

	def test_split_images_multiple_nodes(self):
		node_1 = TextNode("This is a text with an ![image](https://i.imgur.com/FirstImage) and another ![second image](https://i.imgur.com/SecondImage)",
			 TextType.TEXT)
		node_2 = TextNode("This is the second text with an ![image](https://i.imgur.com/FirstImageSecond) and another ![second image](https://i.imgur.com/SecondImageSecond)",
			TextType.TEXT)
		new_nodes = split_nodes_image([node_1, node_2])
		self.assertListEqual(
			[
				TextNode("This is a text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/FirstImage"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second image", TextType.IMAGE, "https://i.imgur.com/SecondImage"),
				TextNode("This is the second text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/FirstImageSecond"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second image", TextType.IMAGE, "https://i.imgur.com/SecondImageSecond"),
			],
			new_nodes,
		)

	def test_split_urls(self):
		node = TextNode(
			"This is text with an [url](https://i.imgur.com) and another [second url](https://i.imgur.com)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_url([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("url", TextType.LINK, "https://i.imgur.com"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second url", TextType.LINK, "https://i.imgur.com"),
			],
			new_nodes,
		)

	def test_split_urls_wrong(self):
		node = TextNode("This is a text with no url", TextType.TEXT)
		new_nodes = split_nodes_url([node])
		self.assertListEqual(
			[
				TextNode("This is a text with no url", TextType.TEXT)
			],
			new_nodes,
		)

	def test_split_urls_multiple_nodes(self):
		node_1 = TextNode("This is a text with a [url](https://i.imgur.com) and another [second url](https://i.imgur.com)",
			 TextType.TEXT)
		node_2 = TextNode("This is the second text with a [url](https://i.imgur.com/Second) and another [second url](https://i.imgur.com/SecondSecond)",
			TextType.TEXT)
		new_nodes = split_nodes_url([node_1, node_2])
		self.assertListEqual(
			[
				TextNode("This is a text with a ", TextType.TEXT),
				TextNode("url", TextType.LINK, "https://i.imgur.com"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second url", TextType.LINK, "https://i.imgur.com"),
				TextNode("This is the second text with a ", TextType.TEXT),
				TextNode("url", TextType.LINK, "https://i.imgur.com/Second"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second url", TextType.LINK, "https://i.imgur.com/SecondSecond"),
			],
			new_nodes,
		)

	def test_text_to_textnodes(self):
		node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		new_node = text_to_textnodes(node)
		self.assertListEqual(
			[
				TextNode("This is ", TextType.TEXT),
				TextNode("text", TextType.BOLD),
				TextNode(" with an ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
				TextNode(" word and a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
				TextNode(" and an ", TextType.TEXT),
				TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
				TextNode(" and a ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://boot.dev"),
			],
			new_node,
		)

	def test_text_to_textnodes_no_urls(self):
		node = "This is **text** with an _italic_ word and a `code block`"
		new_node = text_to_textnodes(node)
		self.assertListEqual(
			[
				TextNode("This is ", TextType.TEXT),
				TextNode("text", TextType.BOLD),
				TextNode(" with an ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
				TextNode(" word and a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
			],
			new_node,
		)

	def test_text_to_textnodes_only_urls(self):
		node = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://boot.dev)"
		new_node = text_to_textnodes(node)
		self.assertListEqual(
			[
				TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
				TextNode("link", TextType.LINK, "https://boot.dev"),
			],
			new_node,
		)

	def test_text_to_textnodes_nothing(self):
		node = ""
		new_node = text_to_textnodes(node)
		self.assertListEqual(
			[],
			new_node,
		)

	def test_paragraphs_to_html(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
		)


	def test_code_to_html(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
		)

	def test_heading_to_html(self):
		md = """
# Heading One

## Heading Two

#### Heading Four
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h1>Heading One</h1><h2>Heading Two</h2><h4>Heading Four</h4></div>",
		)

	def test_quote_to_html(self):
		md = """
> Quote One
> Quote Two
> Quote Three
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><blockquote>Quote One Quote Two Quote Three</blockquote></div>",
		)

	def test_ordered_list_to_html(self):
		md = """
1. One
2. Two
3. Three
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ol><li>One</li><li>Two</li><li>Three</li></ol></div>",
		)

	def test_unordered_list_to_html(self):
		md = """
- One
- Two
- Three
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ul><li>One</li><li>Two</li><li>Three</li></ul></div>",
		)

	def test_extract_title(self):
		md = "# Heading 1"
		title = extract_title(md)
		self.assertEqual(
			title,
			"Heading 1",
		)

	def test_bad_extract_title(self):
		md = "#Heading 1"
		with self.assertRaises(Exception) as context:
			extract_title(md)
		self.assertEqual(str(context.exception), "No h1 header present")

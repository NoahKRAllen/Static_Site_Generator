from textnode import TextNode, TextType
from block import Blocks, BlockType
from textnode import text_node_to_html_node
from htmlnode import ParentNode
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
	new_nodes = list()
	for node in old_nodes:
		if node.text == "":
			continue
		if node.text_type is not TextType.TEXT:
			new_nodes.append(node)
			continue
		split_node_text = node.text.split(delimiter)
		if len(split_node_text) % 2 == 0:
			raise Exception(f"Invalid markdown syntax attempted on TextNode: {node} using delimiter: {delimiter}")
		even_index = True
		for new_node_text in split_node_text:
			if new_node_text == "":
				even_index = not even_index
				continue
			if even_index:
				even_index = not even_index
				new_nodes.append(TextNode(new_node_text, TextType.TEXT))
				continue
			even_index = not even_index
			new_nodes.append(TextNode(new_node_text, text_type))
	return new_nodes

def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_urls(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes = []
	#Old Nodes example: ["Blah ![image_alt](image_link) Blah ![image_alt_2](image_link_2)", TextType.TEXT]
	for node in old_nodes:
		string_to_split = node.text
		split_nodes = []

		#Should give us [["image_alt", "image_link"], ["image_alt_2", "image_link_2"]
		extracted_imgs = extract_markdown_images(string_to_split)

		for img_alt, img_link in extracted_imgs:
			#This should leave us with ["Blah ", " Blah", " "]
			split_string = string_to_split.split(f"![{img_alt}]({img_link})", 1)
			#This will add the tuple of ["Blah ", TextType.TEXT] to new_nodes
			#Skips this in cases like "![image_alt](image_link)".split(f"![{image_alt}](image_link)") which would return ["", ""]
			if split_string[0] != "":
				new_nodes.append(TextNode(split_string[0], TextType.TEXT))
			#Now we need to take img_alt and img_link and make the second tuple to add, with [img_alt, TextType.IMAGE, img_link]
			new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_link))
			#Finally, swap string_to_split to equal split_string[1] which is " Blah"
			string_to_split = split_string[1]
			#The loop will continue until we are through all the extracted_imgs that extract_markdown_image found
		#Catches last split to add to new_nodes, supposed to stop any non-image nodes from being caught
		if string_to_split != "":
			new_nodes.append(TextNode(string_to_split, node.text_type, node.url))
	if new_nodes == []:
		return old_nodes
	return new_nodes

def split_nodes_url(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		string_to_split = node.text
		split_nodes = []

		extracted_urls = extract_markdown_urls(string_to_split)

		for url_title, url in extracted_urls:
			split_string = string_to_split.split(f"[{url_title}]({url})", 1)
			if split_string[0] != "":
				new_nodes.append(TextNode(split_string[0], TextType.TEXT))
			new_nodes.append(TextNode(url_title, TextType.LINK, url))
			string_to_split = split_string[1]
		if string_to_split != "":
			new_nodes.append(TextNode(string_to_split, node.text_type, node.url))
	if new_nodes == []:
		return old_nodes
	return new_nodes


def text_to_textnodes(text):
	new_nodes = [TextNode(text, TextType.TEXT)]
	new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
	new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
	new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
	new_nodes = split_nodes_image(new_nodes)
	new_nodes = split_nodes_url(new_nodes)
	return new_nodes


def markdown_to_html_node(markdown):
	text_blocks = Blocks.markdown_to_blocks(markdown)
	html_nodes = []
	for text_block in text_blocks:
		block_type = Blocks.block_to_block_type(text_block)

		match block_type:
			case BlockType.PARAGRAPH:
				html_nodes.append(paragraph_to_html_node(text_block))
			case BlockType.CODE:
				html_nodes.append(code_to_html_node(text_block))
			case BlockType.HEADING:
				html_nodes.append(heading_to_html_node(text_block))
			case BlockType.QUOTE:
				html_nodes.append(quote_to_html_node(text_block))
			case BlockType.ORDERED_LIST:
				html_nodes.append(ordered_list_to_html_node(text_block))
			case BlockType.UNORDERED_LIST:
				html_nodes.append(unordered_list_to_html_node(text_block))
			case _:
				raise Exception("Invalid BlockType passed into markdown_to_html_node")
	return ParentNode("div", html_nodes)

def text_to_children(unsyntaxed_text):
	text_nodes = text_to_textnodes(unsyntaxed_text)
	child_nodes = []
	for node in text_nodes:
		child_nodes.append(text_node_to_html_node(node))
	return child_nodes

def paragraph_to_html_node(paragraph_text):
	trimmed_text = paragraph_text.replace("\n", " ")
	html_children = text_to_children(trimmed_text)
	return ParentNode("p", html_children)

def code_to_html_node(code_text):
	trimmed_text = code_text[4:-3]
	node = TextNode(trimmed_text, TextType.TEXT)
	leaf_node = text_node_to_html_node(node)
	code_node = ParentNode("code", [leaf_node])
	return ParentNode("pre", [code_node])

def heading_to_html_node(heading_text):
	symbol_count = 0
	for char in heading_text:
		if char != "#":
			break
		symbol_count += 1
	tag = f"h{symbol_count}"
	trimmed_text = heading_text[symbol_count + 1:]
	html_children = text_to_children(trimmed_text)
	return ParentNode(tag, html_children)

def quote_to_html_node(quote_text):
	quotes = quote_text.split("\n")
	trimmed_text = ""
	for quote in quotes:
		quote = quote[2:]
		trimmed_text += quote + " "
	trimmed_text = trimmed_text.strip()
	html_children = text_to_children(trimmed_text)
	return ParentNode("blockquote", html_children)

def individual_list_line_helper(block_list_text):
	split_list = block_list_text.split("\n")
	parents = []
	for line in split_list:
		split_line = line.split(" ", 1)
		children = text_to_children(split_line[1])
		parents.append(ParentNode("li", children))
	return parents

def ordered_list_to_html_node(ordered_list_text):
	children = individual_list_line_helper(ordered_list_text)
	return ParentNode("ol", children)

def unordered_list_to_html_node(unordered_list_text):
	children = individual_list_line_helper(unordered_list_text)
	return ParentNode("ul", children)

def extract_title(markdown):
	if markdown.startswith("# "):
		return markdown[2:].strip()
	else:
		raise Exception("No h1 header present")

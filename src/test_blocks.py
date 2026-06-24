import unittest
from block import Blocks, BlockType

class TestBlock(unittest.TestCase):
	def test_markdown_to_blocks(self):
		markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = Blocks.markdown_to_blocks(markdown)
		self.assertEqual(
			blocks,
			[
				"This is **bolded** paragraph",
				"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
				"- This is a list\n- with items",
			],
		)

	def test_block_to_block_heading(self):
		markdown = "### This is a Heading Markdown"
		block_type = Blocks.block_to_block_type(markdown)
		self.assertEqual(block_type, BlockType.HEADING)

	def test_block_to_block_code(self):
		markdown = "```\nCode is here\n```"
		block_type = Blocks.block_to_block_type(markdown)
		self.assertEqual(block_type, BlockType.CODE)

	def test_block_to_block_quote(self):
		markdown = "> Quote is here"
		block_type = Blocks.block_to_block_type(markdown)
		self.assertEqual(block_type, BlockType.QUOTE)

	def test_block_to_block_unordered(self):
		markdown = "- Unordered\n- List\n- Here"
		block_type = Blocks.block_to_block_type(markdown)
		self.assertEqual(block_type, BlockType.UNORDERED_LIST)

	def test_block_to_block_ordered(self):
		markdown = "1. Ordered\n2. List\n3. Here"
		block_type = Blocks.block_to_block_type(markdown)
		self.assertEqual(block_type, BlockType.ORDERED_LIST)

	def test_block_to_block_paragraph(self):
		markdown = "Basic Paragraph here"
		block_type = Blocks.block_to_block_type(markdown)
		self.assertEqual(block_type, BlockType.PARAGRAPH)

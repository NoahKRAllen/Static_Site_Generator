from enum import Enum


class BlockType(Enum):
	HEADING = "#"
	CODE = "```"
	QUOTE = "> "
	UNORDERED_LIST = "- "
	ORDERED_LIST = "#. "
	PARAGRAPH = ""

class Blocks:

	def markdown_to_blocks(markdown):
		split_blocks = markdown.split("\n\n")
		final_blocks = []
		for temp_block in split_blocks:
			if temp_block != "":
				block = temp_block.strip()
				final_blocks.append(block)
		return final_blocks


	def block_to_block_type(markdown_text: str):
		#Heading blocks will start with 1-6 '#' characters followed by a space and then the text
		if markdown_text.startswith("#"):
			prev_char = ""
			symbol_count = 0
			for char in markdown_text:
				if char != "#" and char != " ":
					break
				if char == " " and prev_char == "#" and 1 <= symbol_count <= 6:
					return BlockType.HEADING
				prev_char = char
				symbol_count += 1

		#Code blocks start with ``` and \n and then end with ```
		if markdown_text.startswith("```\n") and markdown_text.endswith("\n```"):
			return BlockType.CODE

		#Quote blocks always start with '>' followed by the text. A space is not required but is sometimes added
		correct_quote_marking = False
		for line in markdown_text.splitlines():
			if not line.startswith(">"):
				correct_quote_marking = False
				break
			correct_quote_marking = True
		if correct_quote_marking:
			return BlockType.QUOTE
		#Unordered list blocks must start every line with '- '
		correct_ulist_marking = False
		for line in markdown_text.splitlines():
			if not line.startswith("- "):
				correct_ulist_marking = False
				break
			correct_ulist_marking = True
		if correct_ulist_marking:
			return BlockType.UNORDERED_LIST
		#Ordered list blocks must start every line with a number followed by '. ' The numbers must start at 1, and increment by 1 every line
		correct_list_marking = False
		current_num = 1
		for line in markdown_text.splitlines():
			if not line.startswith(f"{current_num}. "):
				correct_list_marking = False
				break
			correct_list_marking = True
			current_num += 1
		if correct_list_marking:
			return BlockType.ORDERED_LIST
		#If all checks fail, then the block is a paragraph block
		return BlockType.PARAGRAPH

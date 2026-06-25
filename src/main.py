from textnode import TextNode, TextType
from inline import extract_title, markdown_to_html_node

import shutil
import os
import pathlib
def main():
	delete_remake_public_dir('public')
	copy_dir_to_dir('static', 'public')
	generate_pages_recursive("content", "template.html", "public")


def delete_remake_public_dir(dir_path):
	shutil.rmtree(dir_path)
	os.makedirs(dir_path, exist_ok=True)

def copy_dir_to_dir(copy, target):
	items = os.listdir(copy)
	for item in items:
		copy_path = os.path.join(copy, item)
		destination_path = os.path.join(target, item)
		if os.path.isfile(copy_path):
			shutil.copy(copy_path, target)
			#This does return the path of the copied file, if needed in debugging
		elif os.path.isdir(copy_path):
			os.makedirs(destination_path, exist_ok=True)
			copy_dir_to_dir(copy_path, destination_path)

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	markdown_data = None
	template_data = None
	with open(from_path, 'r', encoding="utf-8") as f:
		markdown_data = f.read()
	with open(template_path, 'r', encoding="utf-8") as f:
		template_data = f.read()
	markdown_html_content = markdown_to_html_node(markdown_data).to_html()
	title = extract_title(markdown_data)
	template_updated = template_data.replace("{{ Title }}", title)
	template_updated = template_updated.replace("{{ Content }}", markdown_html_content)
	dirname = os.path.dirname(dest_path)
	if dirname != "":
		os.makedirs(dirname, exist_ok=True)
	with open(dest_path, 'w', encoding="utf-8") as f:
		f.write(template_updated)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	dir_list = os.listdir(dir_path_content)
	for item in dir_list:
		from_path = os.path.join(dir_path_content, item)
		dest_path = os.path.join(dest_dir_path, item)
		if os.path.isfile(from_path):
			path = pathlib.Path(dest_path)
			dest_path = path.with_suffix(".html")
			generate_page(from_path, template_path, dest_path)
		else:
			generate_pages_recursive(from_path, template_path, dest_path)

if __name__ == "__main__":
	main()


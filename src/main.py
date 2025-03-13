from pathlib import Path
from gencontent import generate_pages_recursive
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode,ParentNode
from markdown_blocks import markdown_to_blocks, markdown_to_html_node
from copystatic import copy_content
import sys


dest_dir_path = r"./docs"
src_dir_path = r"./static"
markdown_path = r"./content"
default_basepath = "/"
index_path = r"./template.html"

def main():
    basepath = default_basepath
    if len(sys.argv) >1:
        basepath = sys.argv[1]
    copy_content(destination=dest_dir_path, source= src_dir_path)
    generate_pages_recursive(
        dir_path_content=markdown_path,
        template_path=index_path,
        dest_dir_path=dest_dir_path,
        basepath = basepath)

    
    



main()

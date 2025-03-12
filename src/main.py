from pathlib import Path
from gencontent import generate_pages_recursive
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode,ParentNode
from markdown_blocks import markdown_to_blocks, markdown_to_html_node
from copystatic import copy_content
import os

print("Hello world")

def main():
    textNode = TextNode(
        "This is some anchor text", 
        text_type= TextType.LINKS, url = "https://www.boot.dev")
    text = textNode.__repr__()
    print(text)
    
    dest_dir_path = r"./public"
    src_dir_path = r"./static"
    markdown_path = r"./content"
    index_path = r"./template.html"
    copy_content(destination=dest_dir_path, source= src_dir_path)
    generate_pages_recursive(
        content_dir=markdown_path,
        template_path=index_path,
        output_dir=dest_dir_path)

    
    



main()

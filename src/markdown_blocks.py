from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered list'
    ORDERED_LIST = 'ordered list'


def markdown_to_blocks(markdown)-> list:
    
    inline_markdowns = markdown.split("\n\n")
    results = []
    for line in inline_markdowns:
        if line.strip() !="":
            results.append(line.strip())

    return results

def block_to_block_type(block) -> BlockType:
    
    starting_char = block[0]
    lines = block.split("\n")
    
    if starting_char == "#":
        for i in range(1,6):
            if block[i] == "#":
                continue
            if block[i] == " ": 
                return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE    
    if starting_char == ">":
        boolean = False
        for line in lines:
            if line.startswith(">"):
                boolean = True
            else: 
                boolean = False
        if boolean: 
            return BlockType.QUOTE   
        
    
    if starting_char == "-":
        boolean = False
        for line in lines:
            if line.startswith("- "):
                boolean = True
            else: 
                boolean = False
        if boolean: 
            return BlockType.UNORDERED_LIST   
    if starting_char.isnumeric():
        number = 1
        boolean = False
        for line in lines:
            
            if line.startswith(f"{number}. "):
                number += 1
                boolean = True
        
        if boolean:
            return BlockType.ORDERED_LIST   
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    
    child_nodes = []
    
    # creates blocks 
    for block in blocks:
        node = block_to_html_node(block=block)
        child_nodes.append(node)
    
    return ParentNode("div", child_nodes, None)

    


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")
        

def text_to_children(text) -> list:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
    
def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
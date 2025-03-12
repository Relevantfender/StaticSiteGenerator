from textnode import TextNode, TextType
from htmlnode import HTMLNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text) -> list:
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text) -> list:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)



def split_nodes_image(old_nodes):
    new_nodes=[]
    for old_node in old_nodes:
        matches = extract_markdown_images(old_node.text)
    
        if not matches:
            new_nodes.append(old_node)
            continue
        sections = []
        node_text = old_node.text
        
        for match in matches:
            sections = node_text.split(f"![{match[0]}]({match[1]})",1)
            
            if len(sections)==1:
                new_image_node = TextNode(text=match[0], text_type=TextType.IMAGES, url=match[1])
                continue
            
            if sections[0]!="":
                new_text_node = TextNode(text=sections[0], text_type=TextType.TEXT)
                new_nodes.append(new_text_node)
            new_image_node = TextNode(text=match[0], text_type=TextType.IMAGES, url=match[1])
            new_nodes.append(new_image_node)
            node_text = sections[1]

      
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINKS, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes 
  
        
    
def text_to_textnodes(text) -> list:
    text_node = TextNode(text=text, text_type= TextType.TEXT)
    image_nodes = split_nodes_image([text_node])
    link_nodes = split_nodes_link(image_nodes)
    italic_nodes = split_nodes_delimiter(link_nodes,"_",TextType.ITALIC)
    bold_nodes = split_nodes_delimiter(italic_nodes,"**",TextType.BOLD)
    code_nodes = split_nodes_delimiter(bold_nodes, "`",TextType.CODE)
    return code_nodes
    
    
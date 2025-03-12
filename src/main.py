from pathlib import Path
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
    # generate_page(
    #     dest_path=dest_dir_path,
    #     template_path=index_path,
    #     from_path=markdown_path)
    
    
def extract_title(markdown)-> str:
    string = ""
    with open(markdown, "r") as file:
        string = file.readline()
    
    string = string.strip()
    if not string.startswith("# "):
        raise Exception("File should start with a header")
    string = string[2:].strip()
    return string

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path}, using {template_path}")
    
    # Read markdown content
    with open(from_path, "r") as file:
        markdown = file.read()
    
    # Read template
    with open(template_path, "r") as file:
        template = file.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    
    # Extract title
    title = extract_title(from_path)
    
    # Replace placeholders in template
    template = template.replace("{{ title }}", title).replace("{{ content }}", content)
    
    # Properly handle the output path
    if dest_path.endswith('index'):
        # Keep index.html in its original directory
        file_name = dest_path + ".html"
    else:
        # For other files, create a directory with the file's name and put index.html inside
        # This gives us clean URLs like /blog/majesty/ instead of /blog/majesty.html
        file_name = os.path.join(dest_path, "index.html")
    
    # Create directories if they don't exist
    save_dir = os.path.dirname(file_name)
    if not os.path.exists(save_dir):
        print(f"Created destination path directory: {save_dir}")
        os.makedirs(save_dir)
    
    # Write the output file
    with open(file_name, "w", encoding="utf-8") as file:
        result = file.write(template)
        if result > 0:
            print(f"Page with the title \"{title}\" generated successfully")

def generate_pages_recursive(content_dir, template_path, output_dir):
    """
    Recursively process markdown files and generate HTML pages.
    
    Args:
        content_dir: Directory containing markdown files and subdirectories
        template_path: Path to the HTML template file
        output_dir: Directory where generated HTML files should be saved
    """
    
    def process_dir(current_dir, rel_path=""):
        """
        Process a directory, generating HTML for markdown files and recursively
        processing subdirectories.
        
        Args:
            current_dir: Full path to the current directory being processed
            rel_path: Relative path from content_dir to current_dir
        """
        # List all files and directories in the current directory
        items = os.listdir(current_dir)
        
        for item in items:
            # Full path to the current item
            item_path = os.path.join(current_dir, item)
            
            # If it's a directory, process it recursively
            if os.path.isdir(item_path):
                # Calculate the new relative path for the subdirectory
                new_rel_path = os.path.join(rel_path, item)
                process_dir(item_path, new_rel_path)
            
            # If it's a markdown file, generate HTML
            elif item.endswith('.md'):
                # Base filename without extension
                basename = os.path.splitext(item)[0]
                
                # Handle the special case for index.md files
                if basename == 'index':
                    # For index.md, keep the parent directory name
                    dest_dir = os.path.join(output_dir, rel_path)
                    dest_path = os.path.join(dest_dir, basename)
                else:
                    # For other .md files, create a directory based on the filename
                    dest_dir = os.path.join(output_dir, rel_path)
                    dest_path = os.path.join(dest_dir, basename)
                
                # Generate the HTML page
                generate_page(
                    from_path=item_path,
                    template_path=template_path,
                    dest_path=dest_path
                )
    
    # Start processing from the root content directory
    process_dir(content_dir)
main()

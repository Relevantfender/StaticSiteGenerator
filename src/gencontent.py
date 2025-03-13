import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, BASEPATH):
    print(f"Generating page from {from_path} to {dest_path}, using {template_path}")
    
    with open(from_path, "r") as file:
        markdown = file.read()
    
    with open(template_path, "r") as file:
        template = file.read()
    
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    
    title = extract_title(from_path)
    
    template = template.replace("{{ title }}", title).replace("{{ content }}", content)
    template = template.replace("href=\"/", f"href=\"{BASEPATH}")
    template = template.replace("src=\"/", f"src=\"{BASEPATH}")
    
    dest_dir_path = os.path.dirname(dest_path)
    # name = os.path.join(dest_path, "index.html")
    
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
        print(f"Created destination path directory: {dest_dir_path}")

    
    with open(dest_path, "w", encoding="utf-8") as file:
        result = file.write(template)
        if result > 0:
            print(f"Page with the title \"{title}\" generated successfully")

def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, BASEPATH
):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, BASEPATH)
        else:
            generate_pages_recursive(
                from_path,
                template_path,
                dest_path,
                BASEPATH)
            
def extract_title(markdown)-> str:
    string = ""
    with open(markdown, "r") as file:
        string = file.readline()
    
    string = string.strip()
    if not string.startswith("# "):
        raise Exception("File should start with a header")
    string = string[2:].strip()
    return string
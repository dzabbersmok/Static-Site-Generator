import os
import shutil

from functions import markdown_to_html_node

def create_directory(dir_name):
    directory = dir_name
    parent_dir = ""
    path = os.path.join(parent_dir, directory)

    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Deleted directory: {directory}") 

    os.mkdir(path)
    print(f"Created directory: {directory}") 

def list_files(path):
    if not os.path.exists(path):
        print(f"Path does not exist: {path}")
        return
    
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            create_directory(f"{full_path.replace("static", "public")}")
            list_files(full_path)

        if os.path.isfile(full_path):
            shutil.copy(full_path, full_path.replace("static", "public"))
            return

def extract_title(markdown):
    lines = markdown.split("\n")
    header = None
    for line in lines:
        if line.strip()[0:2] == "# ":
            header = line[2:]
            break

    if not header:
        raise Exception("missing main header")
    
    return header

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        md_file = file.read()

    with open(template_path, "r") as file:
        template_file = file.read()

    content = markdown_to_html_node(md_file).to_html()

    title = extract_title(md_file)
    output_html = template_file.replace("{{ Content }}", content).replace("{{ Title }}", title)

    with open(dest_path, "w") as file:
        file.write(output_html)

def main():
    create_directory("public")
    list_files("static")

    # test_md/simple_header.md
    # content/index.md
    from_path = "content/index.md"
    template_path = "template.html" 
    dest_path = "public/index.html"
    generate_page(from_path, template_path, dest_path)

main()
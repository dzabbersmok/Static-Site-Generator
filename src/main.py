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
            create_directory(f"{full_path.replace(path, "public")}")
            list_files(full_path)

        if os.path.isfile(full_path):
            shutil.copy(full_path, full_path.replace("static", "public"))
            return
        
def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)

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
    # create_directory("public")
    # list_files("static")
    copy_files_recursive("static", "public")
    copy_files_recursive("content", "public")

    # test_md/simple_header.md
    # content/index.md
    from_path = "content/index.md"
    template_path = "template.html" 
    dest_path = "public/index.html"
    generate_page(from_path, template_path, dest_path)

    generate_page("content/blog/glorfindel/index.md", template_path, "public/blog/glorfindel.html")
    generate_page("content/blog/tom/index.md", template_path, "public/blog/tom.html")
    generate_page("content/blog/majesty/index.md", template_path, "public/blog/majesty.html")
    generate_page("content/contact/index.md", template_path, "public/contact.html")

main()
import os
import shutil
import sys

from functions import markdown_to_html_node

basepath = "/"
if sys.argv[0]:
    basepath = sys.argv[0]

print("basepath", basepath)
# def create_directory(dir_name):
#     directory = dir_name
#     parent_dir = ""
#     path = os.path.join(parent_dir, directory)

#     if os.path.exists(path):
#         shutil.rmtree(path)
#         print(f"Deleted directory: {directory}") 

#     os.mkdir(path)
#     print(f"Created directory: {directory}") 

# def list_files(path):
#     if not os.path.exists(path):
#         print(f"Path does not exist: {path}")
#         return
    
#     for entry in os.listdir(path):
#         full_path = os.path.join(path, entry)

#         if os.path.isdir(full_path):
#             create_directory(f"{full_path.replace(path, "public")}")
#             list_files(full_path)

#         if os.path.isfile(full_path):
#             shutil.copy(full_path, full_path.replace("static", "public"))
            # return
        
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        md_file = file.read()

    with open(template_path, "r") as file:
        template_file = file.read()

    content = markdown_to_html_node(md_file).to_html()

    title = extract_title(md_file)
    output_html = template_file.replace("{{ Content }}", content).replace("{{ Title }}", title).replace("href=/", f"href={basepath}").replace("src=/", f"src={basepath}")

    with open(dest_path, "w") as file:
        file.write(output_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    data = os.listdir(dir_path_content)
    for item in data:
        item_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(item_path):
            html = item.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, html)
            generate_page(item_path, template_path, dest_path, basepath)
        else:
            dir_path = os.path.join(dir_path_content, item)
            des_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(dir_path, template_path, des_path, basepath)

def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        # print(f" * {from_path} -> {dest_path}")
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

print("test")

def main():
    # create_directory("public")
    # list_files("static")
    copy_files_recursive("static", "docs")
    copy_files_recursive("content", "docs")

    # test_md/simple_header.md
    # content/index.md
    # from_path = "content/index.md"
    template_path = "template.html" 
    # dest_path = "public/index.html"
    # generate_page(from_path, template_path, dest_path)

    # generate_page("content/blog/glorfindel/index.md", template_path, "public/blog/glorfindel.html")
    # generate_page("content/blog/tom/index.md", template_path, "public/blog/tom.html")
    # generate_page("content/blog/majesty/index.md", template_path, "public/blog/majesty.html")
    # generate_page("content/contact/index.md", template_path, "public/contact.html")

    generate_pages_recursive("content", template_path, "docs", basepath)

main()
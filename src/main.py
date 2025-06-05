import os
import shutil

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
        print(f"full_path: {full_path}")

        if os.path.isdir(full_path):
            create_directory(f"{full_path.replace("static", "public")}")
            list_files(full_path)

        if os.path.isfile(full_path):
            shutil.copy(full_path, full_path.replace("static", "public"))
            return

def main():
    create_directory("public")
    list_files("static")

main()
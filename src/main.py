import os
import shutil
import sys
from pathlib import Path

from markdown_to_html import extract_title, markdown_to_html_node

default_basepath = "/"
dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"


def copy_all_files(source, destination):
    if not os.path.exists(source):
        raise ValueError("Path does not exist")
    if os.path.exists(destination):
        print("Deleting destination...")
        shutil.rmtree(destination)
        print("Destination deleted.")

    os.mkdir(destination)
    print("New destination created.")
    items = os.listdir(source)
    for i in items:
        if os.path.isfile(f"{source}/{i}"):
            shutil.copy(f"{source}/{i}", f"{destination}/{i}")
            print(f"File {i} copied.")
        else:
            os.mkdir(f"{destination}/{i}")
            print(f"Folder {i} created.")
            copy_all_files(f"{source}/{i}", f"{destination}/{i}")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)


main()

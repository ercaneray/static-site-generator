import os
import shutil
from pathlib import Path

from markdown_to_html import extract_title, markdown_to_html_node


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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md_file = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    content = markdown_to_html_node(md_file).to_html()
    title = extract_title(md_file)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def main():
    print("Generating content...")
    generate_pages_recursive("content", "template.html", "public")


main()

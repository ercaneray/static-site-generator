import os
import shutil

from markdown_to_html import extract_title, markdown_to_html_node


def copy_all_files(source, destination):
    if not os.path.exists(source):
        raise ValueError("Path does not exist")
    if os.path.exists(destination):
        print("Deleting destination...")
        shutil.rmtree(destination)
        print("Destination deleted.")
    generate_page(source, "template.html", destination)
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
    with open(dest_path, "w") as f:
        f.write(template)


def main():
    copy_all_files("static", "public")


main()

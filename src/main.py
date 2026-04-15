import os
import shutil


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


def main():
    copy_all_files("static", "public")


main()

import os
import yaml
from slugify import slugify

DEFAULT_BLOG_DATA = {
    "id": "Default",
    "slug": "",
    "title": "",
    "next": "Default",
    "previous": "Default",
    "createdBy": "Default",
    "updatedBy": "Default",
    "lastUpdatedTime": "Default",
    "createdTime": "Default",
    "isShow": True,
}

DEFAULT_CATE_DATA = {
    "id": "",
    "slug": "",
    "name": "",
    "displayName": "",
    "isShow": True,
}


def initial_data(parent_path: str, child: str, data):
    folder_path = os.path.join(parent_path, f"{child}")
    os.makedirs(folder_path)

    with open(os.path.join(folder_path, "info.yaml"), "w") as yaml_file:
        yaml.dump({"data": data}, yaml_file)

    with open(os.path.join(folder_path, "README.md"), "w") as readme_file:
        readme_file.writelines("add your content here....")


def get_input_data_for_blog():
    _type = input("Enter 1. Library | 2. Blogs: ")
    parent_folder = "library" if _type == "1" else "blogs"

    categories = set()
    for x in os.walk(f"./{parent_folder}/"):
        x_path = x[0].split("/")
        if len(x_path) >= 2 and x_path[2] != "":
            categories.add(x_path[2])

    if len(categories) == 0:
        print("No valid category found! Pls create category first!")
        exit(1)

    while True:
        _cate = input(f"Enter category [{'-'.join([x for x in categories])}]: ")
        if _cate in categories:
            break
        else:
            print("Invalid category: ")

    _name = input("Enter blog name: ")
    _next = input("Enter next blog id: ")
    _previous = input("Enter previous blog id: ")

    path_to_folder = os.path.join(parent_folder, _cate)

    return path_to_folder, _name, _next, _previous


def create_blog():
    path_to_parent, name, next_id, previous_id = get_input_data_for_blog()
    slug = slugify(name)
    DEFAULT_BLOG_DATA["slug"] = slug
    DEFAULT_BLOG_DATA["next"] = next_id
    DEFAULT_BLOG_DATA["previous"] = previous_id
    DEFAULT_BLOG_DATA["title"] = name

    with open("./INDEX", "r") as file:
        number_post = file.readlines()[0]

    idx = "0" * (4 - len(number_post)) + number_post
    initial_data(path_to_parent, idx, DEFAULT_BLOG_DATA)

    with open("./INDEX", "w") as file:
        file.write(str(int(number_post) + 1))


def create_category():
    _type = input("Enter 1. Library | 2. Blogs: ")
    parent_folder = "library" if _type == "1" else "blogs"
    DEFAULT_CATE_DATA["name"] = input("Enter category name: ")
    DEFAULT_CATE_DATA["displayName"] = input("Enter display name: ")
    DEFAULT_CATE_DATA["slug"] = slugify(DEFAULT_CATE_DATA["displayName"])
    initial_data(parent_folder, DEFAULT_CATE_DATA["name"], DEFAULT_CATE_DATA)


if __name__ == "__main__":
    selected = input(
        "Enter \n\t1. Create new blog.\n\t2. Create new category \n Your choice: "
    )
    create_blog() if selected == "1" else create_category()
    print("Process done.")

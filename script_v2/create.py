import os
import yaml
import subprocess
from slugify import slugify


DEFAULT_BLOG_DATA = {
    "createdBy": "",
    "isShow": True,
    "nextBlog": "",
    "previousBlog": "",
    "slug": "",
    "title": "",
    "updateBy": "",
    "cateId": 1,
    "id": None
}

DEFAULT_CATE_DATA = {
    "id": None,
    "slug": "",
    "name": "",
    "parent": "",
    "isShow": True,
}


def initial_data(parent_path: str, child: str, data):
    folder_path = os.path.join(parent_path, f"{child}")
    os.makedirs(folder_path)

    with open(os.path.join(folder_path, "info.yaml"), "w") as yaml_file:
        yaml.dump({"data": data}, yaml_file)

    with open(os.path.join(folder_path, "README.md"), "w") as readme_file:
        readme_file.writelines("add your content here....")


def create_blog():
    parent_folder = input("Enter category folder name: ")

    for x in os.walk("./docs"):
        if x[0].split("/")[-1] == parent_folder:
            cate_path = x[0]

    name = input("Enter blog name: ")
    next = input("Enter next blog id: ")
    previous = input("Enter previous blog id: ")
    
    with open(os.path.join(cate_path, "info.yaml"), "r") as f:
        data = yaml.safe_load(f)['data']

    slug = slugify(name)
    DEFAULT_BLOG_DATA["slug"] = slug
    DEFAULT_BLOG_DATA["nextBlog"] = next
    DEFAULT_BLOG_DATA["previousBlog"] = previous
    DEFAULT_BLOG_DATA["title"] = name
    DEFAULT_BLOG_DATA['cateId'] = data['id']

    # get current user
    res = subprocess.run(["git", "config", "user.name"], stdout=subprocess.PIPE)
    git_username = res.stdout.strip().decode()
    DEFAULT_BLOG_DATA["updateBy"] = git_username
    DEFAULT_BLOG_DATA["createdBy"] = git_username

    with open("./INDEX", "r") as file:
        number_post = file.readlines()[0]

    idx = "0" * (4 - len(number_post)) + number_post
    initial_data(cate_path, idx, DEFAULT_BLOG_DATA)

    with open("./INDEX", "w") as file:
        file.write(str(int(number_post) + 1))


def create_category():
    while True:
        parent_folder = input("Enter parent folder: ")
        if parent_folder is not None:
            break
    
    name =  input("Enter category name: ")
    DEFAULT_CATE_DATA["name"] = name
    DEFAULT_CATE_DATA["parent"] = slugify(parent_folder)
    DEFAULT_CATE_DATA["slug"] = slugify(name)
    
    for x in os.walk("./docs"):
        if x[0].split("/")[-1] == parent_folder:
            parent_path = x[0]
    
    initial_data(parent_path, slugify(name), DEFAULT_CATE_DATA)


if __name__ == "__main__":
    selected = input(
        "Enter \n\t1. Create new blog.\n\t2. Create new category \n Your choice: "
    )
    create_blog() if selected == "1" else create_category()
    print("Process done.")

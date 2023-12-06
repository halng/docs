"""
This is my pet project.
This script will be run when new pr merged into base branch is dev.
Script will deploy all change and alert for slack group aware about the change.
"""

import os
from main import alert_slack, GitUtils, update_build_and_comment
import requests
import yaml

# define url
BASE_URL = os.getenv("BASE_URL", "")
URL_CATEGORY = f"{BASE_URL}/categories"
URL_BLOG_META = f"{BASE_URL}/blogs"
URL_BLOG_CONTENT = f"{BASE_URL}/blogs-content"

HEADER = {'Content-Type': 'application/json', "X-REQUEST-API-TOKEN": os.getenv(
    "API_KEY_NAME", "")}


def read_file(file_path: str):
    with open(file_path, "r") as f:
        if file_path.endswith("yaml"):
            return yaml.safe_load(f)['data']
        else:
            return f.read()


def update_file(file_path: str, data):
    with open(file_path, "w") as f:
        yaml.dump({"data": data}, f)


def create(yaml_path: str, url: str) -> str:
    data = read_file(yaml_path)
    req = requests.post(url=url, json=data, headers=HEADER)
    res = req.json()
    if res['code'] == 201:
        update_file(yaml_path, res['data'])
        return 'Success'
    else:
        return 'Failed'


def update(yaml_path: str, url: str) -> str:  # need to load file and read id
    data = read_file(yaml_path)
    req = requests.post(url=url, json=data, headers=HEADER)
    res = req.json()
    print(res)
    if res['code'] == 200:
        update_file(yaml_path, res['data'])
        return 'Success'
    else:
        return 'Failed'


def update_content(path: str, url: str) -> str:
    content = read_file(path)
    metadata = read_file(path.replace("README.md", "info.yaml"))
    req = requests.put(
        url=url, json={"slug": metadata["slug"], "content": content, "id": metadata["id"], "createdBy": metadata['createdBy'], "updatedBy": metadata["updateBy"]}, headers=HEADER
    )
    return req.json()["data"]


def create_content(path: str, url: str) -> str:
    content = read_file(path)
    metadata = read_file(path.replace("README.md", "info.yaml"))
    req = requests.post(
        url=url, json={"slug": metadata["slug"], "content": content, "id": metadata["id"], "createdBy": metadata['createdBy'], "updatedBy": metadata["updateBy"]}, headers=HEADER
    )
    return req.json()["data"]


if __name__ == "__main__":
    alert_slack(
        "Hi <!here>. new code merged in `dev` branch. Process deploy start...")

    g = GitUtils(remote_branch="dev", current_branch="dev")

    if len(g.get_category_change()) > 0:
        for x in g.get_category_change():
            if str(x["_path"]).endswith("yaml"):
                msg = (
                    create(x["_path"], URL_CATEGORY)
                    if x["_type"] == "A"
                    else update(x["_path"], URL_CATEGORY)
                )
                alert_slack(f'{x["_type"]} metadata {x["_path"]}: {msg}')

    if len(g.get_blog_change()) > 0:
        for x in g.get_blog_change():
            if x["_path"].endswith("yaml"):
                msg = (
                    create(x["_path"], URL_BLOG_META)
                    if x["_type"] == "A"
                    else update(x["_path"], URL_BLOG_META)
                )
                alert_slack(f'{x["_type"]} metadata {x["_path"]}: {msg}')

        # priority for create metadata first
        for x in g.get_blog_change():
            msg = (
                create_content(x["_path"], URL_BLOG_CONTENT)
                if x["_type"] == "A"
                else update_content(x["_path"], URL_BLOG_CONTENT)
            )
            alert_slack(f'{x["_type"]} metadata {x["_path"]}: {msg}')

    update_build_and_comment(g)

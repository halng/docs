import os

import requests

from utils import (
    get_all_changes,
    get_file_content,
    get_current_user,
    update_file_content,
    alert_slack,
    add_latest_change,
)

# get variable from env
BASE_URL = os.getenv("BASE_URL", "http://localhost:9090/api/v1/admin-blogger")
URL_CATEGORY = f"{BASE_URL}/categories"
URL_BLOG_META = f"{BASE_URL}/blogs"
URL_BLOG_CONTENT = f"{BASE_URL}/blogs-content"
API_TOKEN_VALUE = os.getenv("API_TOKEN_VALUE", "this-is-not-a-token")
REQUEST_HEADER = {
    "Content-Type": "application/json",
    "X-REQUEST-API-TOKEN": API_TOKEN_VALUE,
}


def create_request(json_data: dict, url: str) -> dict:
    req = requests.post(url, json=json_data, headers=REQUEST_HEADER)
    return req.json()


def update_request(json_data: dict, url: str) -> dict:
    req = requests.put(url, json=json_data, headers=REQUEST_HEADER)
    return req.json()


def create_category(yaml_file_path: str, metadata_changes):
    data = get_file_content(yaml_file_path)
    res = create_request(data, URL_CATEGORY)
    if res["code"] == 201:
        cate = res["data"]
        cate_id = cate["id"]
        update_file_content(yaml_file_path, cate)
        print(f"Create new category `{yaml_file_path.replace('/', ' > ')}`: Success")
        for change in metadata_changes:
            # update cateId in metadata for blog if need
            if (
                change["path"].endswith("yaml")
                and change["action"] == "A"
                and change["path"].startswith(yaml_file_path[:-10])
            ):
                _data = get_file_content(change["path"])
                _data["cateId"] = cate_id
                update_file_content(change["path"], _data)
                print(
                    f"Update category id for blog `{change['path'].replace('/', ' > ')}`: Success"
                )

    else:
        print(
            f"Create new category `{yaml_file_path.replace('/', ' > ')}`: Error with {res}"
        )


def create_metadata(yaml_file_path: str):
    data = get_file_content(yaml_file_path)
    res = create_request(data, URL_BLOG_META)
    if res["code"] == 201:
        res_data = res["data"]
        update_file_content(yaml_file_path, res_data)

        # insert new blog into README.md file in category folder
        new_row = f'\n| {res_data["id"]} | {res_data["title"]} | {res_data["nextBlog"] } | {res_data["previousBlog"]} |'
        category_info_path = yaml_file_path[:-14] + "README.md"
        update_file_content(category_info_path, new_row)

        print(f'Create new metadata `{yaml_file_path.replace("/", " > ")}`: Success')
    else:
        print(
            f'Create new metadata `{yaml_file_path.replace("/", " > ")}`: Error with {res}'
        )


def create_content(file_path: str):
    rm_data = get_file_content(file_path)
    meta_data = get_file_content(file_path.replace("README.md", "info.yaml"))
    json_data = {
        "content": rm_data,
        "id": meta_data["id"],
        "createdBy": meta_data["createdBy"],
        "updatedBy": get_current_user(),
    }
    res = create_request(json_data, URL_BLOG_CONTENT)

    msg = "Success" if res["code"] == 201 else "Error"
    print(f'Create content for blog `{file_path.replace("/", " > ")}`: {msg}')


def update_metadata(yaml_file_path: str):
    data = get_file_content(yaml_file_path)
    res = update_request(data, f'{URL_BLOG_META}/{data["id"]}')
    msg = "Success" if res["code"] == 200 else "Error"
    print(f'Update metadata `{yaml_file_path.replace("/", " > ")}`: {msg}')


def update_content(file_path: str):
    rm_data = get_file_content(file_path)
    meta_data = get_file_content(file_path.replace("README.md", "info.yaml"))
    json_data = {
        "content": rm_data,
        "id": meta_data["id"],
        "createdBy": meta_data["createdBy"],
        "updatedBy": get_current_user(),
    }
    res = update_request(json_data, URL_BLOG_CONTENT)

    return "Success" if res["code"] == 200 else "Error"


def update_category(yaml_file_path: str):
    data = get_file_content(yaml_file_path)
    res = update_request(data, f'{URL_CATEGORY}/{data["id"]}')
    msg = "Success" if res["code"] == 200 else "Error"
    print(f'Update category `{yaml_file_path.replace("/", " > ")}`: {msg}')


def update_build_and_comment():
    with open("./BUILD", "r") as f:
        current_index = int(f.readlines()[0])
    new_idx = current_index + 1
    with open("./BUILD", "w") as f2:
        f2.write(str(new_idx))

    add_latest_change(new_idx)


if __name__ == "__main__":
    alert_slack("Hi <!here>, new code merged into `dev` branch. Start deploying...")
    all_changes = get_all_changes("dev", "dev")

    category_changes = []
    metadata_changes = []
    content_changes = []

    for x in all_changes:
        action_type, _path = x.split("_")
        obj = {"path": _path, "action": action_type}
        if str(_path.split("/")[-2]).isdigit():
            if str(_path).endswith("yaml"):
                metadata_changes.append(obj)
            else:
                content_changes.append(obj)
        else:
            if str(_path).endswith("yaml"):
                category_changes.append(obj)

    if len(category_changes) > 0:
        for category in category_changes:
            update_category(category["path"]) if category[
                "action"
            ] == "M" else create_category(category["path"], metadata_changes)

    if len(metadata_changes) > 0:
        for metadata in metadata_changes:
            update_metadata(metadata["path"]) if metadata[
                "action"
            ] == "M" else create_metadata(metadata["path"])

    if len(content_changes) > 0:
        for content in content_changes:
            update_content(content["path"]) if content[
                "action"
            ] == "M" else create_content(content["path"])

    update_build_and_comment()

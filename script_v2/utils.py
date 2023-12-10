import os

import git
import requests
import yaml
import subprocess


def alert_slack(msg):
    payload = {"username": "AutoBot", "icon_emoji": ":robot_face:", "text": msg}
    web_hook = os.getenv("SLACK_WEB_HOOK", "")
    requests.post(web_hook, json=payload)


def get_all_changes(current_branch, remote_branch="dev") -> list:
    repo = git.Repo(".")
    all_changes = []
    if remote_branch == current_branch:
        latest_commit = repo.head.commit
        second_latest_commit = list(repo.iter_commits(paths="./BUILD"))[0]
        changes = repo.git.diff(second_latest_commit, latest_commit, name_status=True)

    else:
        repo.remotes.origin.fetch()
        local_commit = repo.commit(current_branch)
        remote_commit = repo.commit(remote_branch)
        changes = repo.git.diff(remote_commit, local_commit, name_status=True)
    for d in changes.split("\n"):
        if d is not None and (d.startswith("A") or d.startswith("M")):
            change_type, file_path = d.split("\t")
            if str(file_path).startswith("docs") and len(file_path.split("/")) > 2:
                all_changes.append(f"{change_type}_{file_path}")

    return all_changes


def get_file_content(file_path: str) -> dict | str:
    with open(file_path, "r") as f:
        raw = yaml.safe_load(f)
    return raw["data"] if file_path.endswith("yaml") else raw


def update_file_content(file_path: str, data):
    if file_path.endswith("yaml"):
        with open(file_path, "w") as f:
            yaml.dump({"data": data}, f)

    if file_path.endswith("md"):
        raw = get_file_content(file_path)
        raw = raw + data
        with open(file_path, "w") as f:
            f.write(raw)


def get_current_user():
    res = subprocess.run(["git", "config", "user.name"], stdout=subprocess.PIPE)
    git_username = res.stdout.strip().decode()
    return git_username

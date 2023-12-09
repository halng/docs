import os
import requests
import git

def alert_slack(msg):
    payload = {"username": "AutoBot", "icon_emoji": ":robot_face:", "text": msg}
    web_hook = os.getenv("SLACK_WEB_HOOK", "")
    requests.post(web_hook, json=payload)
    
def get_all_changes(current_branch, remote_branch="dev") -> list:
    repo = git.Repo('.')
    all_changes = []
    if remote_branch == current_branch:
        latest_commit = repo.head.commit
        second_latest_commit = list(repo.iter_commits(paths="./BUILD"))[0]
        changes = repo.git.diff(
            second_latest_commit, latest_commit, name_status=True
        )

    else:
        repo.remotes.origin.fetch()
        local_commit = repo.commit(current_branch)
        remote_commit = repo.commit(remote_branch)
        changes = repo.git.diff(remote_commit, local_commit, name_status=True)
    for d in changes.split("\n"):
        if d:
            change_type, file_path = d.split("\t")
            if(str(file_path).startswith("./docs")):
                all_changes.append(f"{change_type}_{file_path}")
            
    return all_changes
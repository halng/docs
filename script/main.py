import os
import requests
from enum import Enum
import git
import yaml

API_KEY_NAME = "API_AUTH_TOKEN_VALUE"
BASE_URL = "BACKEND_BASE_URL"
PR_NUMBER = "PR_NUMBER"
GITHUB_TOKEN = "GITHUB_TOKEN"
SLACK_WEB_HOOK = "SLACK_WEB_HOOK"


class Action(Enum):
    CREATE_NEW = (1,)
    UPDATE = (2,)
    UPDATE_METADATA = 3
    UPDATE_CONTENT = 4


class GitUtils:
    def __init__(self, remote_branch="dev", current_branch="") -> None:
        self.pr_number = os.getenv(PR_NUMBER)
        self.repo = git.Repo(".")
        self.all_changes = []
        self.remote_branch = remote_branch
        self.current_branch = current_branch
        self.get_all_changes()

    def get_all_changes(self):
        if self.remote_branch == self.current_branch:
            latest_commit = self.repo.head.commit
            second_latest_commit = list(self.repo.iter_commits(paths="./BUILD"))[0]
            changes = self.repo.git.diff(
                second_latest_commit, latest_commit, name_status=True
            )

        else:
            self.repo.remotes.origin.fetch()
            local_commit = self.repo.commit(self.current_branch)
            remote_commit = self.repo.commit(self.remote_branch)
            changes = self.repo.git.diff(remote_commit, local_commit, name_status=True)
        for d in changes.split("\n"):
            if d:
                change_type, file_path = d.split("\t")
                self.all_changes.append({"_type": change_type, "_path": file_path})

    def get_category_change(self):
        # {update: [category name], create: []}
        cate_changes = []
        for change in self.all_changes:
            _p = change["_path"].split("/")
            if len(_p) == 3 and _p[0] in ["blogs", "library"]:
                cate_changes.append(change)
        return cate_changes

    def get_blog_change(self):
        blogs_changes = []
        for change in self.all_changes:
            _p = change["_path"].split("/")
            if len(_p) == 4 and _p[0] in ["blogs", "library"]:
                blogs_changes.append(change)
        return blogs_changes

    def is_run(self):
        """Check is need to send request to create or not by checking file BUILD."""
        return "BUILD" not in self.all_changes

    def add_latest_change(self, _version):
        self.repo.config_writer().set_value(
            "user", "email", os.getenv("USER_EMAIL", "haonguyentan2001@gmail.com")
        ).release()
        self.repo.config_writer().set_value("user", "name", "Bot").release()
        self.repo.git.add(all=True)
        self.repo.git.commit("-m", str(_version))
        self.repo.git.push("origin", self.current_branch)

    def comment_pr(self, msg):
        pr_url = f"https://api.github.com/repos/tanhaok/docs/issues/{self.pr_number}/comments"
        # Set up the comment data
        comment_data = {
            "body": msg,
        }

        # Create a comment on the pull request
        response = requests.post(
            url=pr_url,
            json=comment_data,
            headers={
                "Authorization": f'token {os.getenv("GITHUB_TOKEN")}',
                "Accept": "application/vnd.github.v3+json",
            },
        )

        if response.status_code == 201:
            print("Comment created successfully.")
        else:
            print(
                f"Error creating comment. Status code: {response.status_code}, Response: {response.text}"
            )


class CRUDBase:
    def __init__(self, _url) -> None:
        api_key = os.getenv(API_KEY_NAME)
        self.base_url = os.getenv(BASE_URL)
        self.req_url = f"{self.base_url}/{_url}"
        self.header = {"X-REQUEST-API-TOKEN": api_key}
        self.data = {}
        self._id = None

    def create(self):
        req = requests.post(url=self.req_url, headers=self.header, data=self.data)
        return req

    def update(self):
        _url = f"{self.req_url}/{self._id}"
        req = requests.put(url=_url, data=self.data, headers=self.header)
        return req

    def update_status(self):
        _url = f"{self.req_url}/{self._id}"
        req = requests.patch(url=_url, data=self.data, headers=self.header)
        return req

    def execute(self, action):
        match action:
            case Action.CREATE_NEW:
                res = self.create()
            case Action.UPDATE:
                res = self.update()
            case Action.UPDATE_STATUS:
                res = self.update_status()

        if str(res.status_code).startswith("2"):
            # alert on slack
            return True
        else:
            # alert on slack
            return False

    def run_pre_merged(self, data):
        # show by comment on pr which file or category change
        pass

    def run_merged(self, data):
        # Alert on slack about change
        pass

    def run(self, branch, data):
        return self.run_merged(data) if branch == "dev" else self.run_pre_merged(data)


class Category(CRUDBase):
    def __init__(self) -> None:
        super().__init__("categories")

    def run_merged(self, data):
        pass

    def run_pre_merged(self, data_changes: dict):
        msg = ""
        for _data in data_changes:
            if str(_data["_path"]).endswith(".yaml"):
                with open(_data["_path"], "r") as f:
                    new_data = yaml.safe_load(f)
                _type = _data["_type"]
                _action = ""
                if _type == "A":
                    _action = "Create"
                elif _type == "M":
                    _action = "Update"
                else:
                    _action = "Un-support"

                msg = (
                    msg
                    + f"\n- {_action} category name `{new_data['data']['name']}` under `{str(_data['_path'])}`"
                )

        return msg


class Blog(CRUDBase):
    def __init__(self) -> None:
        super().__init__("blogs")

    def run_pre_merged(self, data_changes: dict):
        msg = ""
        content_msg = ""
        for _data in data_changes:
            if str(_data["_path"]).endswith(".yaml"):
                with open(_data["_path"], "r") as f:
                    new_data = yaml.safe_load(f)
                _type = _data["_type"]
                _action = ""
                if _type == "A":
                    _action = "Create"
                elif _type == "M":
                    _action = "Update"
                else:
                    _action = "Un-support"

                msg = (
                    msg
                    + f"\n- {_action} blog metadata `{new_data['data']['title']}` under `{str(_data['_path'])}`"
                )
            else:
                if _data["_type"] == "M":
                    content_msg = (
                        content_msg + f'\n- Update blog content `{_data["_path"][:-9]}`'
                    )
        return f"{msg}\n{content_msg}"

    def run_merged(self, data):
        pass


def update_build_and_comment(_g: GitUtils):
    with open("./BUILD", "r") as f:
        current_index = int(f.readlines()[0])
    new_idx = current_index + 1
    with open("./BUILD", "w") as f2:
        f2.write(str(new_idx))

    _g.add_latest_change(new_idx)


def alert_slack(msg):
    print(msg)
    payload = {"username": "AutoBot", "icon_emoji": ":robot_face:", "text": msg}
    web_hook = os.getenv(SLACK_WEB_HOOK, "")
    requests.post(web_hook, json=payload)


if __name__ == "__main__":
    branch = os.getenv("CURRENT_BRANCH", "")
    if branch is None or branch == "":
        branch = "dev"
    g = GitUtils(remote_branch="dev", current_branch=branch)

    if branch != "dev":
        alert_slack(
            f"Hi <!here>. Have some change in\n- pr https://github.com/tanhaok/docs/pull/{os.getenv(PR_NUMBER)} \n- Branch: https://github.com/tanhaok/docs/tree/{branch}"
        )
    else:
        alert_slack("Hi <!here>. New pr merged into dev")

    if g.is_run():
        if len(g.get_category_change()) > 0:
            c = Category()
            msg = "> CATEGORY \n" + c.run(branch, g.get_category_change())
            g.comment_pr(msg)
            alert_slack(msg)
        if len(g.get_blog_change()) > 0:
            b = Blog()
            msg = "> BLOG \n" + b.run(branch, g.get_blog_change())
            g.comment_pr(msg)
            alert_slack(msg)
    if branch == "dev":
        update_build_and_comment(g)


def get_action(type1: str, type2: str) -> Action:
    """Get action needed for blog/category

    Args:
        type1 (str): readme file type
        type2 (str): yaml file type

    Returns:
        _type_: Action Needed
    """

    if type1 == type2 and type1 == "A":
        return Action.CREATE_NEW
    elif type1 is None and type2 == "A":
        return Action.CREATE_NEW
    elif type1 is None and type2 == "M":
        return Action.UPDATE_METADATA
    elif type1 == "M" and type2 is None:
        return Action.UPDATE_CONTENT

import os
import requests
from enum import Enum
import git

API_KEY_NAME = "API_AUTH_TOKEN_VALUE"
BASE_URL = "BACKEND_BASE_URL"

class Action(Enum):
    CREATE = 1,
    UPDATE = 2,
    UPDATE_STATUS = 3
    
class GitUtils:
    def __init__(self) -> None:
        self.pr_number = ""
        self.repo = git.Repo(".")
        self.all_changes = [
            d.a_path for d in self.repo.index.diff(None)] + self.repo.untracked_files
    def get_category_change(self):
        # {update: [category name], create: []}
        cate_changes = []
        for change in self.all_changes:
            _p = change.split("/")
            if len(_p) == 3 and _p[0] in ["blogs", "library"]:
                cate_changes.append(change) 
        return cate_changes
    
    def get_blog_change(self):
        blogs_changes = []
        for change in self.all_changes:
            _p = change.split("/")
            if len(_p) == 4 and _p[0] in ["blogs", "library"]:
                blogs_changes.append(change)
        return blogs_changes
    
    def is_run(self):
        """ Check is need to send request to create or not by checking file BUILD."""
        return "BUILD" not in self.all_changes
    
    def add_latest_change(self, _version):
        self.repo.git.add(all=True)
        self.repo.git.commit("-m", str(_version))
        
class CRUDBase:
    def __init__(self, _url) -> None:
        api_key = os.environ.get(API_KEY_NAME)
        self.base_url = os.environ.get(BASE_URL)
        self.req_url = _url
        self.header = {'X-REQUEST-API-TOKEN': api_key}
        self.data = {}
        self._id = None

    def create(self):
        req = requests.post(
            url=self.req_url, headers=self.header, data=self.data)
        return req

    def update(self):
        _url = f'{self.req_url}/{self._id}'
        req = requests.put(url=_url, data=self.data, headers=self.header)
        return req

    def update_status(self):
        _url = f'{self.req_url}/{self._id}'
        req = requests.patch(url=_url, data=self.data, headers=self.header)
        return req

    def execute(self, action):
        match action:
            case Action.CREATE:
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
        
    def run_pre_merged(self):
        # show by comment on pr which file or category change
        pass
    
    def run_merged(self):
        # Alert on slack about change
        pass
    
    def run(self, branch):
        self.run_merged() if branch == "main" else self.run_pre_merged()
    
class Category(CRUDBase):
    def __init__(self) -> None:
        cate_url = f'{self.base_url}/categories'
        super().__init__(cate_url)
    
    
class Blog(CRUDBase):
    def __init__(self) -> None:
        blog_url = f'{self.base_url}/blogs'
        super().__init__(blog_url)
            
            
def update_build_and_comment(_g: GitUtils):
    with open("./BUILD", "r") as f:
        current_index = int(f.readlines()[0])
    new_idx = current_index + 1
    with open("./BUILD", "w") as f2:
        f2.write(str(new_idx))
    
    _g.add_latest_change(new_idx)
    
if __name__ == '__main__':
    g = GitUtils()
    branch = "dev"
    if g.is_run():
        if len(g.get_category_change()) == 0:
            c = Category()
            c.run(branch)
        if len(g.get_blog_change()) == 0:
            b = Blog()
            b.run(branch)
        update_build_and_comment(g)

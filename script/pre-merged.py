"""
This is my pet project.
This script will be run when new pr created with base branch is dev.
Script will check all file change and alert for slack group aware about the change.
And comment change on pr for pr's owner know.
"""

import os
from main import alert_slack, GitUtils, PR_NUMBER, get_action


if __name__ == "__main__":
    branch = "op1" #os.getenv("CURRENT_BRANCH", "")
    pr_number = 1 #os.getenv(PR_NUMBER)
    alert_slack(
        f"Hi <!here>. Have some change in\n- pr https://github.com/tanhaok/docs/pull/{pr_number} \n- Branch: https://github.com/tanhaok/docs/tree/{branch}"
    )

    g = GitUtils(remote_branch="dev", current_branch=branch)
    print(g.all_changes)
    if g.is_run():
        if len(g.get_category_change()) > 0:
            pass
        if len(g.get_blog_change()) > 0:
            pass 

        

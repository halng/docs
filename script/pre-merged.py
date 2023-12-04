"""
This is my pet project.
This script will be run when new pr created with base branch is dev.
Script will check all file change and alert for slack group aware about the change.
And comment change on pr for pr's owner know.
"""

import os
from main import alert_slack, GitUtils, PR_NUMBER, get_action, Action


if __name__ == "__main__":
    branch = os.getenv("CURRENT_BRANCH", "dev-1")
    pr_number = os.getenv(PR_NUMBER, "1")
    alert_slack(
        f"Hi <!here>. Have some change in\n- pr https://github.com/tanhaok/docs/pull/{pr_number} \n- Branch: https://github.com/tanhaok/docs/tree/{branch}"
    )

    g = GitUtils(remote_branch="dev", current_branch=branch)
    if len(g.get_category_change()) > 0:
        msg = "> CATEGORY "
        for x in g.get_category_change():
            if str(x["_path"]).endswith("yaml"):
                msg = (
                    msg
                    + f'\n- {get_action(None, x["_type"]).name} for category `{str(x["_path"]).split("/")[1]}` under `{str(x["_path"]).split("/")[0]}`'
                )
        alert_slack(msg)
        g.comment_pr(msg)
    if len(g.get_blog_change()) > 0:
        msg = "> BLOG "
        for x in g.get_blog_change():
            action = ""
            if x["_path"].endswith("yaml"):
                action = (
                    Action.UPDATE_METADATA if x["_type"] == "M" else Action.CREATE_NEW
                )
            elif x["_path"].endswith("md"):
                action = (
                    Action.UPDATE_CONTENT if x["_type"] == "M" else Action.CREATE_NEW
                )
            msg = (
                msg
                + f"\n- {action.name} for blog id: `{str(x['_path']).split('/')[2]}` under `{x['_path'].split('/')[0]} -> {x['_path'].split('/')[1]}`"
            )
        alert_slack(msg)
        g.comment_pr(msg)

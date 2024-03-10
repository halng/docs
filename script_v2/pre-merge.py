import os

from utils import get_all_changes, alert_slack

if __name__ == "__main__":
    branch = os.getenv("CURRENT_BRANCH", "dev-test")
    pr_number = os.getenv("PR_NUMBER", "1")

    alert_slack(
        f"Hi <!here>. Have some change in\n- pr https://github.com/tanhaok/docs/pull/{pr_number} \n- Branch: https://github.com/tanhaok/docs/tree/{branch}"
    )

    all_changes = get_all_changes(branch, "dev")

    for x in all_changes:
        action_type, _path = x.split("_")
        action = "CREATE" if action_type == "A" else "UPDATE"

        if not str(_path).endswith("png"):
            if str(_path.split("/")[-2]).isdigit():
                obj = "BLOG_META" if str(_path).endswith("yaml") else "BLOG_CONTENT"
                alert_slack(
                    f'`{action}` the `{obj}` in path: `{_path.replace("/", " > ")}`'
                )
            else:
                if str(_path).endswith("yaml"):
                    alert_slack(
                        f'`{action}` the `CATEGORY` in path: `{_path.replace("/", " > ")}`'
                    )

import os
from utils import get_all_changes, alert_slack

branch = os.getenv("CURRENT_BRANCH", "dev-test")
pr_number = os.getenv("PR_NUMBER", "1")

alert_slack(
        f"Hi <!here>. Have some change in\n- pr https://github.com/tanhaok/docs/pull/{pr_number} \n- Branch: https://github.com/tanhaok/docs/tree/{branch}"
    )

all_changes = get_all_changes(branch, "dev")

for x in all_changes:
    action_type, _path = x.split('_')
    action = "CREATE" if action_type == "A" else "UPDATE"
     
    try:
        int(_path.split("/")[-2])
        obj = "BLOG_META" if str(_path).endswith("yaml") else "BLOG_CONTENT"
        alert_slack(f'`{action}` the `{obj}` in path: `{_path.replace("/", " > ")}`')
    except ValueError:
        if str(_path).endswith("yaml"):
            alert_slack(f'`{action}` the `CATEGORY` in path: `{_path.replace("/", " > ")}`')
    
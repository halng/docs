from main import GitUtils, update_build_and_comment

g = GitUtils(remote_branch="dev", current_branch="dev")


update_build_and_comment(g)

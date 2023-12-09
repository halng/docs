import os
from utils import get_all_changes, alert_slack

print(get_all_changes("dev-004", "dev"))
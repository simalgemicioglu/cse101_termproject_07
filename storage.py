import json
import os
from datetime import datetimefrom shutil import copyfile
TASK_FILE = "data/tasks.json"
CATEGORY_FILE = "data/categories.json"
ACTIVITY_LOG = "data/activity.log"
BACKUP_DIR = "backups/"
def _load_json(filepath: str) -> list:
    if not os.path.exists(filepath):
        return[]
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            if not content:
                return[]
            return json.loads(content)
    except (json.JSONecodeError, FileNotFoundError):
        print(f"Error: There was a problem loading the {filepath} file. Invalid format or file not found")
        return[]
    
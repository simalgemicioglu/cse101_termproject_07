import json
import os
from datetime import datetime
from shutil import copyfile
TASK_FILE = "data/tasks.json"
CATEGORY_FILE = "data/categories.json"
ACTIVITY_LOG = "data/activity.log"
BACKUP_DIR = "backups/"
def _load_json(filepath: str) -> list:
    if not os.path.exists(filepath):
        return[]
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content:
                return[]
            return json.loads(content)
    except (json.JSONecodeError, FileNotFoundError):
        print(f"Error: There was a problem loading the {filepath} file. Invalid format or file not found")
        return[]
def _save_json(filepath: str, data: list) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error: {filepath} There was a problem while saving: {e}")
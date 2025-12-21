import json
import os
import shutil
from datetime import datetime

TASK_FILE = "data/tasks.json"
CATEGORY_FILE = "data/categories.json"
ACTIVITY_LOG = "data/activity.log"
BACKUP_DIR = "backups/"

def load_state(base_dir: str = "data") -> tuple[list, list, list]:
    tasks = _load_json(os.path.join(base_dir, "tasks.json"))
    categories = _load_json(os.path.join(base_dir, "categories.json"))
    
    activity_log = [] 
    log_path = os.path.join(base_dir, "activity.log")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            activity_log = [line.strip() for line in f.readlines() if line.strip()]
            
    return tasks, categories, activity_log

def save_state(base_dir: str, tasks: list, categories: list, activity_log: list) -> None:
    _save_json(os.path.join(base_dir, "tasks.json"), tasks)
    _save_json(os.path.join(base_dir, "categories.json"), categories)
    
    log_path = os.path.join(base_dir, "activity.log")
    with open(log_path, "w", encoding="utf-8") as f:
        for line in activity_log:
            f.write(line + "\n")

def backup_state(base_dir: str, backup_dir: str) -> str:
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{timestamp}"
    backup_full_path = os.path.join(backup_dir, backup_filename)
    return shutil.make_archive(backup_full_path, 'zip', base_dir)



def validate_task_schema(tasks: list) -> bool:
    required = ["id", "title", "status", "priority"]
    for task in tasks:
        if not all(field in task for field in required):
            return False
    return True

def _load_json(filepath: str) -> list:
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return json.loads(content) if content else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _save_json(filepath: str, data: list) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
import json
import os
import shutil
from datetime import datetime

TASK_FILENAME = "tasks.json"
CATEGORY_FILENAME = "categories.json"
LOG_FILENAME = "activity.log"

def load_state(base_dir: str) -> tuple[list, list, list]:
    
    tasks_path = os.path.join(base_dir, TASK_FILENAME)
    cats_path = os.path.join(base_dir, CATEGORY_FILENAME)
    log_path = os.path.join(base_dir, LOG_FILENAME)
    
    tasks = _load_json(tasks_path)
    categories = _load_json(cats_path)
    
    activity_log = []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            activity_log = [line.strip() for line in f.readlines()]
            
    return tasks, categories, activity_log

def save_state(base_dir: str, tasks: list, categories: list, activity_log: list) -> None:
    os.makedirs(base_dir, exist_ok=True)
    
    _save_json(os.path.join(base_dir, TASK_FILENAME), tasks)
    _save_json(os.path.join(base_dir, CATEGORY_FILENAME), categories)
    
    with open(os.path.join(base_dir, LOG_FILENAME), "w", encoding="utf-8") as f:
        for entry in activity_log:
            f.write(f"{entry}\n")

def backup_state(base_dir: str, backup_dir: str) -> list[str]:
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
    
    zip_path = shutil.make_archive(backup_path, 'zip', base_dir)
    return [zip_path]

def validate_task_schema(tasks: list) -> bool:
    required_fields = ["id", "title", "status", "priority", "category"]
    for task in tasks:
        if not all(field in task for field in required_fields):
            return False
    return True

def _load_json(filepath: str) -> list:
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _save_json(filepath: str, data: list) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
import json
import os
from datetime import datetime

def log_activity(log_path: str, event: dict) -> None:
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": event['action'],
        "task_id": event['task_id'],
        "summary": event['summary']
    }
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

def load_activity(log_path: str) -> list:
    if not os.path.exists(log_path): 
        return []
    activities = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                activities.append(json.loads(line.strip()))
    return activities

def productivity_stats(tasks: list) -> dict:
    total = len(tasks)
    completed = [t for t in tasks if t['status'] == 'Completed']
    efficiency = (len(completed) / total * 100) if total > 0 else 0
    
    return {
        "total_tasks": total,
        "completed_count": len(completed),
        "efficiency": round(efficiency, 2)
    }

def export_report(report: dict, filename: str) -> str:
    os.makedirs("reports", exist_ok=True)
    path = f"reports/{filename}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"--- Productivity Report - {datetime.now().strftime('%Y-%m-%d %H:%M')} ---\n")
        f.write(json.dumps(report, indent=4))
    return path
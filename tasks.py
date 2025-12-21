from datetime import datetime, timedelta

def get_next_id(tasks):
    if not tasks:
        return "1"
    all_ids = [int(task['id']) for task in tasks]
    new_id = max(all_ids) + 1
    return str(new_id)

def create_task(tasks: list, task_data: dict) -> dict:
    current_id = get_next_id(tasks)
    new_task = {
        "id": current_id,
        "title": task_data.get('title', 'Untitled'),
        "description": task_data.get('description', ''),
        "status": "Pending",
        "priority": task_data.get('priority', 'Medium'),
        "category": task_data.get('category', 'General'),
        "due_date": task_data.get('due_date'),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "subtasks": []
    }
    tasks.append(new_task)
    return new_task

def filter_tasks(tasks, status=None, category=None, due_before=None):
    filtered = tasks
    
    if status:
        filtered = [t for t in filtered if t.get('status') == status]
        
    if category:
        filtered = [t for t in filtered if t.get('category') == category]
        
    if due_before:
        filtered = [t for t in filtered if t.get('due_date') and t['due_date'] < due_before]   
    return filtered

def update_task(tasks, task_id, updates):
    for task in tasks:
        if task['id'] == task_id:
            task.update(updates)
            return task
    return None

def mark_task_status(tasks: list, task_id: str, status: str) -> dict:
    return update_task(tasks, task_id, {"status": status})

def add_subtask(tasks: list, task_id: str, subtask_data: dict) -> dict:
    for task in tasks:
        if task['id'] == task_id:
            task['subtasks'].append(subtask_data)
            return task
    return None

def search_tasks(tasks: list, query: str) -> list:
    query = query.lower()
    return [t for t in tasks if query in t['title'].lower() or query in t['description'].lower()]

def delete_task(tasks: list, task_id: str) -> bool:
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks.pop(i)
            return True
    return False

def summarize_by_category(tasks: list) -> dict:
    summary = {}
    for t in tasks:
        cat = t['category']
        summary[cat] = summary.get(cat, 0) + 1
    return summary

def upcoming_tasks(tasks: list, within_days: int) -> list:
    limit_date = (datetime.now() + timedelta(days=within_days)).isoformat()
    return [t for t in tasks if t['due_date'] and t['due_date'] <= limit_date]

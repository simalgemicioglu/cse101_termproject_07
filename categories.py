import json
import os

def load_categories(path: str) -> list:
    if not os.path.exists(path):
        return[]
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_categories(path: str, categories: list) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=4)

def add_category(categories: list, category_data: dict) -> dict:
    if any(c['name'] == category_data['name'] for c in categories):
        return None
    if not categories:
        new_id = "1"
    else:
        new_id = str(max(int(c['id']) for c in categories) + 1)
    new_cat = {
        "id": new_id,
        "name": category_data['name'],
        "description": category_data.get('description', ''),
        "color_code": category_data.get('color_code', 'White')
    }
    categories.append(new_cat)
    return new_cat
def update_category(categories: list, category_id: str, updates: dict) -> dict:
    for cat in categories:
        if cat['id'] == category_id:
            cat.update(updates)
            return cat
        return {}

def delete_category(categories: list, category_id: str, tasks: list) -> bool:
    for i, cat in enumerate(categories):
        if cat['id'] == category_id:
            cat_name = categories[i]['name']
            categories.pop(i)
            for task in tasks:
                if task.get('category') == cat_name:
                    task['category'] = 'General'
            return True
    return False
from asyncio import current_task
import storage
import os
import tasks as task_ops
import categories as cat_ops
import activity
from datetime import datetime

def setup_folders():
    os.makedirs("data", exist_ok=True)
    os.makedirs("backups", exist_ok=True)

def display_summary(tasks, overdue_tasks):
    today = datetime.now().strftime("%Y-%m-%d")
    due_today = [t for t in tasks if t.get('due_date') == today and t['status'] != 'Completed']
    print("\n" + "="*50)
    print(f"📅 WELCOME! Today's Date: {today}")
    print("-" * 50)
    if due_today:
        print(f"🔔 NOTIFICATION: You have {len(due_today)} task(s) due today!")
    if overdue_tasks:
        print(f"⚠️  WARNING: {len(overdue_tasks)} overdue task(s) detected!")
        for ot in overdue_tasks:
            print(f"   - [ID: {ot['id']}] {ot['title']} (Due: {ot['due_date']})")
    if not due_today and not overdue_tasks:
        print("✅ Excellent! No urgent or overdue tasks for today.")
        
    print("="*50)

def main():
    setup_folders()
    all_tasks, all_cats, activity_log = storage.load_state("data")
    if not any(c['name'] == 'General' for c in all_cats):
        all_cats.insert(0, {"id": "0", "name": "General"})
    overdue_tasks = task_ops.check_overdue_tasks(all_tasks)
    display_summary(all_tasks, overdue_tasks)

    while True:
        print("\n--- 🛠️ TASK MANAGEMENT SYSTEM ---")
        print("1. 📋 List Tasks")
        print("2. 🆕 Add New Task")
        print("3. 📝 Update Task Status (Complete/Archive)")
        print("4. 🗑️ Delete Task")
        print("5. 🗂️ Category Management")
        print("6. 📈 Statistics & Reports")
        print("7. ➕ Add Subtask")
        print("8. 🚪 Backup & Exit")
        
        choice = input("\nYour Choice (1-8): ")

        if choice == "1":
            print(f"\n{'ID':<4} | {'TITLE':<20} | {'STATUS':<12} | {'PRIORITY':<8}")
            print("-" * 55)
            for t in all_tasks:
                status_icon = "✅" if t['status'] == "Completed" else "⏳"
                print(f"{t['id']:<4} | {t['title']:<20} | {status_icon} {t['status']:<9} | {t['priority']:<8}")
                for sub in t.get('subtasks', []):
                    sub_icon = "✔️" if sub['status'] == "Completed" else "○"
                    print(f"     └── {sub_icon} {sub['title']}")
        elif choice == "2":
            if not all_cats:
                print("⚠️  No categories found. Adding to 'General'.")
                selected_category = "General"
            else:
                print("\nSelect a category for this task:")
                for i, cat in enumerate(all_cats, 1):
                    print(f" {i}. {cat['name']}")
                
                try:
                    cat_idx = int(input("\nEnter category number: "))
                    if 1 <= cat_idx <= len(all_cats):
                        selected_category = all_cats[cat_idx - 1]['name']
                    else:
                        print("Invalid choice. Defaulting to 'General'.")
                        selected_category = "General"
                except ValueError:
                    print("Invalid input. Defaulting to 'General'.")
                    selected_category = "General"
            title = input("Task Title: ")
            desc = input("Description: ")
            priority = input("Priority (Low/Medium/High): ")
            due = input("Due Date (YYYY-MM-DD): ")
            
            new_t = task_ops.create_task(all_tasks, {
                "title": title, 
                "description": desc, 
                "priority": priority, 
                "due_date": due,
                "category": selected_category
            })
            
            activity.log_activity("data/activity.log", {
                "action": "CREATE", "task_id": new_t['id'], "summary": f"Added: {title}"
            })
            storage.save_state("data", all_tasks, all_cats, activity_log)
            print(f"📌 [ID: {new_t['id']}] {new_t['title']} (Status: {new_t['status']})")
        elif choice == "3":
            try:
                tid = input("Task ID to update: ")
                new_status = input("New Status (Pending/Completed/Archived): ")
                updated = task_ops.mark_task_status(all_tasks, tid, new_status)
                if updated:
                    activity.log_activity("data/activity.log", {
                        "action": "UPDATE", "task_id": tid, "summary": f"Status: {new_status}"
                    })
                    storage.save_state("data", all_tasks, all_cats, activity_log)
                    print("✔️ Status updated.")
                else:
                    print("❌ Task not found.")
            except ValueError:
                print("⚠️ Please enter a valid numerical ID.")

        elif choice == "4":
            if not all_cats:
                print("⚠️ No categories found. Please add a category first.")
                continue

            print("Select a category to view its tasks:")
            for idx, cat in enumerate(all_cats, 1):
                print(f"{idx}. {cat['name']}")

            try:
                cat_choice = int(input("\nEnter Category No: "))
                selected_cat_name = all_cats[cat_choice - 1]['name']
                filtered_tasks = [t for t in all_tasks if t.get('category') == selected_cat_name]

                if not filtered_tasks:
                    print(f"ℹ️ No tasks found in category '{selected_cat_name}'.")
                    continue
                print(f"\nTasks in '{selected_cat_name}':")
                print("-" * 30)
                for task in filtered_tasks:
                    print(f"ID: {task['id']} | Title: {task['title']}")
                print("-" * 30)
                tid = input("\nEnter Task ID to delete: ")

                task_exists_in_cat = any(str(t['id']) == str(tid) for t in filtered_tasks)

                if task_exists_in_cat:
                    confirm = input(f"Are you sure you want to delete Task {tid}? (Y/N): ")
                    if confirm.lower() == 'y':
                        if task_ops.delete_task(all_tasks, tid):
                            activity.log_activity("data/activity.log", {
                                "action": "DELETE", 
                                "task_id": tid, 
                                "summary": f"Task deleted from {selected_cat_name}"
                            })
                            storage.save_state("data", all_tasks, all_cats, activity_log)
                            print("🗑️ Task deleted.")
                        else:
                            print("❌ Unexpected error: Task could not be deleted.")
                    else:
                        print("Operation cancelled.")
                else:
                    print(f"❌ Task ID {tid} not found in category '{selected_cat_name}'.")

            except (ValueError, IndexError):
                print("⚠️ Please enter a valid number from the list.")

        elif choice == "5":
                if not all_cats:
                    print("No categories found.")
                else:
                    print(f"{'No':<4} | {'Category Name':<20}")
                    print("-" * 28)
                    for idx, cat in enumerate(all_cats, 1):
                        name = cat.get('name', 'Unknown')
                        print(f"{idx:<4} | {name:<20}")

                print("\n[A] Add New Category")
                print("[D] Delete Category")
                print("[B] Back to Main Menu")
                
                sub_choice = input("\nYour Choice: ").upper()
                
                if sub_choice == "B":
                    continue 
                
                elif sub_choice == "A":
                    cat_name = input("New Category Name: ")
                    new_cat = cat_ops.add_category(all_cats, {"name": cat_name})
                    if new_cat:
                        storage.save_state("data", all_tasks, all_cats, activity_log)
                        print(f"✔️ Category '{cat_name}' added.")
                
                elif sub_choice == "D":
                    if not all_cats:
                        print("❌ Nothing to delete.")
                        continue
                        
                    try:
                        idx_input = int(input("Enter the 'No' of the category to delete: "))
                        target_cat = all_cats[idx_input - 1]
                        target_id = target_cat['id']
                        target_name = target_cat['name']
                        success = cat_ops.delete_category(all_cats, target_id, all_tasks)
                        
                        if success:
                            storage.save_state("data", all_tasks, all_cats, activity_log)
                            print(f"🗑️ '{target_name}' deleted. Tasks moved to 'General'.")
                        else:
                            print("❌ Delete operation failed.")
                            
                    except (ValueError, IndexError):
                        print("⚠️ Invalid number! Please enter a number from the list above.")
        elif choice == "6":
            stats = activity.productivity_stats(all_tasks, activity_log)
            print(f"\n📊 PRODUCTIVITY REPORT")
            print(f"Total Tasks: {stats['total_tasks']}")
            print(f"Completed: {stats['completed_count']}")
            print(f"Efficiency Rate: %{stats['efficiency']:.2f}")

        elif choice == "7":
            print("\n--- Select a Category ---")
            for i, cat in enumerate(all_cats, 1):
                print(f"{i}) {cat['name']}")

            try:
                cat_idx = int(input("Select category number: ")) - 1
                selected_cat_name = all_cats[cat_idx]['name']
                filtered = [t for t in all_tasks if t['category'] == selected_cat_name]
                
                if not filtered:
                    print(f"❌ No tasks found in category '{selected_cat_name}'.")
                else:
                    print(f"\n--- Tasks in '{selected_cat_name}' ---")
                    for t in filtered:
                        print(f"ID: {t['id']} | Title: {t['title']}")
                    task_id = input("Enter the Parent Task ID: ")
                    parent_task = next((t for t in all_tasks if t['id'] == task_id), None)
                    if parent_task:
                        sub_title = input("Enter subtask title: ")
                        subtask_data = {
                            "title": sub_title,
                            "status": "Pending",
                            "created_at": datetime.now().isoformat()
                        }
                        updated_task = task_ops.add_subtask(all_tasks, task_id, subtask_data)
                        if updated_task:
                            activity_log.append(f"{datetime.now().isoformat()} | SUBTASK_ADDED | Task ID: {task_id} | Sub: {sub_title}")
                            storage.save_state("data", all_tasks, all_cats, activity_log)
                            print(f"✅ Subtask '{sub_title}' added to Task {task_id}!")
                    else:
                        print("❌ Parent Task ID not found!")
            except (ValueError, IndexError):
                print("⚠️ Invalid category selection!")

        elif choice == "8":
            storage.backup_state("data", "backups")
            print("💾 Data backed up. Goodbye!")
            break

if __name__ == "__main__":
    main()

import storage
import os
import tasks as task_ops
import categories as cat_ops
import activity
from datetime import datetime

def setup_folders():
    os.makedirs("data", exist_ok=True)
    os.makedirs("backups", exist_ok=True)
def display_summary(tasks):
    today = datetime.now().strftime("%Y-%m-%d")
    due_today = [t for t in tasks if t.get('due_date') == today and t['status'] != 'Completed']
    
    print("\n" + "="*45)
    print(f"📅 WELCOME! Today's Date: {today}")
    if due_today:
        print(f"🔔 You have {len(due_today)} task(s) due today!")
    else:
        print("✅ No urgent tasks for today.")
    print("="*45)

def main():
    all_tasks, all_cats, activity_log = storage.load_state("data")
    display_summary(all_tasks)

    while True:
        print("\n--- 🛠️ TASK MANAGEMENT SYSTEM ---")
        print("1. List Tasks")
        print("2. Add New Task")
        print("3. Update Task Status (Complete/Archive)")
        print("4. Delete Task")
        print("5. Category Management")
        print("6. Statistics & Reports")
        print("7. Backup & Exit")
        
        choice = input("\nYour Choice (1-7): ")

        if choice == "1":
            print(f"\n{'ID':<4} | {'TITLE':<20} | {'STATUS':<12} | {'PRIORITY':<8}")
            print("-" * 55)
            for t in all_tasks:
                status_icon = "✅" if t['status'] == "Completed" else "⏳"
                print(f"{t['id']:<4} | {t['title']:<20} | {status_icon} {t['status']:<9} | {t['priority']:<8}")

        elif choice == "2":
            title = input("Task Title: ")
            desc = input("Description: ")
            priority = input("Priority (Low/Medium/High): ")
            due = input("Due Date (YYYY-MM-DD): ")
            
            new_t = task_ops.create_task(all_tasks, {
                "title": title, "description": desc, 
                "priority": priority, "due_date": due
            })
            
            activity.log_activity("data/activity.log", {
                "action": "CREATE", "task_id": new_t['id'], "summary": f"Added: {title}"
            })
            storage.save_state("data", all_tasks, all_cats, activity_log)
            print("✔️ Task saved successfully.")

        elif choice == "3":
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

        elif choice == "4":
            tid = input("Task ID to delete: ")
            confirm = input(f"Are you sure you want to delete Task {tid}? (Y/N): ")
            if confirm.lower() == 'y':
                if task_ops.delete_task(all_tasks, tid):
                    activity.log_activity("data/activity.log", {
                        "action": "DELETE", "task_id": tid, "summary": "Task deleted"
                    })
                    storage.save_state("data", all_tasks, all_cats, activity_log)
                    print("🗑️ Task deleted.")
                else:
                    print("❌ Task not found.")

        elif choice == "5":
            cat_name = input("New Category Name: ")
            new_cat = cat_ops.add_category(all_cats, {"name": cat_name})
            if new_cat:
                storage.save_state("data", all_tasks, all_cats, activity_log)
                print(f"✔️ Category '{cat_name}' added.")
            else:
                print("❌ Category already exists.")

        elif choice == "6":
            stats = activity.productivity_stats(all_tasks, activity_log)
            print(f"\n📊 PRODUCTIVITY REPORT")
            print(f"Total Tasks: {stats['total_tasks']}")
            print(f"Completed: {stats['completed_count']}")
            print(f"Efficiency Rate: %{stats['efficiency']:.2f}")

        elif choice == "7":
            storage.backup_state("data", "backups")
            print("💾 Data backed up. Goodbye!")
            break
if __name__ == "__main__":
    main()
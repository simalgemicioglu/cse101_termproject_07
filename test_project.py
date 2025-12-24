import unittest
import os
import shutil
import tempfile
from datetime import datetime
import tasks as task_ops
import storage

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.tasks = []
        self.categories = []

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_create_task(self):
        task_data = {"title": "Test Task", "priority": "High"}
        new_task = task_ops.create_task(self.tasks, task_data)
        
        self.assertEqual(len(self.tasks), 1)
        self.assertEqual(new_task['title'], "Test Task")
        self.assertEqual(new_task['status'], "Pending")

    def test_filter_by_status(self):
        task_ops.create_task(self.tasks, {"title": "T1"})
        t2 = task_ops.create_task(self.tasks, {"title": "T2"})
        task_ops.mark_task_status(self.tasks, t2['id'], "Completed")
        completed_tasks = task_ops.filter_tasks(self.tasks, status="Completed")
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0]['title'], "T2")
    
    def test_backup_and_restoration(self):
        task_ops.create_task(self.tasks, {"title": "Backup Task"})
        storage.save_state(self.test_dir, self.tasks, self.categories, [])
        backup_dir = os.path.join(self.test_dir, "backups")

        created_backups = storage.backup_state(self.test_dir, backup_dir)

        self.assertTrue(len(created_backups) > 0, "Yedekleme listesi boş döndü!")
        zip_file_path = created_backups[0]
        self.assertTrue(os.path.exists(zip_file_path), f"Zip dosyası bulunamadı: {zip_file_path}")
        self.assertTrue(zip_file_path.endswith(".zip"))

if __name__ == '__main__':
    unittest.main()
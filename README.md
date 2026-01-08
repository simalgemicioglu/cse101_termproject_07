Python Term Project – To-Do & Task Management System.
This project is a terminal-based personal task management system developed in Python.

Setup & Installation
    To run this project, you only need Python 3.x installed on your computer:
        -Download the project folder.
        -Open your terminal and navigate to the project directory.
        -Run the application using the following command: python3 main.py

Project Structure
    The project is divided into modules to ensure clean and maintainable code:
        -main.py: The entry point of the program. It handles the user interface and menu navigation.
        -tasks.py: Manages the core logic for tasks, including creation, deletion, and subtask management.
        -categories.py: Handles the organization of tasks into different groups.
        -storage.py: Manages data persistence by saving and loading data in JSON format.
        -activity.py: Tracks user actions and calculates productivity statistics.

Usage Guide
    1 - 📋 List Tasks [View all tasks and their subtasks in a hierarchical list.]
    2 - 🆕 Add Task [Create a new task within a specific category.]
    3 - 📝 Update Status ["Change the status of a task (e.g., Pending to Completed)."]  
    4 - 🗑️ Delete Task [Remove a task from the system based on its category.]
    5 - 🗂️ Categories [Add new categories or delete existing ones.]
    6 - 📈 Statistics [View your total productivity and efficiency reports.]
    7 - ➕ Add Subtask [Add detailed sub-steps to an existing parent task.]
    8 - 🚪 Exit [Backup all data and safely close the program.]
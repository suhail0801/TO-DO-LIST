import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

class TodoList:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize tasks list
        self.tasks = []
        self.load_tasks()
        
        # Style configuration
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#2196F3")
        style.configure("TCheckbutton", background="#f0f0f0")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            self.main_frame,
            text="To-Do List",
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=20)
        
        # Task input frame
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(
            input_frame,
            textvariable=self.task_var,
            font=("Helvetica", 12),
            width=40
        )
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        add_button = ttk.Button(
            input_frame,
            text="Add Task",
            command=self.add_task
        )
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Tasks list frame
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create Treeview
        self.tree = ttk.Treeview(
            list_frame,
            columns=("Task", "Date", "Status"),
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.tree.heading("Task", text="Task")
        self.tree.heading("Date", text="Date Added")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Task", width=300)
        self.tree.column("Date", width=150)
        self.tree.column("Status", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        complete_button = ttk.Button(
            button_frame,
            text="Mark Complete",
            command=self.mark_complete
        )
        complete_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(
            button_frame,
            text="Delete Task",
            command=self.delete_task
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to add task
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Load existing tasks
        self.refresh_task_list()
        
    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.tasks.append({
                "task": task,
                "date": current_time,
                "status": "Pending"
            })
            self.task_var.set("")
            self.save_tasks()
            self.refresh_task_list()
        else:
            messagebox.showwarning("Warning", "Please enter a task!")
            
    def mark_complete(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            task_index = int(item_id[1:]) - 1
            if 0 <= task_index < len(self.tasks):
                self.tasks[task_index]["status"] = "Completed"
                self.save_tasks()
                self.refresh_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task!")
            
    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            task_index = int(item_id[1:]) - 1
            if 0 <= task_index < len(self.tasks):
                del self.tasks[task_index]
                self.save_tasks()
                self.refresh_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task!")
            
    def refresh_task_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add tasks to treeview
        for i, task in enumerate(self.tasks, 1):
            self.tree.insert(
                "",
                "end",
                iid=f"I{i}",
                values=(task["task"], task["date"], task["status"])
            )
            
    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)
            
    def load_tasks(self):
        try:
            if os.path.exists("tasks.json"):
                with open("tasks.json", "r") as f:
                    self.tasks = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading tasks: {str(e)}")
            self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoList(root)
    root.mainloop() 
from datetime import date
from task_service.connection import conn

def add_tasks(user_name: str, task_name: str, due_date: date, recurring: str = None):
    try:
        cursor = conn.cursor()
        if due_date >= date.today():
            cursor.execute("INSERT INTO tasks (user_name, task_name, due_date, status, repeat) VALUES (%s, %s, %s, 'pending', %s)", (user_name, task_name, due_date, recurring))
        else:
            raise ValueError("Due date cannot be in the past.")
    except Exception as e:
        print("Error adding task: ", e)
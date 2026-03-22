from datetime import date, timedelta
from task_service.connection import conn
import os
from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv('INFO_SCHEMA')

def delete_task(task_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM %s.tasks WHERE task_id = %s", (SCHEMA, task_id))
        cursor.close()
        conn.commit()
    except Exception as e:
        print("Error deleting task: ", e)

def deactivate_task(task_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id))
        task = cursor.fetchone()
        if task:
            cursor.execute("INSERT INTO %s.inactive_tasks (user_name, task_name, due_date, status, repeat, notify_at, category) VALUES (%s, %s, %s, %s, %s, %s, %s)", (SCHEMA, task[1], task[2], task[3], task[4], task[5], task[6], task[7]))
            cursor.execute("DELETE FROM %s.tasks WHERE task_id = %s", (SCHEMA, task_id))
            cursor.close()
            conn.commit()
        else:
            raise ValueError("Task not found.")
    except Exception as e:
        print("Couldn't deactivate task: ", e)
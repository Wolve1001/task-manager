from datetime import date, datetime
from task_service.connection import conn
import os
from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv('INFO_SCHEMA')

def add_tasks(user_name: str, task_name: str, due_date: date, recurring: str = None, notify_at: datetime = None, category: str = None):
    try:
        cursor = conn.cursor()
        if due_date >= date.today() and notify_at >= datetime.now().time("%H:%M:%S"):
            cursor.execute("INSERT INTO %s.tasks (user_name, task_name, due_date, status, repeat, notify_at, category) VALUES (%s, %s, %s, 'pending', %s, %s, %s)", (SCHEMA, user_name, task_name, due_date, recurring, notify_at, category))
        else:
            raise ValueError("Due date cannot be in the past.")
        cursor.close()
        conn.commit()
    except Exception as e:
        print("Error adding task: ", e)
from datetime import date, timedelta
from task_service.connection import conn
import os
from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv('INFO_SCHEMA')

def update_tasks(task_id: int, task_name: str, due_date: date = None, recurring: str = None):
    try:
        cursor = conn.cursor()
        if due_date >= date.today():
            cursor.execute("UPDATE %s.tasks SET task_name = %s, due_date = %s, recurring = %s WHERE task_id = %s", (SCHEMA, task_name, due_date, recurring, task_id))
        else:
            raise ValueError("Due date cannot be in the past.")
        cursor.close()
        conn.commit()
    except Exception as e:
        print("Error updating task: ", e)

def mark_task_done(task_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM %s.tasks WHERE task_id = %s", (SCHEMA, task_id))
        if cursor.fetchone() == 'pending':
            cursor.execute("UPDATE %s.tasks SET status = 'done' WHERE task_id = %s", (SCHEMA, task_id))
        else:
            raise ValueError("Task is already marked as done.")
        cursor.close()
        conn.commit()
    except Exception as e:
        print("Error marking task as done: ", e)

def recurring_task():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM %s.tasks WHERE repeat IS NOT NULL", (SCHEMA,))
        recurring_tasks = cursor.fetchall()
        for task in recurring_tasks:
            if task[5] == 'daily' and task[4] == 'done':
                new_due_date = task[3] + timedelta(days=1)
                cursor.execute("UPDATE %s.tasks SET status = 'pending', due_date = %s WHERE task_id = %s", (SCHEMA, new_due_date, task[0]))
            elif task[5] == 'weekly' and task[4] == 'done':
                new_due_date = task[3] + timedelta(days=7)
                cursor.execute("UPDATE %s.tasks SET status = 'pending', due_date = %s WHERE task_id = %s", (SCHEMA, new_due_date, task[0]))
        cursor.close()
        conn.commit()    
    except Exception as e:
        print("Error creating recurring task: ", e)
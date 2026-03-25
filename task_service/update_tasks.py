from datetime import date, timedelta
from task_service.connection import conn
import os
from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv('INFO_SCHEMA')

def update_task(task_id: int, task_name: str, due_date: date = None, recurring: str = None):
    try:
        cursor = conn.cursor()
        if due_date >= date.today():
            cursor.execute("UPDATE {SCHEMA}.tasks SET task_name = %s, due_date = %s, recurring = %s WHERE task_id = %s", (task_name, due_date, recurring, task_id))
        else:
            raise ValueError("Due date cannot be in the past.")
        
        cursor.execute("SELECT task_name FROM {SCHEMA}.tasks WHERE task_id = %s", (task_id))
        task_name = cursor.fetchone()[1]

        cursor.close()
        conn.commit()
        return {"message": "Task " + task_name + " updated successfully."}
    except Exception as e:
        print("Error updating task: ", e)

def mark_task_done(task_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM {SCHEMA}.tasks WHERE task_id = %s", (task_id))
        if cursor.fetchone() == 'pending':
            cursor.execute("UPDATE {SCHEMA}.tasks SET status = 'done' WHERE task_id = %s", (task_id))
        else:
            raise ValueError("Task is already marked as done.")
        
        cursor.execute("SELECT task_name FROM {SCHEMA}.tasks WHERE task_id = %s", (task_id))
        task_name = cursor.fetchone()[1]
        
        cursor.close()
        conn.commit()
        return {"message": "Task " + task_name + " marked as done."}
    except Exception as e:
        print("Error marking task as done: ", e)

def recurring_task():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM {SCHEMA}.tasks WHERE repeat IS NOT NULL")
        recurring_tasks = cursor.fetchall()
        for task in recurring_tasks:
            if task[5] == 'daily' and task[4] == 'done':
                new_due_date = task[3] + timedelta(days=1)
                cursor.execute("UPDATE {SCHEMA}.tasks SET status = 'pending', due_date = %s WHERE task_id = %s", (new_due_date, task[0]))
            elif task[5] == 'weekly' and task[4] == 'done':
                new_due_date = task[3] + timedelta(days=7)
                cursor.execute("UPDATE {SCHEMA}.tasks SET status = 'pending', due_date = %s WHERE task_id = %s", (new_due_date, task[0]))
        cursor.close()
        conn.commit()
        return {"message": "Recurring tasks updated successfully."}
    except Exception as e:
        print("Error creating recurring task: ", e)
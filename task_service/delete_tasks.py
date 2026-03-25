from datetime import date, timedelta
from task_service.connection import conn
import os
from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv('INFO_SCHEMA')

def delete_task(task_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT task_name FROM user_info.tasks WHERE task_id = %s", (task_id,))
        task_name = cursor.fetchone()[0]

        cursor.execute("DELETE FROM user_info.tasks WHERE task_id = %s", (task_id,))

        cursor.close()
        conn.commit()
        return {"message": "Task " + task_name + " deleted successfully."}
    except Exception as e:
        print("Error deleting task: ", e)

def deactivate_task(task_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id))
        task = cursor.fetchone()
        if task:
            cursor.execute("INSERT INTO {SCHEMA}.inactive_tasks (user_name, task_name, due_date, status, repeat, notify_at, category) VALUES (%s, %s, %s, %s, %s, %s, %s)", (task[1], task[2], task[3], task[4], task[5], task[6], task[7]))
            cursor.execute("DELETE FROM {SCHEMA}.tasks WHERE task_id = %s", (task_id))
        else:
            raise ValueError("Task not found.")
        
        cursor.execute("SELECT task_name FROM {SCHEMA}.tasks WHERE task_id = %s", (task_id))
        task_name = cursor.fetchone()[1]
        
        cursor.close()
        conn.commit()
        return {"message": "Task " + task_name + " deactivated successfully."}
    except Exception as e:
        print("Couldn't deactivate task: ", e)
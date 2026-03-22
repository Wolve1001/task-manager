from datetime import date, timedelta
from task_service.connection import conn

def update_tasks(task_id: int, task_name: str, due_date: date = None, recurring: str = None):
    try:
        cursor = conn.cursor()
        if due_date >= date.today():
            cursor.execute("UPDATE tasks SET task_name = %s, due_date = %s, recurring = %s WHERE task_id = %s", (task_name, due_date, recurring, task_id))
        else:
            raise ValueError("Due date cannot be in the past.")
        cursor.commit()
    except Exception as e:
        print("Error updating task: ", e)

def mark_task_done(task_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM tasks WHERE task_id = %s", (task_id))
        if cursor.fetchone()[4] == 'pending':
            cursor.execute("UPDATE tasks SET status = 'done' WHERE task_id = %s", (task_id))
        else:
            raise ValueError("Task is already marked as done.")
        cursor.commit()
    except Exception as e:
        print("Error marking task as done: ", e)

def recurring_task():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE repeat IS NOT NULL;")
        recurring_tasks = cursor.fetchall()
        for task in recurring_tasks:
            if task[5] == 'daily' and task[4] == 'done':
                new_due_date = task[3] + timedelta(days=1)
                cursor.execute("UPDATE tasks SET status = 'pending', due_date = %s WHERE task_id = %s", (new_due_date, task[0]))
            elif task[5] == 'weekly' and task[4] == 'done':
                new_due_date = task[3] + timedelta(days=7)
                cursor.execute("UPDATE tasks SET status = 'pending', due_date = %s WHERE task_id = %s", (new_due_date, task[0]))
    except Exception as e:
        print("Error creating recurring task: ", e)
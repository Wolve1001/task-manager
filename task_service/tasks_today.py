from task_service.connection import conn
from datetime import date, datetime
import os
from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv('INFO_SCHEMA')

def task_today(user_name: str, sort: str = None):
    try:
        cursor = conn.cursor()
        date = date.today()
        if sort == "desc":
            cursor.execute("SELECT * FROM %s.tasks WHERE user_name = %s AND due_date = %s AND status = 'pending' ORDER BY due_date DESC", (SCHEMA, user_name, date))
        else:
            cursor.execute("SELECT * FROM %s.tasks WHERE user_name = %s AND due_date = %s AND status = 'pending' ORDER BY due_date", (SCHEMA, user_name, date))
        tasks_rem_today = cursor.fetchall()

        if tasks_rem_today:
            print("Tasks due for today: ")
            for task in tasks_rem_today:
                print("Task: " + task[1] + ", Due_By: " + str(task[3]))
        else:
            print("All tasks are completed.")
        
        cursor.execute("SELECT * FROM %s.tasks WHERE user_name = %s AND due_date = %s AND status = 'done'", (SCHEMA, user_name, date))
        tasks_done_today = cursor.fetchall()

        if tasks_done_today:
            print("Tasks completed today: ")
            for task in tasks_done_today:
                print("Task: " + task[1])
        else:
            raise ValueError("No tasks added today.")
    except Exception as e:
        print("Error fetching tasks: ", e)

def task_by_notification(user_name: str, notify_at: datetime, sort: str = None);
    try:
        cursor = conn.cursor()
        date = date.today()
        if sort == "desc":
            cursor.execute("SELECT * FROM %s.tasks WHERE user_name = %s AND notify_at = %s AND due_date = %s ORDER BY notify_at DESC", (SCHEMA, user_name, notify_at, date))
        else:
            cursor.execute("SELECT * FROM %s.tasks WHERE user_name = %s AND notify_at = %s AND due_date = %s ORDER BY notify_at", (SCHEMA, user_name, notify_at, date))
        tasks_notify_today = cursor.fetchall()

        if tasks_notify_today:
            print("Tasks to be notified about today: ")
            for task in tasks_notify_today:
                print("Task: " + task[1] + ", Notify At: " + str(task[6]))
        else:
            raise ValueError("No tasks to notify about today.")
    except Exception as e:
        print("Error fetching tasks: ", e)

def task_by_category(user_name: str, category: str, sort: str = None):
    try:
        cursor = conn.cursor()
        date = date.today()
        if sort == "desc":
            cursor.execute("SELECT * FROM %s.tasks WHERE user_name = %s AND category = %s AND due_date = %s ORDER BY due_date DESC", (SCHEMA, user_name, category, date))
        else:
            cursor.execute("SELECT * FROM %s.tasks WHERE user_name = %s AND category = %s AND due_date = %s ORDER BY due_date", (SCHEMA, user_name, category, date))
        tasks = cursor.fetchall()

        for task in tasks:
            print("Task: " + task[1] + ", Due By: " + str(task[3]) + ", Category: " + task[7])
    except Exception as e:
        print("Error fetching tasks: ", e)
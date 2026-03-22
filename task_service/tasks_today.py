from task_service.connection import conn
from datetime import date

def task_today(user_name: str, date: date):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_name = %s AND due_date = %s AND status = 'pending'", (user_name, date))
        tasks_rem_today = cursor.fetchall()

        if tasks_rem_today:
            print("Tasks due for today: ")
            for task in tasks_rem_today:
                print("Task: " + task[1] + ", Due_By: " + str(task[3]))
        else:
            print("All tasks are completed.")
        
        cursor.execute("SELECT * FROM tasks WHERE user_name = %s AND due_date = %s AND status = 'done'", (user_name, date))
        tasks_done_today = cursor.fetchall()

        if tasks_done_today:
            print("Tasks completed today: ")
            for task in tasks_done_today:
                print("Task: " + task[1])
        else:
            raise ValueError("No tasks added today.")
    except Exception as e:
        print("Error fetching tasks: ", e)
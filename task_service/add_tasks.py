from datetime import date, datetime
from connection import connect_db

async def add_task(user_name: str, task_name: str, due_date: date, recurring: str = None, notify_at: datetime = None, category: str = None):
    try:
        conn = await connect_db()
        cursor = await conn.cursor()
        if due_date >= date.today() and notify_at.time() > datetime.now().time():
            cursor.execute("INSERT INTO tasks (user_name, task_name, due_date, status, repeat, notify_at, category) VALUES (%s, %s, %s, 'pending', %s, %s, %s)", (user_name, task_name, due_date, recurring, notify_at, category))
        else:
            raise ValueError("Due date cannot be in the past.")
        await cursor.close()
        await conn.commit()
        return {"message": "Task " + task_name + " added successfully."}
    except Exception as e:
        print("Error adding task: ", e)
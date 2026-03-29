from datetime import date, timedelta
from connection import connect_db

async def update_task(task_id: int, task_name: str, due_date: date = None, recurring: str = None):
    try:
        conn = await connect_db()
        cursor = await conn.cursor()
        if due_date >= date.today():
            await cursor.execute("UPDATE user_info.tasks SET task_name = %s, due_date = %s, recurring = %s WHERE task_id = %s", (task_name, due_date, recurring, task_id))
        else:
            raise ValueError("Due date cannot be in the past.")
        
        await cursor.execute("SELECT task_name FROM user_info.tasks WHERE task_id = %s", (task_id))
        task_name = (await cursor.fetchone())[0]

        await cursor.close()
        await conn.commit()
        return {"message": "Task " + task_name + " updated successfully."}
    except Exception as e:
        print("Error updating task: ", e)

async def mark_task_done(task_id: int):
    try:
        conn = await connect_db()
        cursor = await conn.cursor()
        await cursor.execute("SELECT status FROM user_info.tasks WHERE task_id = %s", (task_id))
        if await cursor.fetchone() == 'pending':
            await cursor.execute("UPDATE user_info.tasks SET status = 'done' WHERE task_id = %s", (task_id))
        else:
            raise ValueError("Task is already marked as done.")
        
        await cursor.execute("SELECT task_name FROM user_info.tasks WHERE task_id = %s", (task_id))
        task_name = (await cursor.fetchone())[0]
        
        await cursor.close()
        await conn.commit()
        return {"message": "Task " + task_name + " marked as done."}
    except Exception as e:
        print("Error marking task as done: ", e)

async def recurring_task():
    try:
        conn = await connect_db()
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM user_info.tasks WHERE repeat IS NOT NULL")
        recurring_tasks = await cursor.fetchall()
        for task in recurring_tasks:
            if task[5] == 'daily' and task[4] == 'done':
                new_due_date = task[3] + timedelta(days=1)
                await cursor.execute("UPDATE user_info.tasks SET status = 'pending', due_date = %s WHERE task_id = %s", (new_due_date, task[0]))
            elif task[5] == 'weekly' and task[4] == 'done':
                new_due_date = task[3] + timedelta(days=7)
                await cursor.execute("UPDATE user_info.tasks SET status = 'pending', due_date = %s WHERE task_id = %s", (new_due_date, task[0]))
        await cursor.close()
        await conn.commit()
        return {"message": "Recurring tasks updated successfully."}
    except Exception as e:
        print("Error creating recurring task: ", e)
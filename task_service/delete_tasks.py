from connection import connect_db

async def delete_task(task_id: int):
    try:
        conn = await connect_db()
        cursor = await conn.cursor()
        await cursor.execute("SELECT task_name FROM tasks WHERE task_id = %s", (task_id,))
        task_name = await cursor.fetchone()[0]

        await cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))

        await cursor.close()
        await conn.commit()
        return {"message": "Task " + task_name + " deleted successfully."}
    except Exception as e:
        print("Error deleting task: ", e)

async def deactivate_task(task_id: int):
    try:
        conn = await connect_db()
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id, ))
        task = await cursor.fetchone()
        if task:
            await cursor.execute("INSERT INTO inactive_tasks (task_id, user_name, task_name, due_date, status, repeat, notify_at, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (task_id, task[1], task[2], task[3], task[4], task[5], task[6], task[7]))
            await cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id, ))
        else:
            raise ValueError("Task not found.")

        task_name = task[2]
        
        await cursor.close()
        await conn.commit()
        return {"message": "Task " + task_name + " deactivated successfully."}
    except Exception as e:
        print("Couldn't deactivate task: ", e)
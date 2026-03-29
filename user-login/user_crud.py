from datetime import date
from connection import connect_db
import bcrypt


async def add_user(user_name: str, password: str):
    try:
        hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        created_at = date.today()

        conn = await connect_db()
        cursor = await conn.cursor()
        await cursor.execute("SELECT count(*) FROM platform_users WHERE user_name = %s", (user_name, ))
        if await cursor.fetchone()[0] > 0:
            raise ValueError("Username already exists.")
        
        await cursor.execute("INSERT INTO platform_users (user_name, password, created_at, status) VALUES (%s, %s, %s, 'active')", (user_name, hashed_pass, created_at))
        await cursor.close()
        await conn.commit()
    except Exception as e:
        print("Error adding user: ", e)

async def get_user(find_user: str, self_user: str):
    try:
        conn = await connect_db()
        cursor = await conn.cursor()
        if self_user == 'admin':
            await cursor.execute("SELECT * FROM platform_users WHERE user_name = %s", (find_user,))
            user = await cursor.fetchone()
            await cursor.close()
            await conn.commit()
            return {
            "user": [
                {"user_id": user[0], "user_name": user[1], "created_at": str(user[3]), "status": user[4]} 
            ]}
        else:
            await cursor.close()
            await conn.commit()
            raise ValueError("Only admin can access user information.")
    except Exception as e:
        print("Error fetching user: ", e)

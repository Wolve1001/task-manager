import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_SCHEMA = os.getenv('INFO_SCHEMA')

async def connect_db() -> asyncpg.Connection:
    try:
        conn = await asyncpg.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                server_settings={'search_path': DB_SCHEMA})
        print("Database connected successfully")
        return conn
    except Exception as e:
        print("Database not connected successfully")
        print(e)
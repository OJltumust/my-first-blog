import datetime
import sqlite3
import sys
import pathlib
import datetime
import logging
import asyncio
import time

from aiogram import Bot, Dispatcher, executor, types
script_path = pathlib.Path(sys.argv[0]).parent

TOKEN = "5689103411:AAFNxmYASblnCK76THumwm_UIz3FJ6ixXoM"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

conn = sqlite3.connect(script_path / 'test_db0.db', check_same_thread=False)
cursor = conn.cursor()
print("gjldr.xty")


def table_to(user_id: int, user_name: str, joining_date):
    sqlite_insert_query = """INSERT INTO sqlitedb_developers (user_id, user_name, joining_date) VALUES (?, ?, ?)"""
    data = (user_id, user_name, joining_date)
    cursor.execute(sqlite_insert_query, data)
    print("Добавлено")
    conn.commit()

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    joining_date = time.asctime()

    await message.answer("Привет, " + user_name)

    table_to(user_id, user_name, joining_date)

if __name__ == "__main__":
    executor.start_polling(dp)
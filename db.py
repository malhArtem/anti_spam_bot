import datetime
import sqlite3
from aiogram import types


async def make_table(db: sqlite3.Connection):
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT, chat_id TEXT, username TEXT, time TEXT, count INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS spammers (user_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS chats (chat_id TEXT)")
    db.commit()
    cur.close()


async def add_chat(chat_id, db: sqlite3.Connection):
    cur = db.cursor()
    cur.execute("SELECT 1 FROM chats WHERE chat_id = ?",
                (str(chat_id),))
    if cur.fetchone():
        cur.close()
        return 0

    cur.execute("INSERT INTO chats VALUES(?)"
                , (chat_id,))
    db.commit()
    cur.close()
    return 1


async def get_chats(db: sqlite3.Connection):
    cur = db.cursor()
    cur.execute("SELECT DISTINCT * FROM chats ")
    chats = cur.fetchall()
    cur.close()
    return chats


async def delete_chat(chat_id, db: sqlite3.Connection):
    cur = db.cursor()

    cur.execute("DELETE FROM chats WHERE chat_id = ?"
                , (chat_id,))
    db.commit()
    cur.close()
    return 1


async def get_user(user_id, chat_id, db: sqlite3.Connection):
    cur = db.cursor()
    cur.execute("SElECT * FROM users WHERE user_id= ? and chat_id = ?", (str(user_id), str(chat_id)))

    user = cur.fetchone()

    cur.close()
    return user


async def delete_user_username(username, chat_id, db: sqlite3.Connection):
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE username = ? and chat_id = ?", (str(username), str(chat_id)))
    db.commit()
    cur.close()


async def add_new_user(message: types.Message, db: sqlite3.Connection):
    cur = db.cursor()
    time = datetime.datetime.now()

    cur.execute("SELECT 1 FROM users WHERE user_id = ? and chat_id = ? ", (str(message.from_user.id), str(message.chat.id)))
    if cur.fetchone():
        print(1)
        cur.close()
        return 0

    print(0)
    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)"
                , (message.from_user.id, message.chat.id, message.from_user.username, time, 0))
    db.commit()
    cur.close()
    return 1


async def add_old_user(message: types.Message, db: sqlite3.Connection):
    cur = db.cursor()
    time = datetime.datetime.now()

    cur.execute("SELECT 1 FROM users WHERE user_id = ? and chat_id = ? ", (str(message.from_user.id), str(message.chat.id)))
    if cur.fetchone():
        return 0

    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)"
                , (message.from_user.id, message.chat.id, message.from_user.username, time, 1))
    db.commit()
    cur.close()
    return 1


async def update_count(user_id, chat_id, db: sqlite3.Connection):
    cur = db.cursor()
    cur.execute("UPDATE users SET count = 1 WHERE user_id = ? and chat_id = ?", (str(user_id), str(chat_id)))
    db.commit()
    cur.close()


async def delete_user(user_id, chat_id, db: sqlite3.Connection):
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE user_id = ? and chat_id = ?", (str(user_id), str(chat_id)))
    db.commit()
    cur.close()

import asyncio
import datetime

from aiogram import types, Router, Bot, F
import sqlite3

from aiogram.exceptions import TelegramRetryAfter
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, Command

from db import add_old_user, get_user, add_new_user, delete_user, update_count, delete_user_username, add_chat, \
    delete_chat, get_chats


admins_id = '517922464'

router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


# @router.message(ChatMemberF)
# async def new_user(message: types.Message, db: sqlite3.connect()):
#     await add_new_user(message, db)

@router.message(Command("send_all"))
async def send_all(message: types.Message, db: sqlite3.Connection):
    if str(message.from_user.id) != admins_id:
        return 0

    if message.reply_to_message:
        chats = await get_chats(db)
        print(chats)
        for chat in chats:
            print(chat[0])

            try:
                await message.reply_to_message.send_copy(chat[0])

            except TelegramRetryAfter:
                await asyncio.sleep(3)
                await message.reply_to_message.send_copy(chat[0])

            except Exception:
                pass

        print("Рассылка завершена")
    else:
        "Ответьте на сообщение"


@router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def add_to_chat(event: types.ChatMemberUpdated, db: sqlite3.Connection):
    await add_chat(event.chat.id, db)


@router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def delete_from_chat(event: types.ChatMemberUpdated, db: sqlite3.Connection):
    await delete_chat(event.chat.id, db)


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_user(message: types.ChatMemberUpdated, db: sqlite3.Connection):
    print(message.from_user.username)
    await add_new_user(message, db)


@router.message()
async def messages(message: types.Message, db: sqlite3.connect):
    # await add_old_user(message, db)
    user = await get_user(message.from_user.id, message.chat.id, db)
    if user is None:
        return 0

    user_time = datetime.datetime.strptime(user[3], '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.datetime.now()
    delta = now - user_time
    if delta > datetime.timedelta(hours=12) and user[4]:
        await delete_user(message.from_user.id, message.chat.id, db)
        return 0

    if message.entities is not None:
        entities = message.entities
        print(entities)
        for entity in entities:
            if entity.type == "url" or entity.type == "text_link":
                await message.delete()
                return 0

    if message.forward_from_chat is not None:
        print(message.forward_from_chat)
        if message.forward_from_chat.id != message.chat.id:
            await message.delete()
            return 0

    if message.forward_from is not None:
        await message.delete()

    if not user[4]:
        if delta > datetime.timedelta(hours=12):
            await delete_user(message.from_user.id, message.chat.id, db)

        else:
            await update_count(message.from_user.id, message.chat.id, db)



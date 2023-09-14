import asyncio
import sqlite3

from aiogram import types, Router
from aiogram.exceptions import TelegramRetryAfter
from aiogram.filters import BaseFilter, Command

from db import delete_user, delete_user_username, get_chats
from main import admins_id

router = Router()


class IsAdmin(BaseFilter):  # [1]
    async def __call__(self, message: types.Message) -> bool:  # [3]
        if isinstance(message, types.CallbackQuery):
            member = await message.bot.get_chat_member(message.message.chat.id, message.from_user.id)
        else:
            member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return (isinstance(member, types.ChatMemberAdministrator) and member.can_promote_members) or isinstance(member, types.ChatMemberOwner)




router.message.filter(IsAdmin())


@router.message(Command("allow"))
async def allow_cmd(message: types.Message, db: sqlite3.Connection):
    if message.reply_to_message is not None:
        await delete_user(message.reply_to_message.from_user.id, message.reply_to_message.chat.id, db)

    elif message.entities is not None:
        for entity in message.entities:
            if entity.type == "mention" or entity.type == "text_mention":
                username = entity.extract_from(message.text)[1:]
                await delete_user_username(username, message.chat.id, db)

    else:
        await message.reply("Укажите пользователя")
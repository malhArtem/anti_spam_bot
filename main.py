from aiogram import types, Dispatcher, Bot
import sqlite3
import logging
import asyncio
from handlers import router
from db import make_table
import admins_cmd


token ='6542193322:AAFgPrerO029NYGSJOhq5r1rv-sgNEOYRWs'
admins_id = '517922464'


async def on_startup(bot: Bot):
    await bot.send_message(admins_id, "Бот запущен")


async def main():
    db = sqlite3.connect("anti_spam.db")
    await make_table(db)

    bot = Bot(token)
    dp = Dispatcher()
    dp.include_router(admins_cmd.router)
    dp.include_router(router)

    dp.startup.register(on_startup)
    await dp.start_polling(bot, db=db)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    asyncio.run(main())

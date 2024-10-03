from asyncio import run
# import logging

from aiogram.types import BotCommand

from handler import router, dp, bot


async def start():
    try:
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Ishga tushirish"),
                BotCommand(command="admin", description="Admin bilan bo'glanish"),
            ]
        )
        dp.include_router(router=router)
        await dp.start_polling(bot)
    except Exception as e:
        print("Xatolik mavjud: ", e)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        # logging.basicConfig(level=logging.INFO)
        run(start())
    except KeyboardInterrupt:
        print("Dastur to'xtatildi!")

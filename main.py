import asyncio
import aiogram
import os
import logging
import sys

logging.basicConfig(level=logging.INFO)

async def main():
    TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
    if TELEGRAM_API_TOKEN is None:
        logging.error("Environment variable TELEGRAM_API_TOKEN is not defined")
        sys.exit(-1)

    bot = aiogram.Bot(token = TELEGRAM_API_TOKEN)
    dispatcher = aiogram.Dispatcher(bot)

    @dispatcher.message_handler(commands=["start", "help"])
    async def send_start(message: aiogram.types.Message):
        bot_name = (await bot.get_me()).full_name
        user_name = message.from_user.full_name
        await message.answer(f"Hello, {user_name}! My name is {bot_name}.\n\n"
                        "Right now I can't do many things but very soon "
                        "I will do the following:\n\n"

                        "* Every day I will send you piece of misical score.\n"
                        "* You can play this piece using your favourite musical instrument or sing it.\n"
                        "* You can send recording of your performance to me and\n"
                        "* I will send it to random user (I will not mention your name or alias, no worries).\n"
                        "* This random user (if he will be generous enough) will provide a feedback for"
                        "your performance and I will share it to you.\n")

    logging.info("Starting bot")
    await dispatcher.start_polling()

if __name__ == "__main__":
    asyncio.run(main())

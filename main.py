import asyncio
from bot.bot import DailyGuitarBot
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

    bot = DailyGuitarBot(TELEGRAM_API_TOKEN)

    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot terminated from the keyboard")
        sys.exit(0)

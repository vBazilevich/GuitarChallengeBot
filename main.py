import asyncio
from bot.bot import DailyGuitarBot
from bot.ImagesStorage import ImagesStorage
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

    MONGO_URL = os.getenv("MONGO_URL")
    if MONGO_URL is None:
        logging.error("Environment variable MONGO_URL is not defined")
        sys.exit(-1)
    images_storage = ImagesStorage(MONGO_URL)

    ADMIN_ID = os.getenv("ADMIN_ID")
    if ADMIN_ID is None:
        logging.warn(
                "Environment variable ADMIN_ID is missing. All errors will be logged"
        )

    bot = DailyGuitarBot(TELEGRAM_API_TOKEN, images_storage)

    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot terminated from the keyboard")
        sys.exit(0)

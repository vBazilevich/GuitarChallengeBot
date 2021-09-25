import asyncio
from bot.userstorage.userstorage import UserStorage
import os
import logging
import sys
import pymongo
from bot.bot import DailyGuitarBot
from bot.ImagesStorage import ImagesStorage

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
    mongo_db = pymongo.MongoClient(MONGO_URL, connect=True)
    # Check that connection was established
    try:
        mongo_db.admin.command('ping')
    except pymongo.errors.ConnectionFailure:
        logging.error("Can not establish connection with MongoDB")
        sys.exit(-1)
    images_storage = ImagesStorage(mongo_db)

    ADMIN_ID = os.getenv("ADMIN_ID")
    if ADMIN_ID is None:
        logging.warn(
          "Environment variable ADMIN_ID is missing. All errors will be logged"
        )

    # Create UserStorage
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL is None:
        logging.error("PostgreSQL database was not provided")
        sys.exit(-1)
    user_storage = UserStorage(DATABASE_URL)

    bot = DailyGuitarBot(TELEGRAM_API_TOKEN, images_storage, user_storage)

    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot terminated from the keyboard")
        sys.exit(0)

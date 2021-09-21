from bot.userstorage.userstorage import UserStorage
from bot.Schedule import Schedule
from bot.MissingTokenError import MissingTokenError
from bot.ImagesStorage import ImagesStorage, LevelDoesNotExistError
import aiogram
import logging
import os


class DailyGuitarBot:
    schedule_storage = {}

    def __init__(self, token, images_storage: ImagesStorage, user_storage: UserStorage):
        if token is None:
            raise MissingTokenError("Telegram API token passed "
                                    "to bot class is None")
        self.bot = aiogram.Bot(token)
        self.dispatcher = aiogram.Dispatcher(self.bot)
        self.images_storage = images_storage
        self.user_storage = user_storage
        self.admin_id = os.getenv("ADMIN_ID")

        @self.dispatcher.message_handler(commands=["start", "help"])
        async def send_start(message: aiogram.types.Message):
            bot_name = (await self.bot.get_me()).full_name
            user_name = message.from_user.full_name
            user_id = message.from_user.id
            if not self.user_storage.user_exists(user_id):
                self.user_storage.create_user(user_id)
            await message.answer(
                f"Hello, {user_name}! My name is {bot_name}.\n\n"
                "Right now I can't do many things but very soon "
                "I will do the following:\n\n"

                "* Every day I will send you piece of misical score.\n"
                "* You can play this piece using your favourite musical "
                "instrument or sing it.\n"
                "* You can send recording of your performance to me and\n"
                "* I will send it to random user (I will not"
                " mention your name or alias, no worries).\n"
                "* This random user (if he will be generous enough) "
                "will provide a feedback for "
                "your performance and I will share it to you.\n"
            )

        @self.dispatcher.message_handler(commands=["set_schedule"])
        async def set_schedule(message: aiogram.types.Message):
            try:
                schedule = Schedule(message.get_args())
                self.schedule_storage[message.from_user.id] = schedule
                logging.debug("Registered new schedule: {schedule}")
                await message.answer(
                    "You schedule was updated. "
                    f"Your current schedule is: {schedule}"
                )
            except Exception as e:
                await message.answer(str(e))

        @self.dispatcher.message_handler(commands=["my_schedule"])
        async def my_schedule(message: aiogram.types.Message):
            try:
                schedule = self.schedule_storage[message.from_user.id]
                await message.answer(f"Your current schedule is: {schedule}")
            except KeyError:
                await message.answer(
                        "You have not chosen your schedule. "
                        "Please, use /set_schedule commant to configure it."
                )

        @self.dispatcher.message_handler(commands=["next"])
        async def next(message: aiogram.types.Message):
            user_id = message.from_user.id
            try:
                user_info = self.user_storage[user_id]
                current_level = user_info["level"]
                image = self.images_storage.level(current_level)
                await message.reply_photo(image)
                self.user_storage[user_id]["level"] += 1

            except KeyError:
                await message.answer(
                    "You are not registered. Please, use /start command first"
                )
            except LevelDoesNotExistError as e:
                await message.answer(e)
                logging.warn("At least one user passed all levels.")
                if self.admin_id:
                    await self.bot.send_message(
                        self.admin_id,
                        "One user passed all levels.",
                    )
        
        @self.dispatcher.message_handler(commands=["reset"])
        async def reset(message: aiogram.types.Message):
            user_id = message.from_user.id
            try:
                self.user_storage[user_id]["level"] = 1
                await message.answer("Progress resetted successfully")
            except KeyError:
                await message.answer("Can't reset progress for unregistered user")

    # Starts bot
    async def start(self):
        logging.info("Starting bot...")
        await self.dispatcher.start_polling()

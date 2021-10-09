import logging
import os
import aiogram
from bot.userstorage.updatingnonexistingusererror import UpdatingNonExistingUserError
from bot.userstorage.userstorage import UserStorage
from bot.schedule import Schedule
from bot.schedule import HoursOutOfRangeError, StartAfterEndError, WrongScheduleFormat
from bot.missingtokenerror import MissingTokenError
from bot.imagesstorage import ImagesStorage, LevelDoesNotExistError


class DailyGuitarBot:
    """
    Implements main Bot logic
    """
    def __init__(self, token: str, images_storage: ImagesStorage, user_storage: UserStorage):
        """
        :param token: Telegram API token
        :param images_storage: ImagesStorage object containing music scores
        :param user_storage: UserStorage object that stores and manages information about users
        :raises:
            MissingTokenError: no telegram token provided
        """
        if token is None:
            raise MissingTokenError("Telegram API token passed "
                                    "to bot class is None")
        self.bot = aiogram.Bot(token)
        self.dispatcher = aiogram.Dispatcher(self.bot)
        self.images_storage = images_storage
        self.user_storage = user_storage
        self.admin_id = os.getenv("ADMIN_ID")

        self.dispatcher.register_message_handler(self.send_start, commands=['start'])
        self.dispatcher.register_message_handler(self.help, commands=["help"])
        self.dispatcher.register_message_handler(self.set_schedule, commands=['set_schedule'])
        self.dispatcher.register_message_handler(self.my_schedule, commands=['my_schedule'])
        self.dispatcher.register_message_handler(self.next, commands=['next'])
        self.dispatcher.register_message_handler(self.reset, commands=['reset'])

    async def send_start(self, message: aiogram.types.Message):
        """
        Handles /start command
        :param message: message from user
        """
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

    async def help(self, message: aiogram.types.Message):
        await message.answer(
                "Here is the list of all supported commands:\n"
                "/start - register as a new user. Get description of the bot\n"
                "/set_schedule - set time interval when you can be asked for a review\n"
                "/my_schedule - check your current schedule\n"
                "/next - proceed to the next level\n"
                "/reset - reset your current progress\n"
                "/help - read this help message")

    async def set_schedule(self, message: aiogram.types.Message):
        """
        Handles /set_schedule command - updates user schedule
        :param message: message from user
        """
        try:
            schedule = Schedule.from_string(message.get_args())
            user_id = message.from_user.id
            self.user_storage.update_user_schedule(user_id, schedule)
            logging.debug("Registered new schedule: {schedule}")
            await message.answer(
                "You schedule was updated. "
                f"Your current schedule is: {schedule}"
            )
        except (ValueError, WrongScheduleFormat, HoursOutOfRangeError, StartAfterEndError) as e:
            await message.answer(str(e))

    async def my_schedule(self, message: aiogram.types.Message):
        """
        Handles /my_schedule command - sends to user his or her current schedule
        :param message: message from user
        """
        try:
            schedule = self.user_storage.get_user_schedule(message.from_user.id)
            await message.answer(f"Your current schedule is: {schedule}")
        except KeyError:
            await message.answer(
                    "You have not chosen your schedule. "
                    "Please, use /set_schedule commant to configure it."
            )

    async def next(self, message: aiogram.types.Message):
        """
        Handles /next command - sends next level to user
        """
        user_id = message.from_user.id
        try:
            current_level = self.user_storage.get_user_level(user_id)[0]
            logging.debug(f"UID: {user_id} LEVEL: {current_level}")
            image = self.images_storage.level(current_level)
            await message.reply_photo(image)
            self.user_storage.update_user_level(user_id)

        except UpdatingNonExistingUserError:
            await message.answer(
                "You are not registered. Please, use /start command first"
            )
        except LevelDoesNotExistError as e:
            await message.answer(e)
            logging.warning("At least one user passed all levels.")
            if self.admin_id:
                await self.bot.send_message(
                    self.admin_id,
                    "One user passed all levels.",
                )

    async def reset(self, message: aiogram.types.Message):
        """
        Handles /reset command - return user to level 1
        """
        user_id = message.from_user.id
        try:
            self.user_storage.reset_user_progress(user_id)
            await message.answer("Progress resetted successfully")
        except KeyError:
            await message.answer("Can't reset progress for unregistered user")

    async def start(self):
        """
        Starts the bot
        """
        logging.info("Starting bot...")
        await self.dispatcher.start_polling()

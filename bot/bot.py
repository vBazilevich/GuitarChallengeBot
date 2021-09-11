from bot.Schedule import Schedule, WrongScheduleFormat
from bot.MissingTokenError import MissingTokenError
import aiogram
import logging

class DailyGuitarBot:
    schedule_storage = dict()
    def __init__(self, token):
        if token is None:
            raise MissingTokenError("Telegram API token passed to bot class is None")
        self.bot = aiogram.Bot(token)
        self.dispatcher = aiogram.Dispatcher(self.bot)

        @self.dispatcher.message_handler(commands=["start", "help"])
        async def send_start(message: aiogram.types.Message):
            bot_name = (await self.bot.get_me()).full_name
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

        @self.dispatcher.message_handler(commands=["set_schedule"])
        async def set_schedule(message: aiogram.types.Message):
            try:
                schedule = Schedule(message.get_args())
                self.schedule_storage[message.from_user.id] = schedule
                logging.debug(f"Registered new schedule: {self.schedule_storage[message.from_user.id]}")
                await message.answer(f"You schedule was updated. Your current schedule is: {schedule}")
            except Exception as e:
                await message.answer(str(e))

    # Starts bot
    async def start(self):
        logging.info("Starting bot...")
        await self.dispatcher.start_polling()

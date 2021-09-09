import aiogram
import logging

class DailyGuitarBot:
    schedule_storage = dict()
    def __init__(self, token):
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
                timezone, start, end = self.parse_schedule(message.get_args())
                self.schedule_storage[message.from_user.id] = {"start" : start - timezone, "end" : end - timezone}
                logging.debug(f"Registered new schedule: {self.schedule_storage[message.from_user.id]}")
                await message.answer("You schedule was updated")
            except ValueError as e:
                await message.answer(str(e))

    def parse_schedule(self, schedule: str):
        try:
            timezone, begin, end = schedule.split(" ", maxsplit = 2)
        except:
            raise ValueError("Wrong schedule format. Expected format: UTC<UTC zone> <start hour> <end hour>")
        timezone = int(timezone.removeprefix("UTC"))
        if abs(timezone) > 12:
            raise ValueError("Invalid timezone")
        try:
            begin = int(begin)
        except ValueError:
            raise ValueError("Start time can not be represented as integer")
        try:
            end = int(end)
        except ValueError:
            raise ValueError("End time can not be represented as integer")


        if begin >= end:
            raise ValueError("Start time is bigger than end time")
        return timezone, begin, end

    # Starts bot
    async def start(self):
        logging.info("Starting bot...")
        await self.dispatcher.start_polling()

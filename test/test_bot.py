from bot.MissingTokenError import MissingTokenError
from bot.bot import DailyGuitarBot
import pytest


class TestBot:
    def test_panics_without_token(self):
        with pytest.raises(MissingTokenError):
            bot = DailyGuitarBot(None, None, None)

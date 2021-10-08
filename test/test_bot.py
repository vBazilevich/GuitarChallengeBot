from bot.missingtokenerror import MissingTokenError
from bot.bot import DailyGuitarBot
import pytest


class TestBot:
    def test_panics_without_token(self):
        with pytest.raises(MissingTokenError):
            DailyGuitarBot(None, None, None)

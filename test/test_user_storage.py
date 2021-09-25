from bot.userstorage import MissingUserDatabaseURLError
import pytest
from bot.userstorage import UserStorage


class TestUserStorage:
    def test_requires_db_url(self):
        with pytest.raises(MissingUserDatabaseURLError):
            user_storage = UserStorage(None)

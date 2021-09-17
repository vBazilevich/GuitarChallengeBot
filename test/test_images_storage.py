import pytest
from bot.ImagesStorage import ImagesStorage, LevelDoesNotExistError, MissingMongoDBToken

class TestImagesStorage:
    def test_panics_without_mongodb_link(self):
        with pytest.raises(MissingMongoDBToken):
            storage = ImagesStorage(None)

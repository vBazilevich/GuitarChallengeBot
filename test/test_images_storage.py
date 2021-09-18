import pytest
from bot.ImagesStorage import ImagesStorage, LevelDoesNotExistError, MissingMongoDBClient

class MockCollection:
    def __init__(self, data):
        self.data = data

    def find_one(self, filters):
        for item in self.data:
            for key, value in filters.items():
                if item[key] == value:
                    return item
            return None


class TestImagesStorage:
    def test_panics_without_mongodb_link(self):
        with pytest.raises(MissingMongoDBClient):
            storage = ImagesStorage(None)

    def test_panics_when_there_are_no_more_levels(self):
        mock_db = {"images-storage": {"images": MockCollection([])}}
        storage = ImagesStorage(mock_db)
        with pytest.raises(LevelDoesNotExistError):
            storage.level(2)

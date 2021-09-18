import pytest
import os
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


@pytest.fixture
def mock_db_empty():
    return {"images-storage": {"images": MockCollection([])}}

@pytest.fixture
def mock_db():
    level_one = {
                    "identifier": "level-1",
                    "content": b"content",
                    "filename": "level-1.png"
                }
    return {"images-storage": {"images": MockCollection([level_one])}}

class TestImagesStorage:
    def test_panics_without_mongodb_link(self):
        with pytest.raises(MissingMongoDBClient):
            storage = ImagesStorage(None)

    def test_panics_when_there_are_no_more_levels(self, mock_db_empty):
        storage = ImagesStorage(mock_db_empty)
        with pytest.raises(LevelDoesNotExistError):
            storage.level(2)

    def test_returns_file_from_cache(self, mock_db_empty, mocker, tmp_path):
        # Create fake image file
        f = tmp_path / "cache/level-1.png"
        f.parent.mkdir()
        f.touch()

        storage = ImagesStorage(mock_db_empty)
        storage.images_cache = {"level-1": f.as_posix()}
        mocker.patch("os.path.exists", returns=True)
        result = storage.level(1)
        assert f.as_posix() == result._path

    def test_returns_file_from_db(self, mock_db, mocker):
        storage = ImagesStorage(mock_db, "tmp/cache/")
        result = storage.level(1)
        assert "tmp/cache/level-1.png" == result._path
        assert os.path.exists("tmp/cache/level-1.png") is True
        os.remove("tmp/cache/level-1.png")
        os.removedirs("tmp/cache")

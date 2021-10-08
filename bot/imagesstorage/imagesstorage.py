import os
from typing import Dict
import pymongo
from aiogram.types.input_file import InputFile
from bot.imagesstorage import MissingMongoDBClient
from bot.imagesstorage import LevelDoesNotExistError


class ImagesStorage:
    """
    This class implements interaction with database
    containing music scores. MongoDB is used as a
    storage. Notice that this class assumes that
    database is called `images-storage` and collection
    is called `images`. For better performance this
    class implements caching.
    """
    def __init__(self, mongodb: pymongo.MongoClient, local_storage="images/"):
        """
        :param mongodb: connection to MongoDB
        :param local_storage: name of the folder where images should be cached
                              Default: `images/`
        """
        if not mongodb:
            raise MissingMongoDBClient
        self.client = mongodb
        self.images_cache: Dict[str, str] = {}
        self.local_storage = local_storage

    def level(self, level_id: int) -> InputFile:
        """
        Loads image for a given level from the database or takes it from local cache.
        :param level_id: numeric identifier of the level. Integer number from 1
        to number of levels.
        :returns: aiogram InputFile object describing the file that contains and image
        :raises:
            LevelDoesNotExistError: there is no image for a given level_id in MongoDB storage
        """
        identifier = f"level-{level_id}"
        if identifier in self.images_cache.keys():
            filename = self.images_cache[identifier]
            if os.path.exists(filename):
                return InputFile(filename)

        database = self.client["images-storage"]
        images = database['images']

        image = images.find_one({"identifier": identifier})
        if not image:
            raise LevelDoesNotExistError
        image_content = image["content"]
        image_filename = image["filename"]
        if not os.path.exists(self.local_storage):
            os.makedirs(self.local_storage)
        with open(self.local_storage + image_filename, "wb") as file:
            file.write(image_content)
        self.images_cache[identifier] = image_filename
        return InputFile(self.local_storage + image_filename)

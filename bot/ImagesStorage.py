import os
import pymongo
from aiogram.types.input_file import InputFile


class LevelDoesNotExistError(Exception):
    def __init__(self):
        self.message = ("Sorry, we have runned out of levels. "
                        "We will add more levels soon:)")
        super().__init__(self.message)


class ImagesStorage:
    def __init__(self, mongodb_link):
        if not mongodb_link:
            raise ValueError("MongoDB link is not provided")
        self.client = pymongo.MongoClient(mongodb_link)
        self.database = self.client["images-storage"]
        self.images = self.database['images']
        self.images_cache = {}

    def level(self, level_id: int):
        # Check if image was downloaded before and it is still stored locally
        identifier = f"level-{level_id}"
        if identifier in self.images_cache.keys():
            filename = self.images_cache[identifier]
            if os.path.exists(filename):
                return InputFile(filename)

        image = self.images.find_one({"identifier": identifier})
        if not image:
            raise LevelDoesNotExistError
        image_content = image["content"]
        image_filename = image["filename"]
        with open(image_filename, "wb") as file:
            file.write(image_content)
        self.images_cache[identifier] = image_filename
        return InputFile(image_filename)

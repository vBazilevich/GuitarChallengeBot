class LevelDoesNotExistError(Exception):
    def __init__(self):
        self.message = ("Sorry, we have runned out of levels. "
                        "We will add more levels soon:)")
        super().__init__(self.message)

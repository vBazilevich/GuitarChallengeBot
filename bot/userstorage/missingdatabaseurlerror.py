class MissingUserDatabaseURLError(Exception):
    def __init__(self):
        self.message = 'Users database URL is not provided'
        super().__init__(self.message)

class MissingMongoDBClient(Exception):
    def __init__(self):
        self.message = "No MongoDB client provided"
        super().__init__(self.message)

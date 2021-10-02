class AccessingNonExistingUserError(Exception):
    def __init__(self, uid):
        self.message = (f"User with ID {uid} can not be accessed as this user",
                        " does not exist or is not registered")
        super().__init__(self.message)

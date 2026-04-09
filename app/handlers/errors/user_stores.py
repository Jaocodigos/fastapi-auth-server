from app.handlers.errors.default import NotFoundError, AlreadyExistsError

class UserStoreNotFound(NotFoundError):

    message = "User Store not found."

class UserStoreAlreadyExists(AlreadyExistsError):

    def __init__(self, us=None):
        self.message = f"UserStore '{us}' already exists."
        super().__init__(self.message)

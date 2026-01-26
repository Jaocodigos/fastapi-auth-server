from app.handlers.errors.default import NotFoundError, AlreadyExistsError


class UserNotFound(NotFoundError):

    message = "User not found."

class UserAlreadyExists(AlreadyExistsError):

    def __init__(self, user=None):
        self.message = f"User '{user}' already exists."
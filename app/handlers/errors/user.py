from app.handlers.errors.default import NotFoundError, AlreadyExistsError, ClientError

class UserNotFound(NotFoundError):

    message = "User not found."

class UserAlreadyExists(AlreadyExistsError):

    def __init__(self, user=None):
        self.message = f"User '{user}' already exists."
        super().__init__(self.message)


class InvalidVerificationToken(ClientError):

    def __init__(self):
        self.message = f"Invalid or expired verification token."
        super().__init__(self.message)


class PasswordPolicyViolation(ClientError):
    def __init__(self, violations: list[str]):
        self.message = f"Password does not meet requirements: {', '.join(violations)}"
        super().__init__(self.message)
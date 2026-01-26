from app.handlers.errors.default import NotFoundError, AlreadyExistsError


class ClaimNotFound(NotFoundError):

    message = "Claim not found."

class ClaimAlreadyExists(AlreadyExistsError):

    def __init__(self, claim=None):
        self.message = f"Claim '{claim}' already exists."


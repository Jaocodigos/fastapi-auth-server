
from app.handlers.errors.default import NotFoundError, AlreadyExistsError

class ScopeNotFound(NotFoundError):

    message = "Scope not found."

class ScopeAlreadyExists(AlreadyExistsError):

    def __init__(self, scope=None):
        self.message = f"Scope '{scope}' already exists."
        super().__init__(self.message)
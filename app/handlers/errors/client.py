from app.handlers.errors.default import NotFoundError, ClientError


class ClientNotFound(NotFoundError):

    message = "Client not found."

class InvalidClient(ClientError):

    def __init__(self):
        self.message = "Invalid client"
        self.status_code = 401
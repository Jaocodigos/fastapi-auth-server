
class AlreadyExistsError(Exception):

    status_code = 409
    error_code = "DOMAIN_ERROR"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class UnauthorizedError(Exception):

    status_code = 401
    error_code = "UNAUTHORIZED"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class NotFoundError(Exception):

    status_code = 404
    error_code = "RESOURCE_NOT_FOUND"
    message = "Resource not found."

class ClientError(Exception):

    error_code = "INVALID_CLIENT"

    def __init__(self, message: str, status_code: int = 400):
        self.status_code = status_code
        self.message = message
        super().__init__(message)

class OauthError(Exception):

    error_code = "OAUTH_ERROR"

    def __init__(self, message: str, status_code: int = 400):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


class OAuthError(Exception):

    def __init__(self, error: str, code: int = 400):
        self.error = error
        self.code = code
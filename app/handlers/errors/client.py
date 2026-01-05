
class ClientNotFound(Exception):

    def __init__(self):
        self.error = "Client not found"
        self.status_code = 404


class InvalidClient(Exception):

    def __init__(self):
        self.error = "Client not found"
        self.status_code = 401
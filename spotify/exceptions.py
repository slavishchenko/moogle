class NoSearchQuery(Exception):
    """Raised if no search query is provided"""

    pass


class InvalidCredentials(Exception):
    """Raised if invalid credentials are passed into client class"""

    pass


class InvalidItemType(Exception):
    """Raise if invalid item_type is provided to parse_json function"""

    pass


class SpotifyException(Exception):
    def __init__(self, status_code: int, endpoint: str, msg: str | None):
        self.status_code = status_code
        self.endpoint = endpoint
        self.msg = msg

    def __str__(self):
        return f'\nHTTP {self.status_code} Error occured while getting "{self.endpoint}".\nReason: {self.msg}.'

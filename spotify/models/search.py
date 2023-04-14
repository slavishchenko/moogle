class Search:
    """
    Spotify search response.

    :ivar href: A link to the Web API endpoint returning the full result of the request.
    :ivar items: List of objects
    :ivar limit: The maximum number of items in the response (as set in the query or by default).
    :ivar next: URL to the next page of items or None.
    :ivar offset: The offset of the items returned (as set in the query or by default).
    :ivar previous: URL to the previous page of items or None.
    :ivar total: The total number of items available to return.
    """

    def __init__(
        self,
        href: str,
        items: list[object],
        limit: int,
        next: str | None,
        offset: int,
        previous: str | None,
        total: int,
    ) -> None:
        self.href = href
        self.items = items
        self.limit = limit
        self.next = next
        self.offset = offset
        self.previous = previous
        self.total = total

    def __str__(self):
        return f"{self.items}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.items})"

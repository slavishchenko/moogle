from .image import Image


class Followers:
    def __init__(self, href, total) -> None:
        self.href = href
        self.total = total

    def __str__(self) -> str:
        return f"{self.total}"


class Artist:
    """
    The Artist model.

    Followers, genres, images and popularity will be None for *simplified version* of the Artist object.
    * You'll get a Simplified Artist object when accessing 'artists' attribute in the Album class, for example.

    :ivar external_urls: Known external URLs for this artist.
    :ivar href: A link to Web API endpoint providing full details of the artist.
    :ivar id: The Spotify ID for the artist.
    :ivar name: The name of the artist.
    :ivar type: The object type. Allowed value: "artist".
    :ivar uri: The Spotify URI for the artist.
    :ivar followers: Information about the followers of the artist.
    :ivar genres: A list of the genres the artist is associated with or an empty list.
    :ivar images: Images of the artist in various sizes, widest first.
    :ivar popularity: The popularity of the artist. Values is between 0 and 100.
    """

    def __init__(
        self,
        external_urls: dict,
        href: str,
        id: str,
        name: str,
        type: str,
        uri: str,
        followers=None | list[Followers],
        genres=None | list,
        images=None | list[Image],
        popularity=None | int,
    ) -> None:
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.name = name
        self.type = type
        self.uri = uri
        self.followers = followers
        self.genres = genres
        self.images = images
        self.popularity = popularity

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

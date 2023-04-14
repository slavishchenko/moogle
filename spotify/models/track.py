from .album import Album
from .artist import Artist


class Track:
    """
    Track model.

    Album, external_ids, and popularity will be None for *simplified version* of the Track object.
    * You'll get a Simplified Track object when accessing 'tracks' attribute in the Album class, for example.


    :ivar artists: The artists who performed the track.
                    Each artist object includes a link in href to more detailed information about the artist.
    :ivar available_markets: A list of the countries in which the track can be played.
    :ivar disc_number: The disc number (usually 1 unless the album consists of more than one disc).
    :ivar duration_ms: The track length in milliseconds.
    :ivar explicit: Whether or not the track has explicit lyrics.
    :ivar external_urls: Known external URLs for this track.
    :ivar href: A link to the Web API endpoint providing full details of the track.
    :ivar id: The Spotify ID of the track.
    :ivar is_local: Whether or not the track is from a local file.
    :ivar name: The name of the track.
    :ivar preview_url: A link to a 30 second preview (MP3 format) of the track. Can be null.
    :ivar track_number: The number of the track. If an album has several discs, the track number is the number on the specified disc.
    :ivar type: The object type. "track".
    :ivar uri: The Spotify URI for the track.
    :ivar album: The album on which the track appears.
    :ivar external_ids: Known external IDs for the track.
    :ivar popularity: Popularity of the track. Value between 0 and 100.
    """

    def __init__(
        self,
        artists: list[Artist],
        disc_number: int,
        duration_ms: int,
        explicit: bool,
        external_urls: dict,
        href: str,
        id: str,
        is_local: bool,
        name: str,
        preview_url: str,
        track_number: int,
        type: str,
        uri: str,
        available_markets: list[str] = None,
        is_playable: bool = None,
        album=None | list[Album],
        external_ids=None | dict,
        popularity=None | float,
    ) -> None:
        self.album = album
        self.artists = artists
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_ids = external_ids
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.is_local = is_local
        self.name = name
        self.popularity = popularity
        self.preview_url = preview_url
        self.track_number = track_number
        self.type = type
        self.uri = uri
        self.is_playable = is_playable

    @property
    def url(self):
        """Returns track URL on Spotify"""
        return f"https://open.spotify.com/track/{self.id}"

    def __str__(self):
        return f"{', '.join([artist.name for artist in self.artists])} - {self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

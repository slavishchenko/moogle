from typing import Dict, List, Optional

from .artist import Artist
from .image import Image


class Album:
    """
    Spotify Album model.

    :ivar album_group: The field is present when getting an artist's albums.
                        This field represents relationship between the artist and the album.
                        Example values: "compilation"
                        Allowed values: "album", "single", "compilation", "appears_on".
    :ivar album_type: The type of the album.
    :ivar artists: The artists of the album (simplified).
                    Each artist object includes a link in href to more detailed information about the artist.
    :ivar available_markets: The markets in which the album is available.
    :ivar external_urls: Known external URLs for this album.
    :ivar href: A link to the Web API endpoint providing full details of the album.
    :ivar id: Spotify id of the Album.
    :ivar images: The cover art for the album in various sizes, widest first.
    :ivar name: The name of the album.
    :ivar release_date: The date the album was first released.
    :ivar release_date_precision: The precision with which release_date value is known.
    :ivar total_tracks: The number of tracks in the album.
    :ivar type: The object type. Allowed values: "album".
    :ivar uri: The Spotify URI for the album.
    :ivar external_ids: Known external IDs for the album or None.
    :ivar copyrights: The copyright statements of the album.
    :ivar genres: A list of genres the album is associated with. If not yet classified, the list is empty.
    :ivar label: The label associated with the album.
    :ivar popularity: The popularity of the album. The values will be between 0 and 100.
    :ivar tracks: The tracks of the album. None for simplified version of the Album.
    :ivar is_playable: True, False or None.
    """

    def __init__(
        self,
        album_type: str,
        artists: List[Artist],
        available_markets: List[str],
        external_urls: Dict,
        href: str,
        id: str,
        images: List[Image],
        name: str,
        release_date: str,
        release_date_precision: str,
        total_tracks: int,
        type: str,
        uri: str,
        album_group: Optional[str] = None,
        external_ids: Optional[Dict] = None,
        copyrights: Optional[List["Copyright"]] = None,
        genres: Optional[List[str]] = None,
        label: Optional[str] = None,
        popularity: Optional[int] = None,
        tracks=None,
        is_playable: Optional[bool] = None,
    ) -> None:
        self.album_group = album_group
        self.album_type = album_type
        self.artists = artists
        self.available_markets = available_markets
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.images = images
        self.name = name
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.total_tracks = total_tracks
        self.type = type
        self.uri = uri
        self.external_ids = external_ids
        self.copyrights = copyrights
        self.genres = genres
        self.label = label
        self.populariy = popularity
        self.tracks = tracks
        self.is_playble = is_playable

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    @property
    def release_year(self):
        return self.release_date.split("-")[0]


class Copyright:
    """
    Copyright model.

    :param text: The copytight text for this content.
    :param type: The type of copyright: C = the copyright, P = performance copyright.
    """

    def __init__(self, text: str, type: str) -> None:
        self.text = text
        self.type = type

    def __str__(self) -> str:
        return f"{self.text}"

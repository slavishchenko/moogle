import asyncio
import base64
import datetime
import logging
from typing import Dict, List, Optional, Union
from urllib.parse import parse_qsl, urlencode

import aiohttp

from .exceptions import InvalidCredentials, NoSearchQuery, SpotifyException
from .models import (
    Album,
    Artist,
    AudioAnalysis,
    Copyright,
    Followers,
    Image,
    Recommendations,
    Search,
    Track,
)
from .utils import parse_json

logger = logging.getLogger(__name__)

MODELS = {
    "tracks": {"main": Track, "extra": {"artists": Artist, "album": Album}},
    "albums": {
        "main": Album,
        "extra": {
            "artists": Artist,
            "images": Image,
            "copyrights": Copyright,
        },
    },
    "artists": {"main": Artist, "extra": {"images": Image, "followers": Followers}},
}


class Client:
    """
    Client used to interact with the Spotify Web Api.

    :ivar client_id: Your Client ID.
    :ivar client_secret: Your Client Secret
    """

    API_URL = "https://api.spotify.com/"
    CURRENT_API_VERSION = "v1"

    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_expired = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id: str, client_secret: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not isinstance(client_id, str) and not isinstance(client_secret, str):
            raise InvalidCredentials(
                "client_id and client_secret need to be of type 'str'."
            )
        self.client_id = client_id
        self.client_secret = client_secret
        self.loop = asyncio.new_event_loop()
        self._session = aiohttp.ClientSession(loop=self.loop)

    async def close(self) -> None:
        await self._session.close()

    async def __aenter__(self) -> "Client":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close()

    def get_client_credentials(self) -> str:
        """
        Returns base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id is None or client_secret is None:
            raise InvalidCredentials("You must provide client_id and client_secret")
        client_credentials = f"{client_id}:{client_secret}"
        client_credentials_b64 = base64.b64encode(client_credentials.encode())
        return client_credentials_b64.decode()

    def get_token_headers(self) -> dict:
        return {"Authorization": f"Basic {self.get_client_credentials()}"}

    def get_token_data(self) -> dict:
        return {"grant_type": "client_credentials"}

    async def authenticate(self) -> bool:
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()

        async with self._session.post(
            token_url, data=token_data, headers=token_headers
        ) as response:
            response.raise_for_status()
            data = await response.json()

        now = datetime.datetime.now()
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_expired = expires < now

        return True

    async def get_access_token(self) -> str:
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            await self.authenticate()
            return await self.get_access_token()
        elif token == None:
            await self.authenticate()
            return await self.get_access_token()
        return token

    async def get_resource_headers(self) -> dict:
        access_token = await self.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers

    async def _get(self, endpoint: str):
        headers = await self.get_resource_headers()
        async with self._session.get(endpoint, headers=headers) as response:
            if response.status not in range(200, 299):
                try:
                    json_response = await response.json()
                    error = json_response.get("error", {})
                    msg = error.get("message")
                except ValueError:
                    msg = response.text or None

                logger.error(
                    f"HTTP {response.status} Error returned for {endpoint}. Reason: {msg}"
                )

                raise SpotifyException(response.status, endpoint, msg)
            data = await response.json()
        return data

    async def get_resource(
        self,
        lookup_id: str,
        resource_type: str = "tracks",
        version: str = None,
        query_params: Optional[str] = None,
    ) -> dict:
        """
        Sends a GET request to Spotify API

        :param lookup_id: Spotify ID for the desired resource.
        :param resource_type: Which resource you're trying to get. Default is: tracks.
        :param version: Spotify API version. Defaults to CURRENT_API_VERSION.
        :return: Spotify JSON response
        :rtype: JSON
        :raises: exceptions.SpotifyException
        """
        if not version:
            version = self.CURRENT_API_VERSION
        endpoint = f"{self.API_URL}{version}/{resource_type}/{lookup_id}"

        if query_params:
            endpoint = f"{endpoint}/{query_params}"

        response = await self._get(endpoint=endpoint)
        return response

    @staticmethod
    def _get_json_lookup_key(query_params: str):
        """Returns the key that will be used to parse json"""
        return f"{parse_qsl(query_params)[1][1]}s"

    async def base_search(self, query_params) -> Dict:
        endpoint = f"{self.API_URL}{self.CURRENT_API_VERSION}/search"
        lookup_url = f"{endpoint}?{query_params}"

        response = await self._get(endpoint=lookup_url)

        search_type = self._get_json_lookup_key(query_params)
        search_result = Search(**response[search_type])
        search_result.items = parse_json(
            item_type=search_type, json_response=search_result.items, models=MODELS
        )
        return search_result

    async def search(
        self,
        query: str,
        search_type: Union[str, list] = None,
        limit: int = 1,
    ) -> Search:
        """
        Get Spotify catalog information about albums, artists and tracks
        that match a keyword string.

        :param query: required - Your search query.
        :param search_type: Optional item type to search accross. Defaults to "track".
        :param limit: Maximum number of results to return. >= 0 <= 50. Default is 1.
        :raise exceptions.NoSearchQuery: If no query is provided.
        :return: :py:class:`~spoti2py.models.search.Search`
        :rtype: object
        """
        if query == None:
            raise NoSearchQuery("A query is required")

        if search_type is None:
            search_type = "track"
        if isinstance(search_type, list):
            search_type = ",".join([type.lower() for type in search_type])
        if isinstance(search_type, str):
            search_type = search_type.lower()
        query_params = urlencode({"q": query, "type": search_type, "limit": limit})
        search_results = await self.base_search(query_params)

        return search_results

    async def get_album(self, id: str) -> Album:
        """
        Get Spotify catalog information for a single album.

        :param id: The Spotify ID of the album. Required.
        :return: :py:class:`~spoti2py.models.album.Album`
        :rtype: object
        """
        album = parse_json(
            item_type="albums",
            json_response=await self.get_resource(id, resource_type="albums"),
            models=MODELS,
        )
        album.tracks = [Track(**song) for song in album.tracks["items"]]
        return album

    async def get_album_tracks(
        self, id: str, market: str = None, limit: int = 20
    ) -> List[Track]:
        """
        Get Spotify catalog information about an album's tracks.
        Optional parameters can be used to limit the number of tracks returned.

        :param id: The Spotify ID of the album. Required.
        :param market: An ISO 3166-1 alpha-2 country code.
                       If a country code is specified, only content that is available in that market will be returned.
                       If a valid user access token is specified in the request header,
                       the country associated with the user account will take priority over this parameter.
                       Default: us.
        :param limit: The maximum number of items to return. Default: 20. Min: 1. Max: 50.
        :return: list[:py:class:`~spoti2py.models.track.Track`]
        :rtype: list
        """
        query_params = {"id": id, "limit": limit}
        if not market:
            query_params["market"] = "us"
        query_params["market"] = market

        endpoint = f"tracks"
        album_tracks = await self.get_resource(
            lookup_id=id, resource_type="albums", query_params=endpoint
        )
        return parse_json(
            item_type="tracks", json_response=album_tracks["items"], models=MODELS
        )

    async def get_new_releases(self, country: str = None, limit: int = 20):
        """
        Get a list of new album releases featured in Spotify

        :param country: A country: an ISO 3166-1 alpha-2 country code.
                        Provide this parameter if you want the list of returned items to be relevant to a particular country.
                        If omitted, the returned items will be relevant to all countries.
        :param limit: The maximum number of items to return. Default: 20. Min: 1. Max: 50.
        :return: list[:py:class:`~spoti2py.models.album.Album`]
        """
        query_params = {"limit": limit}
        endpoint = f"{self.API_URL}{self.CURRENT_API_VERSION}/browse/new-releases?{urlencode(query_params)}"
        if country:
            query_params["country"] = country
            endpoint = f"{endpoint}{urlencode(query_params)}"

        response = await self._get(endpoint=endpoint)

        new_releases = response["albums"]["items"]
        return parse_json(item_type="albums", json_response=new_releases, models=MODELS)

    async def get_artist(self, id: str) -> Artist:
        """
        Get Spotify catalog information for a single artist identified by their unique Spotify ID.

        :param id: The Spotify ID of the artist. Required."
        :return: :py:class:`~spoti2py.models.artist.Artist`
        :rtype: object
        """
        response = await self.get_resource(id, resource_type="artists")
        artist = parse_json(item_type="artists", json_response=response, models=MODELS)

        return artist

    async def get_artists_albums(
        self, id: str, include_groups: Optional[List[str]] = None, limit: int = 20
    ) -> List[Album]:
        """
        Get Spotify catalog information about an artist's albums.

        :param id: The Spotify ID of the artist.
        :param include_groups: A list of keywords that will be used to filter the response.
                               If not supplied, all album types will be returned.
                               Valid values: album, single, appears_on, compilation.
        :param limit: The maximum number of items to return. Default: 20. Min: 1. Max. 50.
        :return: List[:py:class:`~spoti2py.models.album.Album`]
        :rtype: List[object]
        """
        query_params = {"id": id, "limit": limit}
        if include_groups:
            if not isinstance(include_groups, list):
                raise TypeError("include_groups should be a list of strings.")
            query_params["include_groups"] = ",".join(include_groups)
        endpoint = f"albums?{urlencode(query_params)}"

        response = await self.get_resource(
            lookup_id=id, resource_type="artists", query_params=endpoint
        )
        artists_albums = parse_json(
            item_type="albums", json_response=response["items"], models=MODELS
        )

        return artists_albums

    async def get_artists_top_tracks(self, id: str, market: str = None) -> List[Track]:
        """
        Get Spotify catalog information about an artist's top tracks by country.

        :param id: The Spotify ID of the artist.
        :param market: An ISO 3166-1 alpha-2 country code.
                       If a country code is specified, only content that is available in that market will be returned.
                       If a valid user access token is specified in the request header,
                       the country associated with the user account will take priority over this parameter.
                       Default: us.
        :return: list[:py:class:`~spoti2py.models.track.Track`]
        :rtype: list[object]
        """
        if not market:
            market = "us"
        endpoint = f"top-tracks?market={market}"
        response = await self.get_resource(
            lookup_id=id, resource_type="artists", query_params=endpoint
        )
        top_tracks = parse_json(
            item_type="tracks", json_response=response["tracks"], models=MODELS
        )

        return top_tracks

    async def get_related_artists(self, id: str) -> List[Artist]:
        """
        Get Spotify catalog information about artists similar to a given artist.

        :param id: The Spotify ID of the artist.
        :return: list[:py:class:`~spoti2py.models.artist.Artist`]
        :type: list
        """
        endpoint = f"related-artists"
        response = await self.get_resource(
            lookup_id=id, resource_type="artists", query_params=endpoint
        )
        related_artists = parse_json(
            item_type="artists", json_response=response["artists"], models=MODELS
        )
        return related_artists

    async def get_track(self, id: str) -> Track:
        """
        Get Spotify catalog information for a single track identified by its unique Spotify ID.

        :param id: The Spotify ID of the track. Required."
        :return: :py:class:`~spoti2py.models.track.Track`
        :rtype: object
        """
        response = await self.get_resource(id, resource_type="tracks")
        track = parse_json(item_type="tracks", json_response=response, models=MODELS)

        return track

    async def get_audio_analysis(self, id: str) -> AudioAnalysis:
        """
        Get low-level audio analysis for a track in the Spotify catalog.
        The audio analysis describes the track’s structure and musical content, including rhythm, pitch, and timbre.

        :param id: The Spotify ID of the track. Required."
        :return: :py:class:`~spoti2py.models.audio_analysis.AudioAnalysis`
        :rtype: object
        """
        response = await self.get_resource(id, resource_type="audio-analysis")
        audio_analysis = response["track"]
        return AudioAnalysis(**audio_analysis)

    async def get_recommendations(
        self,
        limit: int = 20,
        seed_artists: List[str] = None,
        seed_genres: List[str] = None,
        seed_tracks: List[str] = None,
    ) -> Recommendations:
        """
        Recommendations are generated based on the available information or a given seed entity and matched against similar artists and tracks.
        For artists and tracks that are very new or obscure there might not be enough data to generate a list of tracks.

        :param limit: The target size of the list of recommended tracks.
                      Default: 20. Minimum: 1. Maximum: 100.
        :param seed_artists: A list of Spotify IDs for seed artists.
        :param seed_genres: A list of any genres in the set of available genre seeds.
                            available_genre_seeds is an attribute of the Client class.
        :param seed_tracks: A list of Spotify IDs fpr a seed track.

        Up to 5 seed values may be provided in any combination of seed_artists, seed_tracks and seed_genres.
        At least 1 is required!

        :return: :py:class:`~spoti2py.models.recommendations.Recommendations`
        :rtype: object
        """

        query_params = {"limit": limit}
        args = [
            ("seed_artists", seed_artists),
            ("seed_genres", seed_genres),
            ("seed_tracks", seed_tracks),
        ]
        if not any(arg[1] for arg in args):
            raise Exception("You need to provide at least 1 seed value.")
        for arg in args:
            if not arg[1]:
                pass
            elif isinstance(arg[1], list):
                query_params[arg[0]] = ",".join(arg[1])
            else:
                raise TypeError(
                    f"Invalid value for {arg[0]}. Expected a list, but got '{type(arg[1])}' instead."
                )

        endpoint = f"{self.API_URL}{self.CURRENT_API_VERSION}/recommendations/?{urlencode(query_params)}"
        response = await self._get(endpoint)

        recommendations = Recommendations(**response)
        recommendations.tracks = parse_json(
            item_type="tracks", json_response=recommendations.tracks, models=MODELS
        )
        return recommendations

    @property
    async def available_genre_seeds(self):
        """
        A list of available genres seed parameter values for recommendations.

        :return: List of genres.
        :rtype: list[str]
        """
        endpoint = f"{self.API_URL}{self.CURRENT_API_VERSION}/recommendations/available-genre-seeds"
        available_genre_seeds = await self._get(endpoint=endpoint).json()["genres"]
        return available_genre_seeds

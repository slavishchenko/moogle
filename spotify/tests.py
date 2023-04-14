import os
import unittest

import dotenv

from client import Client
from exceptions import InvalidCredentials
from models import Album, Artist, AudioAnalysis, Recommendations, Search, Track

dotenv.load_dotenv()


CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")


class TestClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        self.endpoint = "https://api.spotify.com/v1/"
        self.headers = self.client.get_resource_headers()
        self.song_id = "13Uvqll8OQDjw3wDweIK9y"
        self.album_id = "2Lq2qX3hYhiuPckC8Flj21"
        self.artist_id = "1vCWHaC5f2uS3yhpwWbIA6"

    def tearDown(self):
        self.client._session.close()

    def test_init_valid_credentials(self):
        self.assertIsInstance(self.client, Client)

    def test_init_invalid_credentials(self):
        def init_client():
            Client(client_id=1, client_secret=2)

        self.assertRaises(InvalidCredentials, init_client)

    def test_get_client_credentials(self):
        self.assertEqual(type(self.client.get_client_credentials()), str)

    def test_authenticate(self):
        self.assertTrue(self.client.authenticate())

    def test__get(self):
        r = self.client._get(endpoint=self.endpoint, headers=self.headers)
        self.assertTrue(r.status_code, 200)

    def test_get_resource(self):
        r = self.client.get_resource(lookup_id=self.song_id, resource_type="tracks")
        self.assertIsInstance(r, dict)

    def test_search(self):
        s = self.client.search("master of puppets", search_type="track")
        self.assertIsInstance(s, Search)
        self.assertTrue(s.items)
        self.assertIsInstance(s.items, list)

    def test_get_album(self):
        a = self.client.get_album(id=self.album_id)
        self.assertIsInstance(a, Album)
        self.assertEqual(a.name.lower(), "master of puppets (remastered)")

    def test_get_album_tracks(self):
        tracks = self.client.get_album_tracks(self.album_id, limit=1)
        self.assertIsInstance(tracks, list)

    def test_get_new_releases(self):
        new_releases = self.client.get_new_releases(limit=1)
        self.assertTrue(len(new_releases), 1)
        self.assertIsInstance(new_releases[0], Album)

    def test_get_artist(self):
        a = self.client.get_artist(id=self.artist_id)
        self.assertIsInstance(a, Artist)
        self.assertEqual(a.name, "Avicii")

    def test_get_artists_albums(self):
        albums = self.client.get_artists_albums(id=self.artist_id, limit=1)
        self.assertTrue(len(albums), 1)
        self.assertIsInstance(albums[0], Album)

    def test_get_artists_top_tracks(self):
        tracks = self.client.get_artists_top_tracks(id=self.artist_id)
        self.assertIsInstance(tracks, list)
        self.assertIsInstance(tracks[0], Track)

    def test_get_related_artists(self):
        artist = self.client.get_related_artists(id=self.artist_id)
        self.assertIsInstance(artist, list)
        self.assertIsInstance(artist[0], Artist)

    def test_get_track(self):
        track = self.client.get_track(id=self.song_id)
        self.assertIsInstance(track, Track)
        self.assertTrue(track.name.lower() == "the day that never comes")

    def test_get_audio_analysis(self):
        aa = self.client.get_audio_analysis(id=self.song_id)
        self.assertIsInstance(aa, AudioAnalysis)

    def test_get_recommendations(self):
        rec = self.client.get_recommendations(limit=1, seed_artists=[self.artist_id])
        self.assertIsInstance(rec, Recommendations)
        self.assertTrue(rec.tracks)
        self.assertIsInstance(rec.tracks[0], Track)

    def test_available_genre_seeds(self):
        genres = self.client.available_genre_seeds
        self.assertIsInstance(genres, list)
        self.assertGreater(len(genres), 10)


if __name__ == "__main__":
    unittest.main()

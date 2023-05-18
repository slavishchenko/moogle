import asyncio
import os
import random

from django.core.exceptions import BadRequest
from django.shortcuts import redirect, render
from django.utils.html import escape

from spoti2py.client import Client

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")


# Create your views here.
def index(request):
    if request.method == "GET":
        try:
            q = escape(request.GET["q"])
            if not q:
                return redirect(index)

            client = Client(client_id=client_id, client_secret=client_secret)

            async def fetch():
                async with client as c:
                    spotify_search = await c.search(query=q, limit=5)
                    songs = spotify_search.items
                    analysis = await asyncio.gather(
                        *[
                            asyncio.create_task(c.get_audio_analysis(song.id))
                            for song in songs
                        ]
                    )
                    albums = [song.album for song in songs]

                    return zip(songs, analysis, albums)

            response = client.loop.run_until_complete(fetch())

            context = {"response": response}

            return render(request, "main/index.html", context)
        except:
            context = {}
            return render(request, "main/index.html", context)
    else:
        raise BadRequest


def song_detail(request, id, title):
    client = Client(client_id=client_id, client_secret=client_secret)

    async def fetch_details():
        async with client as c:
            song = await c.get_track(id=id)
            artist_id = song.artists[0].id
            analysis, artist, album, top_tracks = await asyncio.gather(
                c.get_audio_analysis(id=song.id),
                c.get_artist(id=artist_id),
                c.get_album(id=song.album.id),
                c.get_artists_top_tracks(id=artist_id),
            )
            return (song, analysis, artist, album, top_tracks)

    song, analysis, artist, album, top_tracks = client.loop.run_until_complete(
        fetch_details()
    )

    is_single = False

    if album.album_group == "single":
        is_single = True

    about = f"""<em>{song.name}</em> is a song by <em>{artist.name}</em>, released in {album.release_year} 
                    {'as a standalone single' if is_single else f'as a part of the "{album.name}" album.'}
                """
    title = f"{artist.name} - {song.name} - moogle"

    context = {
        "title": title,
        "song": song,
        "analysis": analysis,
        "artist": artist,
        "album": album,
        "top_tracks": top_tracks,
        "is_single": is_single,
        "about": about,
    }
    return render(request, "main/song-detail.html", context)

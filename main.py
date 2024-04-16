from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify_id = "******************"
spotify_key = "***************"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=spotify_id,
        client_secret=spotify_key,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        cache_path="token.txt"
    )
)
user_id = "*************"

date_to_travel = input("Which date you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date_to_travel}/")
hot_100_chart = response.text

soup = BeautifulSoup(hot_100_chart, "html.parser")

song_titles = soup.select("li ul li h3")
titles = []
for song in song_titles:
    titles.append(song.getText().strip())

songs_uris = []
for title in titles:
    track = sp.search(q=f"track:{title} year:{date_to_travel[:4]}", type="track", limit=1)
    # print(track["tracks"]["items"][0]["artists"][0]["name"]) # Artist's name
    # print(track["tracks"]["items"][0]["name"]) #Song name
    try:
        uri = track["tracks"]["items"][0]["uri"]
        songs_uris.append(uri)
        print(f"{title} Added.")
    except IndexError:
        print(f"{title} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date_to_travel} Billboard 100",
    public=False,
    description=f"Top 100 songs on {date_to_travel}"
)

playlist_id = playlist["id"]
for item in songs_uris:
    sp.playlist_add_items(playlist_id=playlist_id, items=songs_uris)

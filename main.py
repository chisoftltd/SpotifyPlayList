import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
from dotenv import find_dotenv, load_dotenv
import datetime

from bs4 import BeautifulSoup
import requests

dotenv_path = find_dotenv()

Client_ID = os.getenv("Client_ID")
Client_Secret = os.getenv("Client_Secret")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=Client_ID,
                                                           client_secret=Client_Secret))

results = sp.search(q='love', limit=30)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt",
        username="BenSpotufy",
    )
)
user_id = sp.current_user()["id"]
print("Which date do you want to travel to? \n")

year = int(input('Enter a year: '))
while year not in range(1899, 2025):
    year = int(input('Enter a valid year: '))
    print()

month = int(input('Enter a month: '))
while month not in range(1, 13):
    month = int(input('Enter a valid month: '))
    print()

day = int(input('Enter a day: '))
while day not in range(1, 32):
    day = int(input('Enter a valid day: '))
    print()

date1 = datetime.date(year, month, day)

website_url = 'https://www.billboard.com/charts/hot-100/' + str(date1) +'/'
response = requests.get(website_url)
top_hits = response.text

soup = BeautifulSoup(top_hits, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

#song_names = ["The list of song", "titles from your", "web scrape"]

song_uris = []
year = str(date1).split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date1} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
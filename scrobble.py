import os
import sys
import re
import time
import json
import threading
from itertools import cycle
from datetime import datetime

import requests
import pylast
from pylast import NetworkError
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pystyle import Center

W = '\033[0m'
R = '\x1b[38;5;196m'


# -------------------- Utility Functions --------------------

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    
    print(Center.XCenter("""
\n
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣔⣾⣿⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡾⣿⣿⣿⣿⣿⣿⣧⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⢿⣿⣾⣯⡶⠒⢾⡟⣿⡿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⡀⠀⢀⣴⣿⡷⣻⣿⢷⡏⣴⢲⠀⣿⢸⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠄⠒⠊⠉⠍⣉⣩⣭⣿⣿⡿⡿⠿⢾⣿⣿⣿⣗⢬⣥⣴⣿⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠴⠊⠁⠀⠀⢀⣤⣶⣾⠟⠛⠉⠁⠁⣀⡀⠀⠀⣀⠈⠙⠢⢿⣿⣿⣿⣿⠁⠀⠀
⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣠⣔⣡⣤⣤⣤⣤⣶⡿⠋⢁⡠⠄⠒⠊⠉⠁⠀⠉⠙⠻⢿⣾⣷⣦⣤⣽⣿⣿⡿⠀⠀⠀
⢀⣤⣶⡾⣿⣽⣿⠖⠒⠛⣻⣟⣿⣛⣿⣿⡿⢟⣡⡾⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣯⣸⣿⠀⠀⠀
⠸⣿⣿⣿⣿⣇⣿⠾⠋⠩⣿⡿⣿⣿⣿⢟⣵⠗⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣇⠀⠀
⠀⠹⣿⣿⣿⢹⡏⢼⣛⠆⢸⡇⣿⡟⢡⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣷⣿⡀⠀
⠀⠀⠈⢿⣿⣜⢾⣤⣤⣴⣿⣿⡿⠀⡔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣿⣿⣿⣿⡿⣇⠀
⠀⠀⠀⠀⠙⣿⣷⣿⣿⣿⣿⣿⠁⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣷⣮⣿⣿⣿⣸⠟⠀
⠀⠀⠀⠀⠀⠈⠹⣿⡿⣿⣿⣧⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢿⣗⠚⡿⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⡀⣷⡀     
⠀⠀⠀⠀⠀⠀⠀⢻⣿⣶⣧⣿⠀⠀⣠⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡇⢳⢣         
⠀⠀⠀⠀⠀⠀⠀⢹⣿⣯⡟⢻⣆⣼⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⠃⡞⢸
⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡏⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣾⠀⡇⣼
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣯⠁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⢸⣯⣿⣿⣿⣿⣿⣷⣶⣿⣿⣹⠙⡟⢠⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠛⢛⡻⣿⣿⣿⣿⣿⣿⣿⣟⢿⣿⣿⣿⣷⡄⣿⣿⣿⣿⡿⠋⢹⣿⣿⣫⢃⣴⠕⠃⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⣄⡀⠈⠉⠛⢿⣿⣿⣿⣿⣿⡷⣭⡻⣿⣿⣿⠈⠻⢿⣿⣧⣾⣿⡿⠗⠓⠛⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣧⡂⢀⡀⠀⠈⢝⡂⠀⠉⠻⣿⡛⣾⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢦⡈⠂⠀⠀⠉⠢⢄⠈⣸⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⠢⠴⢦⣄⡠⠟⠁⠀⠀⠀⠀⠀⠀⠀
\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""))


def load_config():
    """Load configuration from config.json."""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'config.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


# -------------------- Networking --------------------

def fetch_proxies():
    """Fetch HTTP proxies from ProxyScrape."""
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
    response = requests.get(url)
    return response.text.splitlines()


def authenticate_lastfm(api_key, api_secret, username, password, proxy=None):
    clear_screen()
    banner()
    print(f"  [{R}INFO{W}] Authenticating Last.fm...")
    time.sleep(1)
    if not all([api_key, api_secret, username, password]):
        print(f"  [{R}ERROR{W}] Last.fm credentials are missing in config.json")
        time.sleep(2)
        return None

    try:
        network = pylast.LastFMNetwork(
            api_key=api_key,
            api_secret=api_secret,
            username=username,
            password_hash=pylast.md5(password)
        )
        user = network.get_authenticated_user()
        if not user:
            print("Failed to authenticate with Last.fm.")
            time.sleep(2)
        print(f"  [{R}INFO{W}] Logged in to Last.fm as: {user.get_name()}")
        time.sleep(1)
        return network
    except Exception as e:
        print(f"  [{R}ERROR{W}] Last.fm login failed: {e}")
        time.sleep(2)
        return None
# -------------------- Scrobbling --------------------

def scrobble_track(network, track, artist, album, proxy):
    """Send a single scrobble to Last.fm."""
    try:
        network.scrobble(
            artist=artist,
            title=track,
            album=album,
            timestamp=int(time.time())
        )
        print(f"  [{R}INFO{W}][{datetime.utcnow().strftime('%H:%M:%S.%f')}] "
              f"Scrobbled: {track} | Artist: {artist} | Album: {album} | Proxy: {proxy}")
    except NetworkError:
        print(f"  [{R}ERROR{W}] Failed to scrobble with proxy {proxy}")


def scrobble_tracks_from_file(network, file_name, proxies):
    """Scrobble all tracks from a file."""
    clear_screen()
    banner()
    print(f"Scrobbling from: {file_name}")

    try:
        with open(f"./songlist/{file_name}", 'r', encoding='utf-8') as file:
            lines = file.readlines()

        proxy_pool = cycle(proxies)
        threads = []

        for line in lines:
            parts = line.strip().split(' | ')
            track = next((p.split(': ')[1] for p in parts if 'Song:' in p), None)
            artist = next((p.split(': ')[1] for p in parts if 'Artist:' in p), None)
            album = next((p.split(': ')[1] for p in parts if 'Album:' in p), None)

            if track and artist and album:
                proxy = next(proxy_pool)
                t = threading.Thread(target=scrobble_track, args=(network, track, artist, album, proxy))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()

    except FileNotFoundError:
        print(f"  [{R}ERROR{W}] Songs file not found.")
        time.sleep(2)


def choose_song_list(network, proxies):
    """Allow user to choose a song list file and scrobble it."""
    clear_screen()
    banner()
    txt_files = [f for f in os.listdir("songlist") if f.endswith('.txt')]

    if not txt_files:
        print(f"  [{R}ERROR{W}] No saved song list files found.")
        time.sleep(2)
        return

    print("  Available song list files:")
    for idx, file_name in enumerate(txt_files, start=1):
        print(f"  [{R}{idx}{W}] {file_name}")

    while True:
        try:
            choice = int(input(f"  [{R}INPUT{W}] Enter file number: "))
            if 1 <= choice <= len(txt_files):
                scrobble_tracks_from_file(network, txt_files[choice - 1], proxies)
                break
            else:
                print(f"  [{R}ERROR{W}] Please enter a valid number.")
                time.sleep(2)
        except (ValueError, KeyboardInterrupt):
            print(f"  [{R}ERROR{W}] Invalid input.")
            time.sleep(2)
            return


# -------------------- Spotify Extraction --------------------
def check_spotify_credentials(client_id, client_secret):
    """Check if Spotify credentials are valid."""
    print(f"  [{R}INFO{W}] Checking Spotify credentials...")
    time.sleep(2)
    if not all([client_id, client_secret]):
        print(f"  [{R}ERROR{W}] Spotify credentials are missing in config.json")
        time.sleep(2)
        return None
    try:
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
        sp.search(q="test", limit=1) 
        print(f"  [{R}INFO{W}] Spotify credentials are valid.")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"  [{R}ERROR{W}] Invalid Spotify credentials: {e}")
        time.sleep(2)
        return False

def extract_artist_songs(client_id, client_secret):
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    artist_name = input(f"  [{R}INPUT{W}] please enter the artist name: ")
    file_path = input(f"  [{R}INPUT{W}] please enter the file name to save songs: ")
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    
    results = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
    if not results['artists']['items']:
        print(f"  [{R}ERROR{W}] artist not found.")
        time.sleep(2)
        return
    
    artist_id = results['artists']['items'][0]['id']
    artist_name = results['artists']['items'][0]['name'] 

    print(f'  [{R}INFO{W}] fetching songs for {artist_name}, please wait...\n')

    albums = []
    album_results = sp.artist_albums(artist_id=artist_id, album_type='album,single', limit=50)
    albums.extend(album_results['items'])

    while album_results['next']:
        album_results = sp.next(album_results)
        albums.extend(album_results['items'])


    seen_albums = set()
    unique_albums = [a for a in albums if not (a['name'] in seen_albums or seen_albums.add(a['name']))]

    songs_list = []
    save_path = f"./songlist/{file_path}.txt"

    with open(save_path, 'w', encoding='utf-8') as file:
        for album in unique_albums:
            album_name = album['name']
            tracks = sp.album_tracks(album['id'])

            for track in tracks['items']:
                song_data = {
                    'song_name': track['name'],
                    'artist_name': artist_name,
                    'album_name': album_name
                }
                songs_list.append(song_data)


                print(f"  [{R}SONG{W}] {track['name']}  |  Album: {album_name}")

         
                file.write(f"Song: {track['name']} | Artist: {artist_name} | Album: {album_name}\n")

    print(f"\n  [{R}INFO{W}] extracted {len(songs_list)} songs saved to {save_path}")
    time.sleep(2)

def extract_playlist_id(url):
    """Extract playlist ID from Spotify URL."""
    match = re.search(r'playlist/([a-zA-Z0-9]+)\??', url)
    return match.group(1) if match else None


def extract_playlist_songs(client_id, client_secret):
    """Extract songs from a Spotify playlist and save them."""
    clear_screen()
    banner()
    playlist_url = input(f"  [{R}INPUT{W}] Enter Spotify playlist URL: ")
    file_path = input(f"  [{R}INPUT{W}] Enter file name to save songs: ")

    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print(f"  [{R}ERROR{W}] Invalid playlist URL.")
        return

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
    results = sp.playlist_tracks(playlist_id)

    songs = []
    for item in results['items']:
        track = item['track']
        songs.append({
            'song_name': track['name'],
            'artist_name': track['artists'][0]['name'],
            'album_name': track['album']['name']
        })

    with open(f"./songlist/{file_path}.txt", 'w', encoding='utf-8') as file:
        for s in songs:
            print(f"  [{R}SONG{W}] {track['name']}  |  Artist: {s['artist_name']}  |  Album: {s['album_name']}")
            file.write(f"Song: {s['song_name']} | Artist: {s['artist_name']} | Album: {s['album_name']}\n")

    print(f"  [{R}INFO{W}] Saved {len(songs)} songs to {file_path}.txt")
    time.sleep(2)

# -------------------- Main --------------------

def main():
    config = load_config()

    proxies = fetch_proxies()
    
    network = authenticate_lastfm(
        config['API_KEY'],
        config['API_SECRET'],
        config['LASTFM_USERNAME'],
        config['LASTFM_PASSWORD']
    )
    if not check_spotify_credentials(config['client_id'], config['client_secret']):
        sys.exit(1)
    if not network:
        sys.exit(1)
    while True:
        clear_screen()
        user = network.get_authenticated_user()
        banner()
        print(Center.XCenter(f"  {R}LAFM{W} - Last.fm Auto Scrobbler"))
        print(Center.XCenter(f"  {R}Good day{W} {user.get_name()}"))
        print(Center.XCenter(f"  Made by {R}124dev{W}"))
        print("      1. Scrobble from file")
        print("      2. Scrape Spotify")
        print("      3. Exit")
        choice = input(f"      [{R}INPUT{W}]: ")

        if choice == "1":
            choose_song_list(network, proxies)
        elif choice == "2":
            clear_screen()
            banner()
            print("      1. Scrape artist songs")
            print("      2. Extract songs from playlist")
            print("      3. Back to main menu") 
            choice = input(f"      [{R}INPUT{W}]: ")
            if choice == "1":
                extract_artist_songs(config['client_id'], config['client_secret'])
            elif choice == "2":
                extract_playlist_songs(config['client_id'], config['client_secret'])
            elif choice == "3":
                continue
        elif choice == "3":
            print(f"      [{R}INFO{W}] Exiting program...")
            time.sleep(1)
            sys.exit(0)
        else:
            print(f"      [{R}ERROR{W}] Invalid choice.")
            time.sleep(2)


if __name__ == "__main__":
    main()

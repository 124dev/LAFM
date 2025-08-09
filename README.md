

# LAFM

**LAFM** is a Python-based CLI tool that uses the **Spotify API** and **pylast API** to automatically scrobble tracks to **Last.fm**.

---

## Features
- Scrape all songs from an artist or playlist on Spotify
- Rotate proxies automatically while scrobbling
- Scrobble tracks  to Last.fm  

---


## Installation: 
```
git clone https://github.com/124dev/LAFM.git
cd LAFM
pip install -r requirements.txt
```


## Configuration: 
1. Get you Last.fm API account: https://www.last.fm/api/account/create
2. Get your Spotify App:  https://developer.spotify.com/dashboard
3. Edit the config.json file in the project root:

```
{
"API_KEY": "YOUR LASTFM API KEY",
"API_SECRET": "YOUR LAST FM SECRET KEY",
"LASTFM_USERNAME": "YOUR LASTFM USERNAME",
"LASTFM_PASSWORD": "YOUR LASTFM PASSWORD",
"client_id": "YOUR SPOTIFY CLIENT ID",
"client_secret": "YOUR SPOTIFY SECRET"
}
```
## Usage:

```
python scrobble.py
```


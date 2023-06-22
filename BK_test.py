# 1 - pobieranie linku w formie string z linku do yt

# import requests

# x = requests.get("https://youtube.com/playlist?list=PLIM2IXHjLzGMA1NjX1-_mizbkiNhaydHt")
# print(x.url)

# 2 - pobieranie listy linków w postaci stringów z playlisty
from youtubesearchpython import *

playlistVideos = Playlist.getVideos(
    "https://youtube.com/playlist?list=PL6-nym1-0TdWnICiAzd6CUXCg2crQ18Yq"
)
# print(playlistVideos)

# for video in playlistVideos:
#     video_url = video["link"]
#     print(video_url)

for key in playlistVideos:
    value = playlistVideos[key]
    print(value)

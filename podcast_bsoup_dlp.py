import yt_dlp
import requests
import wget
import pandas as pd
from bs4 import BeautifulSoup
import os

options = {
        "format": "m4a/bestaudio/best",
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
    }

dlp_scraper = yt_dlp.YoutubeDL(options)

# Variables
link_list_all = []
title_list_all = []
time_list_all = []

# Here is the input for creator URL profile
URL_setup = "https://www.youtube.com/watch?v=0Wau6QrESvc&list=PLUWDBVpNIE51d-kaYJyIOIE9fm7RNqI8C"

# Constructing parsed soup through requests [get().text return the components of page, simple get() returns code]
prepared_soup = BeautifulSoup(requests.get(URL_setup).text, 'lxml')

for episodes in prepared_soup.find_all('a', {'role': 'listitem'}):
    # Title of creators show + subtitle of episodes - in case for further validation
    title = prepared_soup.find('title').text
    full_title = title + " " + episodes.find('div', {'class': 'e3ZUqe'}).text
    title_list_all.append(full_title)

    # Also through div tags and classes if the first is not working
    # title = soup.find('div', {'class':'ZfMIwb'}).text

    # Extracting certain links to podcasts through find and JsName tags and splitting from the rest of data
    link = episodes.find('div', {'jsname': 'fvi9Ef'})['jsdata'].split(';')[1]
    link_list_all.append(link)

    # Upload time through class
    upload_time = episodes.find('div', {'class': 'OTz6ee'}).text
    time_list_all.append(upload_time)

    dlp_scraper.download(link)

    print(title)

print(prepared_soup)
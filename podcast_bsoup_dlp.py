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
url_main_list = []
channels_title_list = []

# Here is the input for creator URL profile
URL_setup = "https://podcasts.google.com/?hl=pl"

# Constructing parsed soup through requests [get().text return the components of page, simple get() returns code]
prepared_soup = BeautifulSoup(requests.get(URL_setup).text, 'lxml')

meta_list = prepared_soup.find_all('a', {'class': 'c9x52d'})
# test = prepared_soup.find('div', {'jsname': 'X7oyne'})['jsdata']

for meta in meta_list:
    url_main_list.append("https://podcasts.google.com" + meta['href'][1:-1])
    channels_title_list.append(meta.find('div', {'class': 'eWeGpe'}).text)

for iteration, channels in enumerate(url_main_list):

    current_url = channels
    channel_soup = BeautifulSoup(requests.get(current_url).text, 'lxml')

    os.mkdir(channels_title_list[iteration])
    os.chdir(channels_title_list[iteration])

    for episodes in channel_soup.find_all('a', {'role': 'listitem'}):

        print(channel_soup.find_all('a', {'role': 'listitem'}))
        # Title of creators show + subtitle of episodes - in case for further validation
        full_title = episodes.find('div', {'class': 'e3ZUqe'}).text
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

    os.chdir("..")

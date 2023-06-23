# NOTE:
# Before using this script - use prox_tester which validate for you prox list to restrict problems with connections
# Keyboard interrupt with Ctrl+Z
# Here I have used static list of UA, so it needs update once in a while
# If you are intrested in lib generating approach, check header.py
# There is one thing that can be added to simulate human-like behavior
# In header section can be added - Referer - the URL of site "previously" visited by person
# Additionaly there is Sec-Fetch section which can be useful with difficulty with SSL

import requests
import random
import time
import yt_dlp
import requests
import wget
import pandas as pd
from bs4 import BeautifulSoup
import os

# Script is using "valid_prox.txt" which is the product of prox_tester
try:
    with open("Python_scripts/valid_prox.txt", "r") as item:
        prox_list = item.read().split("\n")

    with open("Python_scripts/static_agents_list.txt", "r") as item:
        agents_list = item.read().split("\n")


    # Function for information extraction using beautifulsoup4 and prox
    def soup_extracting(url_request, prox_status, prox_listed):
        try:
            # Constructing parsed soup through requests [get().text return the components of page, simple get() returns code]
            global extracted_soup
            global finished
            finished = False
            # Functions tries extracting information as long as user don't interrupt it - it jumps through delivered prox
            # If you want to try extract information from other website - change URL_setup below - if you want to use other
            # method of extraction change fragment inside try statement
            while finished is False:
                try:
                    extracted_soup = BeautifulSoup(requests.get(url_request, timeout=15,
                                                                headers={'User-Agent': random.choice(agents_list),
                                                                         'Accept-Language': 'en, en-gb, pl',
                                                                         'Accept-Encoding': 'br, gzip, deflate',
                                                                         'Accept': 'text/html, audio/*, video/*, image/*'},
                                                                proxies={
                                                                    "http": prox_listed[prox_status],
                                                                    "https": prox_listed[prox_status],
                                                                }).text, 'lxml')
                    print("\n" + "Prox success")
                    print(prox_listed[prox_status] + "\n")
                    finished = True
                except:
                    print("\n" + "Prox failed")
                    print(prox_listed[prox_status] + "\n")
                    prox_status += 1
                    if prox_status == len(prox_listed):
                        prox_status = 0
                    continue
                prox_status += 1
                if prox_status == len(prox_listed):
                    prox_status = 0
            return extracted_soup, prox_status
        except KeyboardInterrupt:
            pass


    print(prox_list)

    prox_iter = 0

    # Variables
    link_list_all = []
    title_list_all = []
    time_list_all = []
    url_main_list = []
    channels_title_list = []

    # Directory management for server storage
    os.chdir("/mnt/s01/praktyki/")

    if os.path.exists("gp_storage_test"):
        os.chdir("gp_storage_test")
    else:
        os.mkdir("gp_storage_test")
        os.chdir("gp_storage_test")

    # Here is the input for main URL
    URL_setup = "https://podcasts.google.com/?hl=pl"
    # URL_setup = "https://podcasts.google.com/search/polskie?hl=pl" # Polish search website

    # Extracting information using function
    prepared_soup, prox_iter = soup_extracting(URL_setup, prox_iter, prox_list)

    # Listing positions from main website
    meta_list = prepared_soup.find_all('a', {'class': 'c9x52d'})
    # test = prepared_soup.find('div', {'jsname': 'X7oyne'})['jsdata']

    # Gathering data for link extraction and channels
    for meta in meta_list:
        url_main_list.append("https://podcasts.google.com" + meta['href'][1:-1])
        channels_title_list.append(meta.find('div', {'class': 'eWeGpe'}).text)

    # For each channel, extracting episodes links and data, making dirs for them and sorting
    for iteration, channels in enumerate(url_main_list):
        current_url = channels
        channel_soup, prox_iter = soup_extracting(current_url, prox_iter, prox_list)

        os.mkdir(channels_title_list[iteration])
        os.chdir(channels_title_list[iteration])

        # For each download - there is init for dlp instance
        for episodes in channel_soup.find_all('a', {'role': 'listitem'}):
            finished = False
            while finished is False:
                try:
                    # Options init for DLP
                    options = {
                        "format": "m4a/bestaudio/best",
                        "socket_timeout": '20',
                        "proxy": str(prox_list[prox_iter]),
                        "http_headers": {'User-Agent': random.choice(agents_list),
                                         'Accept-Language': 'en, en-gb, pl',
                                         'Accept-Encoding': 'br, gzip, deflate',
                                         'Accept': 'text/html, audio/*, video/*, image/*'},
                        "debug_printtraffic": True,
                        # ?? See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
                        "postprocessors": [
                            {  # Extract audio using ffmpeg
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": "wav",
                            }
                        ],
                    }

                    # Above debug_printtraffic was used to check functionality of UA
                    # It prints a lot of information, but if you want to check it out uncomment it

                    # Wait time for requests
                    sec = random.randint(0, 10)
                    print("\nWaiting for " + str(sec) + " sec")
                    time.sleep(sec)
                    print("Proceeding\n")

                    # DLP Scraper init
                    dlp_scraper = yt_dlp.YoutubeDL(options)

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

                    # Launching of scraper
                    dlp_scraper.download(link)
                    print("\n" + "Positive prox res")
                    print(prox_list[prox_iter])
                    print("Success:" + str(full_title) + "\n")
                    finished = True
                    del dlp_scraper
                    del options
                except:
                    print("\n" + "Negative prox res")
                    print(prox_list[prox_iter])
                    print("Prox failed\n")
                    prox_iter += 1
                    if prox_iter == len(prox_list):
                        prox_iter = 0
                    del dlp_scraper
                    del options
                    continue
                prox_iter += 1
                if prox_iter == len(prox_list):
                    prox_iter = 0

        # Returning to main
        os.chdir("..")

except KeyboardInterrupt:
    pass

# NOTE:
# Before using this script - use prox_tester which validate for you prox list to restrict problems with connections
# Keyboard interrupt with Ctrl+Z
# Here I have used static list of UA, so it needs update once in a while
# If you are interested in lib generating approach, check header.py
# There is one thing that can be added to simulate human-like behavior
# In header section can be added - Referer - the URL of site "previously" visited by person
# Additionally there is Sec-Fetch section which can be useful with difficulty with SSL

import os
import random
import time
import unicodedata

import requests
import yt_dlp
from bs4 import BeautifulSoup


class gp_operator:
    def __init__(self, valid_path, agents_path, storage_path, ip_rotation, headers_alteration):
        self.valid_path = valid_path
        self.agents_path = agents_path
        self.storage_path = storage_path
        self.ip_rotation = ip_rotation
        self.headers_alteration = headers_alteration

        self.ip_queue = 0

        self.extracted__main_info = None
        self.extracted__subpage_info = None

        self.request_timeout = 10
        self.timeout = 15
        self.lang_accept = 'en, en-gb, pl'
        self.encoding_accept = 'br, gzip, deflate'
        self.header_accept = 'text/html, audio/*, video/*, image/*'

        self.__url_list = []
        self.__link_list = []
        self.__positions_list = []
        self.title_list = []
        self.time_list = []
        self.channels_list = []

        # Here is the input for main URL
        # self.URL_setup = "https://podcasts.google.com/?hl=pl"
        self.URL_setup = "https://podcasts.google.com/search/polskie?hl=pl"

        with open(self.valid_path, "r") as item:
            self.ip_valid_list = item.read().split("\n")

        with open(self.agents_path, "r") as item:
            self.agents_list = item.read().split("\n")

    def base_info_extracting(self, url):

        extracted_info = None

        try:
            # Constructing parsed soup through requests [get().text return the components of page, simple get() returns code]
            request_finished = False
            # Functions tries extracting information as long as user don't interrupt it - it jumps through delivered prox
            # If you want to try extract information from other website - change URL_setup below - if you want to use other
            # method of extraction change fragment inside try statement

            while request_finished is False:
                try:

                    if self.ip_queue == len(self.ip_valid_list):
                        self.ip_queue = 0

                    if self.ip_rotation is True:
                        ip_set = dict(http=self.ip_valid_list[self.ip_queue], https=self.ip_valid_list[self.ip_queue])
                    else:
                        ip_set = {}

                    if self.headers_alteration is True:
                        header = {'User-Agent': random.choice(self.agents_list),
                                  "Accept-Language": self.lang_accept,
                                  "Accept-Encoding": self.encoding_accept,
                                  "Accept": self.header_accept}
                    else:
                        header = {}

                    extracted_info = BeautifulSoup(requests.get(url, timeout=self.timeout,
                                                                     headers=header,
                                                                     proxies=ip_set
                                                                     ).text, 'lxml')

                    if self.ip_rotation is True:
                        print("\n" + "IP success")
                        print(self.ip_valid_list[self.ip_queue] + "\n")
                        self.ip_queue += 1
                    else:
                        print("\n" + "Success")

                    request_finished = True

                except:
                    print("\n" + "IP failed")
                    print(self.ip_valid_list[self.ip_queue] + "\n")
                    self.ip_queue += 1

                    continue

            return extracted_info

        except KeyboardInterrupt:
            pass

    def audio_extraction(self):
        # noinspection SpellCheckingInspection
        try:
            # Directory management for server storage
            os.chdir(self.storage_path)

            if os.path.exists("gp_storage"):
                os.chdir("gp_storage")
            else:
                os.mkdir("gp_storage")
                os.chdir("gp_storage")

            # Extracting information using function
            self.extracted__main_info = self.base_info_extracting(self.URL_setup)

            # Listing positions from main website
            self.__positions_list = self.extracted__main_info.find_all('a', {'class': 'c9x52d'})
            # self.__positions_list = self.extracted_info.find_all('div', {'jsname': 'X7oyne'})['jsdata']

            # Gathering data for link extraction and channels
            for sub_position in self.__positions_list:
                self.__url_list.append("https://podcasts.google.com" + sub_position['href'][1:-1])
                self.title_list.append(sub_position.find('div', {'class': 'eWeGpe'}).text)

            for item in self.title_list:
                self.channels_list.append(unicodedata.normalize('NFD', item.replace(" ", "_")).encode('ascii', 'ignore'))

                self.title_list = []

            # For each channel, extracting episodes links and data, making dirs for them and sorting
            for iteration, channel in enumerate(self.__url_list):
                try:
                    current_url = channel
                    self.extracted__subpage_info = self.base_info_extracting(current_url)

                    if os.path.exists(self.channels_list[iteration]):
                        os.chdir(self.channels_list[iteration])
                    else:
                        os.mkdir(self.channels_list[iteration])
                        os.chdir(self.channels_list[iteration])

                    for episode in self.extracted__subpage_info.find_all('a', {'role': 'listitem'}):
                        request_finished = False
                        while request_finished is False:
                            try:

                                # Title of creators show + subtitle of episodes - in case for further validation
                                self.title_list.append(
                                    unicodedata.normalize('NFD', episode.find('div', {'class': 'e3ZUqe'}).text.replace(" ", "_")).encode('ascii', 'ignore'))

                                # Also through div tags and classes if the first is not working
                                # title = soup.find('div', {'class':'ZfMIwb'}).text

                                # Extracting certain links to podcasts through find and JsName tags and splitting from the rest of data
                                self.__link_list.append(episode.find('div', {'jsname': 'fvi9Ef'})['jsdata'].split(';')[1])

                                # Upload time through class
                                self.time_list.append(episode.find('div', {'class': 'OTz6ee'}).text.replace(" ", "_"))

                                if os.path.exists(str(self.title_list[-1]) + ".wav"):
                                    break
                                else:

                                    # Options init for DLP
                                    options = {
                                        "format": "m4a/bestaudio/best",
                                        "socket_timeout": '20',
                                        "outtmpl": str(self.title_list[-1]),
                                        "debug_printtraffic": True,
                                        # ?? See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
                                        "postprocessors": [
                                            {  # Extract audio using ffmpeg
                                                "key": "FFmpegExtractAudio",
                                                "preferredcodec": "wav",
                                            }
                                        ],
                                    }

                                    if self.ip_queue == len(self.ip_valid_list):
                                        self.ip_queue = 0

                                    if self.headers_alteration is True:
                                        header = {'User-Agent': random.choice(self.agents_list),
                                                  "Accept-Language": self.lang_accept,
                                                  "Accept-Encoding": self.encoding_accept,
                                                  "Accept": self.header_accept}
                                        options["http_headers"] = header

                                    if self.ip_rotation is True:
                                        ip_set = self.ip_valid_list[self.ip_queue]
                                        options["proxy"] = ip_set

                                    # Above debug_printtraffic was used to check functionality of UA
                                    # It prints a lot of information, but if you want to check it out uncomment it

                                    # Wait time for requests
                                    timeout = random.randint(0, self.request_timeout)
                                    print("\nWaiting for " + str(timeout) + " sec")
                                    time.sleep(timeout)
                                    print("Proceeding\n")

                                    # DLP Scraper init
                                    dlp_scraper = yt_dlp.YoutubeDL(options)

                                    # Launching of scraper
                                    dlp_scraper.download(self.__link_list[-1])

                                    if self.ip_rotation is True:
                                        print("\n" + "Positive IP response")
                                        print(self.ip_valid_list[self.ip_queue])
                                        self.ip_queue += 1
                                    else:
                                        print("Success:" + str(self.title_list[-1]) + "\n")

                                    request_finished = True

                                    del dlp_scraper
                                    del options

                            except Exception as e:
                                print("Caught : " + str(e))

                                if self.ip_rotation is True:
                                    print("\n" + "Negative IP response")
                                    print(self.ip_valid_list[self.ip_queue])
                                    print("IP failed\n")

                                self.ip_queue += 1

                                del dlp_scraper
                                del options
                                continue

                    # Returning to main
                    os.chdir("..")

                except Exception as e:
                    print("Episode extraction failed " + str(e))
        except Exception as e:
            print("Information/channel failed + " + str(e))

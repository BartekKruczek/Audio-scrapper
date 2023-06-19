import yt_dlp
import requests
import wget
import pandas as pd
from bs4 import BeautifulSoup
import os

URL_setup = ""

prepared_soup = BeautifulSoup(requests.get().text, 'lxml')

def download()
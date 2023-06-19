import yt_dlp
import requests
import wget
import pandas as pd
from bs4 import BeautifulSoup
import os

def download_podcasts(soup, title):
    i = 0
    time_l = []
    ID_l = []
    description_l = []
    length_l = []
    link_l = []
    name_l = []
    for podcast in soup.find_all('a', {'role': 'listitem'}):
        time = podcast.find('div', {'class': 'OTz6ee'}).text
        i += 1
        time_l.append(time)

        link = podcast.find('div', {'jsname': 'fvi9Ef'})['jsdata'].split(';')[1]
        link_l.append(link)

        name = podcast.find('div', {'class': 'e3ZUqe'}).text
        name_l.append(name)
        print(link_l)

        print(i, ":", time)
        filename = wget.download(link, out=title)
        print(filename)
        os.rename(filename, title+'/audio'+str(i)+'.mp3') # use if the downloaded name is always the same
        ID_l.append('audio'+str(i))
        ID_l.append(str(i))  # ID is just the filename for later access

        try:  # sometimes there's no description
            description = podcast.find('div', {'class': 'LrApYe'}).text
        except:
            description = 'None'
        if description is None:
            description = 'None'
        description_l.append(description)

        length = podcast.find('span', {'class': 'gUJ0Wc'}).text
        length_l.append(length)

    df = pd.DataFrame(list(zip([title] * len(ID_l), ID_l, name_l, time_l, description_l, length_l, link_l)),
                      columns=['Show', 'ID', 'Episode', 'Time', 'Description', 'Length', 'Link'])
    return df

URLs = ["https://podcasts.google.com/feed/aHR0cHM6Ly93d3cucm1mLmZtL3Jzcy9wb2RjYXN0L2JhamtpLWRsYS1kb3Jvc2x5Y2gueG1s?sa=X&ved=0CEcQjs4CKAFqFwoTCOig7qWWz_8CFQAAAAAdAAAAABAw&hl=pl"]

info_df_list = []
for url in URLs:
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    title = soup.find('div', {'class':'ZfMIwb'}).text # This is the name of the show
    print(soup)
    print(title)
    os.mkdir(title) # make a new folder to contain podcasts from the same show
    df = download_podcasts(soup, title) # function details below
    info_df_list.append(df)
info_all_podcasts = pd.concat(info_df_list)


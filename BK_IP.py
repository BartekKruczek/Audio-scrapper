# wersja 7
# import time
# import yt_dlp
# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By


# def change_ip(driver):
#     driver.get("https://www.whatismyip.com/")
#     time.sleep(5)
#     ip_element = driver.find_element(By.ID, "ipv4")
#     new_ip = ip_element.get_attribute("textContent")
#     proxies = {"http": f"http://{new_ip}", "https": f"https://{new_ip}"}
#     return proxies


# def download_playlist_audio(playlist_url, output_path, change_ip_frequency):
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.binary_location = (
#         "C:/Program Files/Google/Chrome/Application/chrome.exe"
#     )
#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         with requests.Session() as session:
#             response = session.get(
#                 f"https://www.youtube.com/playlist_ajax?list={playlist_url}"
#             )
#             playlist_data = response.json()
#             videos = playlist_data["video"]

#             with webdriver.Chrome() as driver:
#                 for video in videos:
#                     video_id = video["encrypted_id"]
#                     video_url = f"https://www.youtube.com/watch?v={video_id}"
#                     video_title = video["title"]

#                     print(f"Pobieranie audio z filmu: {video_title}")

#                     proxies = change_ip(driver)

#                     ydl_opts = {
#                         "format": "bestaudio/best",
#                         "postprocessors": [
#                             {
#                                 "key": "FFmpegExtractAudio",
#                                 "preferredcodec": "wav",
#                                 "preferredquality": "192",
#                             }
#                         ],
#                         "outtmpl": f"{output_path}/{video_title}.wav",
#                         "ignoreerrors": True,
#                         "proxy": proxies["http"],
#                     }

#                     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                         ydl.download([video_url])

#                     time.sleep(change_ip_frequency)

#     except Exception as e:
#         print(f"Wystąpił błąd: {str(e)}")

#     finally:
#         driver.quit()


# # Ustawienia
# playlist_url = "PLJYMhYKidccNMcmNVIqpFLkmOAtKgIfu-"
# output_path = "C:/Users/krucz/Documents/Projekty/Anonimowi-Akustycy/Nagrania"
# change_ip_frequency = 5

# # Wywołanie funkcji
# download_playlist_audio(playlist_url, output_path, change_ip_frequency)

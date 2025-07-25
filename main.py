from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import yt_dlp

def clear_terminal():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options   )

url = "https://feelthemusi.com/playlist/ot3272"
driver.get(url)

time.sleep(5)  

soup = BeautifulSoup(driver.page_source, "html.parser")

title = soup.title.string if soup.title else "No title found"
title = title.split("|")[0].strip() if "|" in title else title
clear_terminal()

print(f"Playlist Name: {title}")

time.sleep(5)

all_links = [a.get("href") for a in soup.find_all("a", href=True)]

filtered_links = [
    link for link in all_links
    if not (link.startswith("https://itunes.apple.com") or link.startswith("musi://"))
]

for link in filtered_links:
    print(link)

driver.quit()

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s', 
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(filtered_links)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import yt_dlp
import http.server
import socketserver
import socket
import shutil

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

url = input("Enter Musi Playlist URL: ")
driver.get(url)

PORT = 8000

time.sleep(5)  

soup = BeautifulSoup(driver.page_source, "html.parser")

title = soup.title.string if soup.title else "No title found"
title = title.split("|")[0].strip() if "|" in title else title
clear_terminal()

print(f"Playlist Name: {title}")

if not os.path.exists(title):
    os.makedirs(title)

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
    'cookiefile': 'cookies.txt',
    'ignoreerrors': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': os.path.join(title, '%(title)s.%(ext)s'),
    # 'verbose': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(filtered_links)

folder_to_zip = title
output_zip = title
FILE_TO_SERVE = title + ".zip"

print("Zipping playlist: " + title)
shutil.make_archive(output_zip, "zip", folder_to_zip)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/download":
            self.send_response(200)
            self.send_header("Content-type", "application/octet-stream")
            self.send_header("Content-Disposition", f'attachment; filename="{os.path.basename(FILE_TO_SERVE)}"')
            self.end_headers()
            with open(FILE_TO_SERVE, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File Not Found")

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

with socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
    clear_terminal()
    print("YOUR PHONE MUST BE ON THE SAME NETWORK AS YOUR COMPUTER!!!!")
    print("Download the music to your phone: http://" + local_ip + ":" + str(PORT))
    print("Once done, use Control + C to exit")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()


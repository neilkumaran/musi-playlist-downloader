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

conf = 'y'
menuchoice = ''
PORT = 8000

def clear_terminal():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

if not os.path.isfile("cookies.txt"):
    clear_terminal()  
    conf = input("Cookies.txt was not found\nIt is highly recommended that you add your cookies so you can download age restricted content and private videos.\n\nInstructions to do so are on https://github.com/neilkumaran/musi-playlist-downloader\nType y to confirm that you have read this.\n")

if (conf != 'y'):
    exit(0)

if not os.path.exists("db"):
    os.makedirs("db")

saved_downloads = [f for f in os.listdir("db") if f.endswith(".txt")]

options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = None

def serve_download(title):
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


def getUrl():
    clear_terminal()
    global driver
    driver = webdriver.Chrome(options=options)
    url = input("Enter Musi Playlist URL: ")
    driver.get(url)

def resumeDownload(db_file):
    with open(db_file, "r") as f:
        lines = f.read().splitlines()

    links = lines[:-1]
    progress = int(lines[-1])

    total = len(links)
    title = os.path.basename(db_file)[:-4]

    if not os.path.exists(title):
        os.makedirs(title)

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
    }

    print(f"\nResuming '{title}' from {progress}/{total}...")

    last_downloaded = progress
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for idx, link in enumerate(links, start=1):
            if idx <= progress:
                continue

            print(f"\nDownloading [{idx}/{total}]: {link}")
            try:
                ydl.download([link])
            except Exception as e:
                print(f"Failed to download {link}: {e}")

            last_downloaded = idx
            with open(db_file, "w") as f:
                f.write("\n".join(links))
                f.write(f"\n{idx}")

    if last_downloaded >= total:
        print(f"\nPlaylist '{title}' completed! Removing save file...")
        os.remove(db_file)

    serve_download(title)

if saved_downloads:
    clear_terminal()
    print("1. Download a new playlist")
    print("2. Resume a previous download")
    menuchoice = input("Enter your choice: ")

    if menuchoice == '1':
        getUrl()
    elif menuchoice == '2':
        clear_terminal()
        print("Saved Downloads:")
        for i, file in enumerate(saved_downloads, start=1):
            print(f"{i}. {file[:-4]}")
        
        choice = input("Enter the number of the playlist you want to resume: ")
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(saved_downloads):
                selected_file = saved_downloads[idx - 1]
                resumeDownload(os.path.join("db", selected_file))
            else:
                print("Invalid choice.")
        else:
            print("Invalid input")
else:
    getUrl()

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

db_file = os.path.join("db", f"{title}.txt")

if not os.path.exists(db_file):
    with open(db_file, "w") as f:
        f.write("\n".join(filtered_links)) 
        f.write("\n0")  

with open(db_file, "r") as f:
    lines = f.read().splitlines()

links_from_db = lines[:-1]  
progress = int(lines[-1])

total = len(links_from_db)

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

last_downloaded = progress
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for idx, link in enumerate(links_from_db, start=1):
        if idx <= progress:
            continue

        print(f"\nDownloading [{idx}/{total}]: {link}")
        try:
            ydl.download([link])
        except Exception as e:
            print(f"Failed to download {link}: {e}")

        last_downloaded = idx
        with open(db_file, "w") as f:
            f.write("\n".join(links_from_db))
            f.write(f"\n{idx}")

# Remove save file if all done
if last_downloaded >= total:
    os.remove(db_file)

serve_download(title)
# Musi Playlist to MP3 Downloader & Web Server

This app takes a **Musi playlist link**, downloads and converts all songs to MP3, and starts a local web server so you can **download the MP3 files directly to your phone or any device** on the same network.

## Features

- Accepts a Musi playlist URL  
- Uses **selenium** and **beautifulsoup4** to scrape the playlist and extract video links  
- Downloads audio using **yt-dlp**  
- Converts audio files to MP3 using **ffmpeg**  
- Starts a local web server for easy downloading  

## Requirements

- Python 3.7+  
- Google Chrome (installed and updated)  
- ffmpeg (installed and available in your PATH)  

## Python Libraries Used

- selenium  
- beautifulsoup4  
- yt-dlp  

These are installed with `pip install -r requirements.txt`

## Installation

1. Clone the repo:

    ```bash
    git clone https://github.com/neilkumaran/musi-playlist-downloader.git
    cd musi-playlist-downloader
    ```

2. Install ffmpeg:

    - **Windows** (Admin PowerShell or CMD):

        ```powershell
        winget install ffmpeg
        ```

    - **macOS**:

        ```bash
        brew install ffmpeg
        ```

    - **Linux (Debian/Ubuntu)**:

        ```bash
        sudo apt install ffmpeg
        ```

3. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

Make sure Chrome is installed and up to date — Selenium uses it automatically.

## Usage

1. Run the app:

    ```bash
    python main.py
    ```

2. Enter your Musi playlist URL when prompted.

3. The app downloads, converts, and starts a local web server.

4. On your phone (same Wi-Fi), open the URL shown in terminal to download MP3 files.

## Known Issues

**Age Verification Errors:**  
You need to import your cookies to confirm your age. 

https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc

I recommend this extention to export your cookies. 

IMPORTANT: Make sure before you do this, you have signed into youtube with an account that is NOT age restricted
--------

1. Install the extention

2. Press "Export All Cookies", it'll generate a file called cookies.txt

3. Place this file in the SAME LOCATION as main.py (so the same folder as main.py)

4. Try it again

WARNING: DO NOT SHARE YOUR COOKIES.TXT, TREAT IT AS YOUR PASSWORD. IF YOU SHARE YOUR COMPUTER, DELETE IT AFTER USE! NEVER GIVE YOUR COOKIES.TXT TO ANYBODY.  


## Notes

- ffmpeg is mandatory for audio conversion.  
- Chrome must be installed and updated.  
- Use this app responsibly and respect copyright.

## License

MIT License
# Spotify To MP3

## Project Overview

**Spotify To MP3** is a Python application that allows you to retrieve and download your favorite songs from a Spotify playlist as MP3 files. It seamlessly integrates with Spotify and YouTube, enabling you to enjoy your music offline, anytime, anywhere.

## How It Works

Spotify To MP3 works by following these steps:

1. **Spotify Playlist Retrieval**: The application first fetches a Spotify playlist, specified by the user. The playlist is a collection of songs you want to download.

2. **Song Search on YouTube**: For each song in the playlist, the application searches YouTube to find the corresponding music video.

3. **MP4 Video Download**: The application downloads the found music video in MP4 format. This is a crucial step in acquiring the audio content of the song.

4. **MP3 Conversion**: The downloaded MP4 video is then converted into an MP3 audio file, ensuring that you get the audio-only version of the song.

## How to Run

Follow these steps to set up and run the **Spotify To MP3** project:

1. **Clone the Repository**: Begin by cloning this repository to your local machine using the following command:
   ```bash
   git clone https://github.com/yourusername/spotify-to-mp3.git
2. **Set Up a Virtual Environment**: If you don't have Pipenv installed, you can install it with pip:
   ```bash
   pip install pipenv
   ```   
4. **Install Dependencies**: Install the required dependencies within the virtual environment:
   ```
   pipenv install
   pipenv shell
   ```
5. **Create a .env File**: Create a file named `.env` in the project directory and define the following variables:

      - `CLIENT_ID`: Your Spotify API client ID (You can obtain this from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)).
      - `CLIENT_SECRET`: Your Spotify API client secret.
      - `SECRET_KEY`: A secret key for the application (can be any unique string).

6. **Create a Spotify Playlist**: Create a Spotify playlist called "spotifyscam" or adjust the playlist name as needed. You can update the playlist name in the code to match the one you've created on Spotify.

7. **Run the Application**: Run the main Python script using the following command:
   ```
   python main.py
   ```

8. **Spotify Authentication**: The application will guide you through the Spotify authentication process. You will be prompted to log in to Spotify and grant access to the application.

9. **Enjoy the Magic**: Once authenticated, the application will start processing your playlist, downloading songs, and converting them to MP3. Sit back, relax, and enjoy the magic as your music library expands.

**Note:** Be sure to follow the legal and ethical guidelines when downloading music from YouTube. Ensure that you have the necessary rights or permissions for any copyrighted content you download.

## Disclaimer

This project is designed to help you download music from Spotify playlists, but it may not always be 100% accurate. Due to variations in song titles, artist names, and availability on YouTube, the program might occasionally download incorrect songs or fail to find certain tracks. 

This project is for educational and personal use only. Downloading copyrighted material without the necessary permissions may infringe on intellectual property rights and may be subject to legal restrictions in your jurisdiction. Be responsible and use this application in compliance with applicable laws and regulations. The project's creators and maintainers are not responsible for any misuse of this software.

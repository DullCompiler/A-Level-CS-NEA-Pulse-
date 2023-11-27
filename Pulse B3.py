# Pulse Beta 3 | Made by Alexander Richard Dennant | NEA Project for Computer Science

# Imports —————————————————————————————————————————————
import os
import pytube
import asyncio
import requests
from shazamio import Shazam
from tkinter import filedialog
from tkinter import messagebox
from customtkinter import CTk as ctk
from customtkinter import CTkLabel, CTkButton, CTkFrame

# Shazamio Function + Song Data Collection —————————————————————————————————————————————

# Initialize youtube_links list
youtube_links = []

# Shazamio Function
async def main(filepath):
    # Initialize Shazam class
    shazam = Shazam()

    # Make a Shazam of the audio file
    out = await shazam.recognize_song(filepath)

    # Get track data
    track = out['track']
    print(f"Title: {track['title']}, Artist: {track['subtitle']}")

    # Get related tracks
    related = await shazam.related_tracks(track_id=track['key'], limit=5, offset=0)
    for related_track in related['tracks']:
        title = related_track['title']
        artist = related_track['subtitle']
        print(f"\nRelated song: {title} by {artist}")

        # Search YouTube for links
        results = search_youtube(f"{title} {artist}")
        if results:
            youtube_links.append(results[0])
            print("Youtube Link: " + results[0])
        else:
            print('No YouTube results found.')

# Youtube Data Grab
def search_youtube(query):
    # Set up the API request parameters
    params = {
        'key': 'AIzaSyDQ4pqmgDr0niIQvT0aPPte5Ew7yZg5Q04',
        'part': 'snippet',
        'q': query,
        'maxResults': 1,
        'type': 'video'
    }

    try:
        # Send the API request
        response = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
        response.raise_for_status()

        # Parse the response JSON
        data = response.json()

        # Retrieve the links of the videos
        results = []
        if 'items' in data and data['items']:
            for item in data['items']:
                video_id = item['id']['videoId']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                results.append(video_url)

        return results
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None
        
# Music Downloading Function


# Music Data Collection Function


# Shazamio Function + Song Data Collection End —————————————————————————————————————————————

# Start Up Menu —————————————————————————————————————————————

# Check internet connectivity
def check_internet():
    try:
        r = requests.get('http://google.com')
        return r.status_code == 200
    except:
        return False

# File Handling —————————————————————————————————————————————
def open_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        print(f"File opened: {filepath}")
        asyncio.run(main(filepath))

def exit_program():
    ctk_root.destroy()

# GUI Start —————————————————————————————————————————————

def center_window(width=500, height=240):
    # get screen width and height
    screen_width = ctk_root.winfo_screenwidth()
    screen_height = ctk_root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    ctk_root.geometry('%dx%d+%d+%d' % (width, height, x, y))


ctk_root = ctk()
ctk_root.title("PULSE: Startup Menu")
#ctk_root.geometry("500x240") - this line is no needed as center_window function will take care of geometry
ctk_root.resizable(False,False)

# Use the center_window function instead of the previous line
center_window(500, 240)

# Title and subtitle
title_label = CTkLabel(ctk_root, text="PULSE", font=("Helvetica", 30, "bold"))
title_label.pack(padx=20, pady=(20, 0))

subtitle_label = CTkLabel(ctk_root, text="Startup menu", font=("Helvetica", 12))
subtitle_label.pack(padx=20, pady=(0, 20))

# Internet connection status
internet_label = CTkLabel(ctk_root, text="", font=("Helvetica", 10, "bold"))

if check_internet():
    internet_label.configure(text="Internet: Connected")
else:
    messagebox.showwarning("No Internet", "Error 01 : No Internet | Pulse requires an active internet connection in order to enable necessary functionalty")
    exit_program()

internet_label.pack(padx=20, pady=20)

# Buttons
button_frame = CTkFrame(ctk_root)
button_frame.pack(side="bottom", pady=20)

CTkButton(button_frame, text='Exit', command=exit_program).pack(side="left", padx=(0, 5))
CTkButton(button_frame, text='Open File', command=open_file).pack(side="left", padx=(5, 0))

ctk_root.mainloop()

# Start Up Menu End —————————————————————————————————————————————

# Program End —————————————————————————————————————————————
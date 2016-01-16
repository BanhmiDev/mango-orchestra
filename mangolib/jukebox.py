#!/usr/bin/env python3
from mpd import MPDClient

class Jukebox():

    def __init__(self):
        # Connect to MPD
        self.client = MPDClient()
        self.client.connect("localhost", 6600)
     
        # Jukebox data
        self.title = "" # Song title
        self.artist = "" # Song artist
        self.src = "/static/test.mp3" # TODO: Song file
        self.time = 0 # Seek time
        self.end_time = 0 # Song end time
        self.listeners = 0 # Listeners
        
        self.queue = [] # TODO: Playlist management
        self.copied = False

        self.sync() # Sync immediately

    def join(self):
        self.listeners += 1

    def leave(self):
        self.listeners -= 1

    def add_song(self, song):
        """TODO: Add song to queue."""
        queue.append(0, song)

    def get_current(self):
        """TODO: Overhaul."""
        return {
            'title': self.title,
            'artist': self.artist,
            'src': self.src
        }

    def get_next(self):
        """TODO: Use the next song in queue."""
        if not self.queue:
            self.title = ""
            self.artist = ""
            self.src = ""
            self.time = 0
        else:
            song = self.queue.pop()
            self.title = song.title
            self.artist = song.artist
            self.src = song.src
            self.time = 0
        return self.get_current()

    def sync(self):
        song = self.client.currentsong()
        status = self.client.status()

        if status["state"] == "stop": # Do nothing
            return

        if 'title' not in song:
            self.title = "Unknown"
        else:
            self.title = song["title"]

        if 'artist' not in song:
            self.artist = "Unknown"
        else:
            self.artist = song["artist"]

        # TODO: src management
        self.src = "/static/test.mp3"
        time_split = status["time"].split(":");
        self.time = time_split[0]
        self.end_time = time_split[1]


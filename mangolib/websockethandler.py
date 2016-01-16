#!/usr/bin/env python3
import tornado.websocket
import tornado.ioloop

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    
    def initialize(self, jukebox):
        self.jukebox = jukebox

    def open(self):
        """Handle joining."""
        self.jukebox.join()
        
        # Sync with client
        self.sync() # Sync immediately
        self.periodic = tornado.ioloop.PeriodicCallback(self.sync, 1000) # Scheduling
        self.periodic.start()

    def on_message(self, message):
        mp("on_message", message);
    
    def on_close(self):
        """Handle closing."""
        self.jukebox.leave()
        self.periodic.stop()

    def sync(self):
        """Sync music to client."""
        result = {
            "src": self.jukebox.src,
            "title": self.jukebox.title,
            "artist": self.jukebox.artist,
            "time": self.jukebox.time,
            "end_time": self.jukebox.end_time,
            "listeners": self.jukebox.listeners
        }
        self.write_message(result)



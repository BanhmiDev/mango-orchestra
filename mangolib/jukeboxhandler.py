#!/usr/bin/env python3
import tornado.web

class JukeboxHandler(tornado.web.RequestHandler):
    
    def initialize(self, jukebox):
        self.jukebox = jukebox

    def get(self):
        """Return basic jukebox information."""
        if self.get_argument("song") == "current":
            self.finish(self.jukebox.get_current())
        elif self.get_argument("song") == "next":
            self.finish(self.jukebox.get_next())



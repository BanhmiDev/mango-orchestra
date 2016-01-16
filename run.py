import os
import json
import shutil

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

from mangolib.jukebox import Jukebox
from mangolib.jukeboxhandler import JukeboxHandler
from mangolib.websockethandler import WebSocketHandler

class Application(tornado.web.Application):
    def __init__(self):
        self.jukebox = Jukebox()

        self.periodic = tornado.ioloop.PeriodicCallback(self.sync, 1000)
        self.periodic.start()

        handlers = [
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler, { 'jukebox': self.jukebox }),
            (r"/jukebox", JukeboxHandler, { 'jukebox': self.jukebox }),
        ]
        dirname = os.path.dirname(__file__)
        settings = {
            "template_path": os.path.join(dirname, 'templates'),
            "static_path": os.path.join(dirname, 'static'),
        }

        tornado.web.Application.__init__(self, handlers, **settings)

        mp("Running on port 8888");

    def sync(self):
        """Let the jukebox sync (to MPD) on server start."""
        self.jukebox.sync()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def mp(message, level=0):
    """Custom print method."""
    red = "\033[01;31m{0}\033[00m"
    green = "\033[01;36m{0}\033[00m"
    cyan = "\033[01;36m{0}\033[00m"
   
    codes = [green.format('OK'), red.format('Error'), cyan.format('Warning')]

    if True: # Only print out if debugging
        message = '[{}] {}'.format(codes[level], message)
        print(message)

def main():
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

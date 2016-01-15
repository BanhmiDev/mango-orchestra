import os
import json
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

class Application(tornado.web.Application):
    def __init__(self):
        self.jukebox = Jukebox()

        self.periodic = tornado.ioloop.PeriodicCallback(self.sync, 1000)
        self.periodic.start()

        handlers = [
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler, { 'jukebox': self.jukebox }), 
        ]
        dirname = os.path.dirname(__file__)
        settings = {
            "template_path": os.path.join(dirname, 'templates'),
            "static_path": os.path.join(dirname, 'static'),
        }

        tornado.web.Application.__init__(self, handlers, **settings)

        mp("Running on port 8888");

    def sync(self):
        self.jukebox.sync()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    
    def initialize(self, jukebox):
        self.jukebox = jukebox

    def open(self):
        self.jukebox.join()
        self.sync() # Sync immediately
        self.periodic = tornado.ioloop.PeriodicCallback(self.sync, 1000) # Schedule client syncing
        self.periodic.start()

    def on_message(self, message):
        mp("on_message", message);
    
    def on_close(self):
        self.jukebox.leave()
        self.periodic.stop()

    def sync(self):
        """Sync music."""
        result = {
            "time": self.jukebox.time,
            "listeners": self.jukebox.listeners
        }
        self.write_message(result)

class Jukebox():
    
    def __init__(self):
        self.time = 0
        self.listeners = 0

    def join(self):
        self.listeners += 1

    def leave(self):
        self.listeners -= 1

    def sync(self):
        self.time += 1

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

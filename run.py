import os
import json
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

class Application(tornado.web.Application):
    def __init__(self):
        self.jukebox = Jukebox()

        handlers = [
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler, {"jukebox": self.jukebox }),
            (r"/sync", SyncHandler, {"jukebox": self.jukebox }),
            (r"/jukebox", JukeboxHandler, {"jukebox": self.jukebox })
        ]
        dirname = os.path.dirname(__file__)
        settings = {
            "template_path": os.path.join(dirname, 'templates'),
            "static_path": os.path.join(dirname, 'static'),
        }

        tornado.web.Application.__init__(self, handlers, **settings)

        mp("Running on port 8888");

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print(os.path.getctime('static/test.mp3'))
        self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    
    def initialize(self, jukebox):
        self.jukebox = jukebox

    def open(self):
        self.jukebox.join()
    
    def on_message(self, message):
        mp("on_message", message);
    
    def on_close(self):
        self.jukebox.leave()

class SyncHandler(tornado.web.RequestHandler):
    
    def initialize(self, jukebox):
        self.jukebox = jukebox

    def get(self):
        if self.jukebox.isMaster():
            self.write("master")
        else:
            self.write(self.jukebox.time)
    
    def post(self):
        #todo: authentication for master
        master_time = self.get_argument("time", default=None, strip=False)
        self.jukebox.set_time(master_time)
        self.write("OK")

class JukeboxHandler(tornado.web.RequestHandler):
   
    def initialize(self, jukebox):
        self.jukebox = jukebox

    def get(self):
        """Returns basic jukebox information."""
        result = {
            'listeners': self.jukebox.listeners,
            'time': self.jukebox.time
        }
        
        self.finish(json.dumps(result))

class Jukebox():

    def __init__(self):
        self.listeners = 0
        self.time = 0

    def set_time(self, time):
        self.time = time

    def isMaster(self):
        return self.listeners == 1

    def join(self):
        mp("User joined")
        self.listeners += 1

    def leave(self):
        mp("User left")
        self.listeners -= 1

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

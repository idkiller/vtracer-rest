import os
from random import randint
import redis
import gevent
from flask_restx import Namespace, reqparse, Resource
from flask_sock import Sock


REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
REDIS_CHAN = "screen"
redis = redis.from_url(REDIS_URL)

screen = Namespace('screen', description="Screen APIs")
parser = reqparse.RequestParser()
parser.add_argument('data')

@screen.route('/')
@screen.route('/<string:screen_id>')
@screen.expect(parser)
class Screen(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api=api, *args, **kwargs)
    
    def post(self, screen_id):
        args = parser.parse_args()
        data = args['data']
        redis.set(screen_id, data)
        redis.publish(REDIS_CHAN, str(screen_id))
        return {'result': screen_id}

class ScreenBackend(object):
    def __init__(self):
        self.screens = {}
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)

    def __iter_data(self):
        for msg in self.pubsub.listen():
            screen_id = msg.get("data")
            if msg["type"] == "message":
                yield screen_id

    def register(self, screen, screen_id):
        print("Registering screen:", screen_id)
        self.screens[screen_id] = screen

    def send(self, screen, screen_id):
        try:
            data = redis.get(screen_id)
            screen.send(data.decode("utf-8"))
            print("Sent data to screen:", screen_id)
        except Exception:
            del self.screens[screen]

    def run(self):
        for key in self.__iter_data():
            screen_id = key.decode("ascii")
            if screen_id in self.screens:
                screen = self.screens[screen_id]
                gevent.spawn(self.send, screen, screen_id)

    def start(self):
        gevent.spawn(self.run)

def screen_screen_register_event(ws):
    while not ws.closed:
        screen_id = ws.receive()
        if not screen_id or not screen_id.strip():
            screen_id = str(randint(1000, 9999))


sockets = Sock()
backend = ScreenBackend()
@sockets.route('/register')
def screen_register_event(ws):
    screen_id = ws.receive()
    if not screen_id or not screen_id.strip():
        screen_id = str(randint(1000, 9999))
    backend.register(ws, screen_id)

def initialize(application):
    sockets.init_app(application)
    backend.start()

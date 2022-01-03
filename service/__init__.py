from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from .base import screen, contents, vision, screen_init

application = Flask(__name__)
CORS(application)

api = Api(application)
api.add_namespace(screen)
api.add_namespace(contents)
api.add_namespace(vision)

screen_init(application)
# source/web/server/__init__.py

import os

from flask import Flask
from flask_cors import CORS

from redis import Redis

from source.web.config import set_flask_config

app = Flask(__name__)
set_flask_config(app)


CORS(app)

redis = Redis.from_url(os.getenv("REDIS_URL", "redis://redis/0"), decode_responses=True)

import source.web.auth
import source.web.monitors

print("WEB IMPORTED")
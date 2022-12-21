from unittest.mock import Mock
from unittest.mock import patch

from .main import app


mock_redis_client = Mock()
mock_redis_client.store = {}

def set(_obj, key, val):
    mock_redis_client.store[key] = val

def get(_obj, key):
    return mock_redis_client.store.get(key, None)

mock_redis_client.set = set
mock_redis_client.get = get


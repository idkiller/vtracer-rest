import os

MONGODB_URL = os.environ.get('MONGODB_URL', 'mongodb://localhost:27017')
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
REDIS_CHAN = "screen"
JWT_KEY = "lightwarp-lightwarp-lightwarp"
JWT_ALGORITHM = "HS256"
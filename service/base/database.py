import os
from pymongo import MongoClient
from ..config import MONGODB_URL

mongo = MongoClient(MONGODB_URL)
db = mongo['lightwarp-contents']
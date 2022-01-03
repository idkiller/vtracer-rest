import os
from typing_extensions import Required
from flask_restx import Namespace, Resource, reqparse
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

MONGODB_URL = os.environ.get('MONGODB_URL', 'mongodb://localhost:27017')
mongo = MongoClient(MONGODB_URL)
db = mongo['lightwarp-contents']

contents = Namespace("contents", description="Content related APIs")

parser = reqparse.RequestParser()
parser.add_argument('type', Required=True)
parser.add_argument('name', Required=True)
parser.add_argument('thumbnail')
parser.add_argument('contents', Required=True)

@contents.route("/")
class Contents(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api=api, *args, **kwargs)   

    def get(self):
        contents = db.contents
        return [{k:v if k != '_id' else str(v) for k,v in x.items()} for x in contents.find()]
    
    @contents.expect(parser)
    def post(self):
        args = parser.parse_args()
        content = {**args}
        if content['type'] == 'physics-world-object':
            content['contents'] = json.loads(content['contents'])
        result = db.contents.insert_one(content)
        return str(result.inserted_id) if result.acknowledged else 'Failed'

@contents.route("/<string:content_id>")
class Content(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api=api, *args, **kwargs)
    
    def get(self, content_id):
        return db.contents.find_one({'_id': ObjectId(content_id)})
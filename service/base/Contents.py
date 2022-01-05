from flask_restx import Namespace, Resource, reqparse
from bson.objectid import ObjectId
import json
from .database import db

contents = Namespace("contents", description="Content related APIs")

parser = reqparse.RequestParser()
parser.add_argument('type', required=True)
parser.add_argument('name', required=True)
parser.add_argument('thumbnail')
parser.add_argument('contents', required=True)

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

@contents.route('/delete/<string:content_id>')
class ContentDelete(Resource):
    def get(self, content_id):
        result = db.contents.delete_one({'_id': ObjectId(content_id)})
        return "OK" if result.deleted_count > 0 else "FAIL"

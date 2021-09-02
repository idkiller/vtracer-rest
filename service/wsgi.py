from flask import Flask, request, Response
from flask_restx import Api, Resource, namespace, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from vlib import convert_to_svg_file

application = Flask(__name__)
app = Api(app = application)

VisionParser = app.parser()
VisionParser.add_argument('file', location='files', type=FileStorage, required=True)

vision = app.namespace('vision', description='vision APIs')

@vision.route('/')
@vision.expect(VisionParser)
class VisionClass(Resource):
    
    def __init__(self, api, *args, **kwargs):
        super().__init__(api=api, *args, **kwargs)
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        args = VisionParser.parse_args()
        #img = request.files['file']
        img = args['file']
        filename = secure_filename(img.filename)
        img.save(filename)
        #convert_to_svg_file(filename, filename + '.svg', "color", "stacked", "polygon", 4, 6, 16, 60, 4.0, 45, 8)
        #svg = convert_to_svg(filename, "color", "stacked", "polygon", 4, 6, 16, 60, 4.0, 45, 8)
        #return Response(svg, mimetype='image/svg+xml')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8090, debug=False)

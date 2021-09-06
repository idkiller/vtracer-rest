from flask import Flask, request, Response
from flask_restx import Api, Resource, namespace, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from vlib import convert_to_svg
from tempfile import mkstemp
import os

from flask_cors import CORS


application = Flask(__name__)
CORS(application)

@application.after_request
def set_headers(response):
    response.headers["Referrer-Policy"] = 'no-referrer'
    return response

app = Api(app = application)


VisionParser = app.parser()
VisionParser.add_argument('color_mode', default='color')
VisionParser.add_argument('hierarchial', default='stacked')
VisionParser.add_argument('mode', default='polygon')
VisionParser.add_argument('filter_speckle', default=4, type=int)
VisionParser.add_argument('color_precision', default=6, type=int)
VisionParser.add_argument('layer_difference', default=16, type=int)
VisionParser.add_argument('corner_threshold', default=60, type=int)
VisionParser.add_argument('length_threshold', default=4.0, type=float)
VisionParser.add_argument('splice_threshold', default=45, type=int)
VisionParser.add_argument('path_precision', default=8, type=int)
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
        img = args['file']
        fd, path = mkstemp()
        img.save(path)
        os.close(fd)
        #svg = convert_to_svg(path, "color", "stacked", "polygon", 4, 6, 16, 60, 4.0, 45, 8)
        svg = convert_to_svg(path,
            args['color_mode'],
            args['hierarchial'],
            args['mode'],
            args['filter_speckle'],
            args['color_precision'],
            args['layer_difference'],
            args['corner_threshold'],
            args['length_threshold'],
            args['splice_threshold'],
            args['path_precision']
        )
        os.unlink(path)
        return Response(svg, mimetype='image/svg+xml')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8090, debug=False)

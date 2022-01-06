import os
from tempfile import mkstemp
from flask import Response, send_file
from flask_restx import Namespace, reqparse, Resource
from werkzeug.datastructures import FileStorage
from pyvtracer import Vtracer

vision = Namespace('vision', description='VTracer APIs')

parser = reqparse.RequestParser()
parser.add_argument('color_mode', default='color')
parser.add_argument('hierarchical', default='stacked')
parser.add_argument('mode', default='polygon')
parser.add_argument('filter_speckle', default=4, type=int)
parser.add_argument('color_precision', default=6, type=int)
parser.add_argument('layer_difference', default=16, type=int)
parser.add_argument('corner_threshold', default=60, type=int)
parser.add_argument('length_threshold', default=4.0, type=float)
parser.add_argument('splice_threshold', default=45, type=int)
parser.add_argument('path_precision', default=8, type=int)
parser.add_argument('file', location='files', type=FileStorage, required=True)

@vision.expect(parser)
@vision.route("/")
class Vision(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api=api, *args, **kwargs)
        self.vtracer = Vtracer()
    
    def post(self):
        args = parser.parse_args()
        img = args["file"]
        maintype, subtype = img.content_type.split("/")
        if not maintype == "image":
            return Response(status=400)
        fd, in_path = mkstemp(suffix=f".{subtype}")
        img.save(in_path)
        os.close(fd)

        v = self.vtracer
        v.color_mode = args["color_mode"]
        v.hierarchical = args["hierarchical"]
        v.path_simplify_mode = args["mode"]
        v.filter_speckle = args["filter_speckle"]
        v.color_precision = args["color_precision"]
        v.layer_difference = args["layer_difference"]
        v.corner_threshold = args["corner_threshold"]
        v.length_threshold = args["length_threshold"]
        v.splice_threshold = args["splice_threshold"]
        v.path_precision = args["path_precision"]

        v.input_path = in_path
        v.output_path = in_path + ".svg"
        v.to_svg()

        return send_file(v.output_path, mimetype="image/svg+xml")

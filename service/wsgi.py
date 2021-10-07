from flask import Flask, request, Response, render_template
from flask_restx import Api, Resource, namespace, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from vlib import convert_to_svg
from tempfile import mkstemp
import os

from flask_cors import CORS, cross_origin

from pymongo import MongoClient

def DB(name):
    DB.client = DB.client or MongoClient(os.environ.get('MONGODB_URI', 'localhost'))
    return DB.client[name]


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

ContentsSaveFilter = app.parser()
ContentsSaveFilter.add_argument('contents', trim=True)
contents = app.namespace('contents', description='Contents APIs')

@contents.route('/')
class ContentsClass(Resource):
    def get(self):
        return [
            {
                'type': 'svg-pattern',
                'name': 'pattern1',
                'contents': '''<pattern x="12.5" y="12.5" width="25" height="25" patternUnits="userSpaceOnUse" viewBox="0 0 100 100">
                    <circle fill="orange" cx="10" cy="10" r="10" />
                </pattern>'''
            },
            {
                'type': 'svg-pattern',
                'name': 'pattern2',
                'contents': '''<pattern x="0" y="0" width="112" height="190" patternUnits="userSpaceOnUse" viewBox="56 -254 112 190">
                    <g fill="#fff" stroke="orange" stroke-width="20">
                        <path d="M168-127.1c0.5,0,1,0.1,1.3,0.3l53.4,30.5c0.7,0.4,1.3,1.4,1.3,2.2v61c0,0.8-0.6,1.8-1.3,2.2L169.3-0.3 c-0.7,0.4-1.9,0.4-2.6,0l-53.4-30.5c-0.7-0.4-1.3-1.4-1.3-2.2v-61c0-0.8,0.6-1.8,1.3-2.2l53.4-30.5C167-127,167.5-127.1,168-127.1 L168-127.1z"></path>
                        <path d="M112-222.5c0.5,0,1,0.1,1.3,0.3l53.4,30.5c0.7,0.4,1.3,1.4,1.3,2.2v61c0,0.8-0.6,1.8-1.3,2.2l-53.4,30.5 c-0.7,0.4-1.9,0.4-2.6,0l-53.4-30.5c-0.7-0.4-1.3-1.4-1.3-2.2v-61c0-0.8,0.6-1.8,1.3-2.2l53.4-30.5 C111-222.4,111.5-222.5,112-222.5L112-222.5z"></path>
                        <path d="M168-317.8c0.5,0,1,0.1,1.3,0.3l53.4,30.5c0.7,0.4,1.3,1.4,1.3,2.2v61c0,0.8-0.6,1.8-1.3,2.2L169.3-191 c-0.7,0.4-1.9,0.4-2.6,0l-53.4-30.5c-0.7-0.4-1.3-1.4-1.3-2.2v-61c0-0.8,0.6-1.8,1.3-2.2l53.4-30.5 C167-317.7,167.5-317.8,168-317.8L168-317.8z"></path>
                    </g>
                </pattern>'''
            },
            {
                'type': 'svg-pattern',
                'name': 'pattern3',
                'contents': '''<pattern x="0" y="126" patternUnits="userSpaceOnUse" width="126" height="200" viewBox="0 0 100 160">
                    <g id="cube">
                        <path fill="orange" d="M0 0l5 3v5l-5 -3z" />
                        <path fill="lighten(orange, 30%)" d="M10 0l-5 3v5l5 -3" />
                    </g>
                    <use x="5" y="8" xlink:href="#cube" />
                    <use x="-5" y="8" xlink:href="#cube" />
                </pattern>'''
            }
        ]

from flask_sockets import Sockets

sockets = Sockets(application)

@sockets.route('/screen')
def screen_connected_event(ws):
    print('screen......')
    while not ws.closed:
        message = ws.receive()
        print('connected : ' + str(message))
        ws.send(message)

if __name__ == '__main__':
    #application.run(host='0.0.0.0', port=8090, debug=True)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 8090), application, handler_class=WebSocketHandler)
    server.serve_forever()
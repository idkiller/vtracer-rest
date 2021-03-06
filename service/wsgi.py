from flask import Flask, request, Response, render_template
from flask_restx import Api, Resource, namespace, reqparse
import gevent
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from vlib import convert_to_svg
from tempfile import mkstemp
import os
import json

from flask_cors import CORS, cross_origin


application = Flask(__name__, template_folder='templates')
CORS(application)

@application.after_request
def set_headers(response):
    response.headers["Referrer-Policy"] = 'no-referrer'
    return response


@application.route('/')
def screen_get():
    return render_template('index.html')

app = Api(app = application, doc='/api')

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

contentsAPI = app.namespace('contents', description='Contents APIs')

@contentsAPI.route('/')
class ContentsClass(Resource):
    def get(self):
        return [
            {
                'type': 'physics-world-object',
                'name': 'physics1',
                'thumbnail': 'https://club-dosomething.github.io/temp/snowicon.png',
                'contents': {
                    'x': {'min': 0, 'max': 1},
                    'y': 0.02,
                    'type': 'polygon',
                    'options': {
                        'sides': 5,
                        'radius': {'min': 3, 'max': 7},
                        'frictionAir': 0.1,
                        'friction': 0.5,
                        'restitution': 0.6
                    },
                    'animation': {
                        'time': {'min': 100, 'max': 150},
                        'bindings': [
                            { 'name': 'dead', 'delay': 25000 },
                            { 'name': 'render.opacity', 'duration': 25000, 'value': { 'from': 1, 'to': 0 }, 'easing': 'linear' }
                        ]
                    }
                }
            },
            {
                'type': 'svg-pattern',
                'name': 'pattern4',
                'contents': '''<pattern x="0" y="0" width="163.84" height="163.84" patternUnits="userSpaceOnUse">
                    <g transform="scale(0.64)"><g>
                <line x1="129.53577788037228" x2="100.23582876150998" y1="27.750038493255815" y2="57.04998761211813" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="129.53577788037228" x2="100.23582876150998" y1="-484.24996150674417" y2="-454.9500123878819" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="385.5357778803723" x2="356.23582876151" y1="-484.24996150674417" y2="-454.9500123878819" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="641.5357778803723" x2="612.23582876151" y1="-484.24996150674417" y2="-454.9500123878819" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="129.53577788037228" x2="100.23582876150998" y1="-228.24996150674417" y2="-198.95001238788188" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="385.5357778803723" x2="356.23582876151" y1="-228.24996150674417" y2="-198.95001238788188" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="641.5357778803723" x2="612.23582876151" y1="-228.24996150674417" y2="-198.95001238788188" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="129.53577788037228" x2="100.23582876150998" y1="27.750038493255815" y2="57.04998761211813" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="385.5357778803723" x2="356.23582876151" y1="27.750038493255815" y2="57.04998761211813" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="641.5357778803723" x2="612.23582876151" y1="27.750038493255815" y2="57.04998761211813" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="189.57388435749118" x2="168.5607115524072" y1="136.85702239976314" y2="157.8701952048471" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="189.57388435749118" x2="168.5607115524072" y1="-375.14297760023686" y2="-354.1298047951529" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="445.5738843574912" x2="424.5607115524072" y1="-375.14297760023686" y2="-354.1298047951529" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="701.5738843574911" x2="680.5607115524072" y1="-375.14297760023686" y2="-354.1298047951529" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="189.57388435749118" x2="168.5607115524072" y1="-119.14297760023686" y2="-98.12980479515289" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="445.5738843574912" x2="424.5607115524072" y1="-119.14297760023686" y2="-98.12980479515289" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="701.5738843574911" x2="680.5607115524072" y1="-119.14297760023686" y2="-98.12980479515289" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="189.57388435749118" x2="168.5607115524072" y1="136.85702239976314" y2="157.8701952048471" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="445.5738843574912" x2="424.5607115524072" y1="136.85702239976314" y2="157.8701952048471" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="701.5738843574911" x2="680.5607115524072" y1="136.85702239976314" y2="157.8701952048471" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="15.087136916989031" x2="5.529096679797484" y1="86.15000515698729" y2="95.70804539417882" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="15.087136916989031" x2="5.529096679797484" y1="-425.8499948430127" y2="-416.29195460582116" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="271.08713691698904" x2="261.5290966797975" y1="-425.8499948430127" y2="-416.29195460582116" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="527.087136916989" x2="517.5290966797975" y1="-425.8499948430127" y2="-416.29195460582116" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="15.087136916989031" x2="5.529096679797484" y1="-169.84999484301272" y2="-160.29195460582116" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="271.08713691698904" x2="261.5290966797975" y1="-169.84999484301272" y2="-160.29195460582116" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="527.087136916989" x2="517.5290966797975" y1="-169.84999484301272" y2="-160.29195460582116" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="15.087136916989031" x2="5.529096679797484" y1="86.15000515698729" y2="95.70804539417882" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="271.08713691698904" x2="261.5290966797975" y1="86.15000515698729" y2="95.70804539417882" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="527.087136916989" x2="517.5290966797975" y1="86.15000515698729" y2="95.70804539417882" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="73.9315541628576" x2="59.72505122403476" y1="-6.795021704110639" y2="7.411481234712199" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="73.9315541628576" x2="59.72505122403476" y1="-518.7950217041107" y2="-504.5885187652878" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="329.9315541628576" x2="315.72505122403476" y1="-518.7950217041107" y2="-504.5885187652878" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="585.9315541628575" x2="571.7250512240348" y1="-518.7950217041107" y2="-504.5885187652878" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="73.9315541628576" x2="59.72505122403476" y1="-262.79502170411064" y2="-248.5885187652878" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="329.9315541628576" x2="315.72505122403476" y1="-262.79502170411064" y2="-248.5885187652878" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="585.9315541628575" x2="571.7250512240348" y1="-262.79502170411064" y2="-248.5885187652878" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="73.9315541628576" x2="59.72505122403476" y1="-6.795021704110639" y2="7.411481234712199" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="329.9315541628576" x2="315.72505122403476" y1="-6.795021704110639" y2="7.411481234712199" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="585.9315541628575" x2="571.7250512240348" y1="-6.795021704110639" y2="7.411481234712199" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="73.9315541628576" x2="59.72505122403476" y1="249.20497829588936" y2="263.4114812347122" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="71.10413428849967" x2="51.60818240967051" y1="183.42238741470686" y2="202.918339293536" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="71.10413428849967" x2="51.60818240967051" y1="-328.57761258529314" y2="-309.081660706464" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="327.10413428849967" x2="307.6081824096705" y1="-328.57761258529314" y2="-309.081660706464" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="583.1041342884996" x2="563.6081824096705" y1="-328.57761258529314" y2="-309.081660706464" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="71.10413428849967" x2="51.60818240967051" y1="-72.57761258529314" y2="-53.08166070646399" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="327.10413428849967" x2="307.6081824096705" y1="-72.57761258529314" y2="-53.08166070646399" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="583.1041342884996" x2="563.6081824096705" y1="-72.57761258529314" y2="-53.08166070646399" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="71.10413428849967" x2="51.60818240967051" y1="183.42238741470686" y2="202.918339293536" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="327.10413428849967" x2="307.6081824096705" y1="183.42238741470686" y2="202.918339293536" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="583.1041342884996" x2="563.6081824096705" y1="183.42238741470686" y2="202.918339293536" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="222.14001000812723" x2="214.74927679524885" y1="184.93629797205412" y2="192.3270311849325" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="222.14001000812723" x2="214.74927679524885" y1="-327.06370202794585" y2="-319.6729688150675" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="478.1400100081272" x2="470.7492767952489" y1="-327.06370202794585" y2="-319.6729688150675" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="734.1400100081272" x2="726.7492767952489" y1="-327.06370202794585" y2="-319.6729688150675" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="222.14001000812723" x2="214.74927679524885" y1="-71.06370202794588" y2="-63.67296881506749" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="478.1400100081272" x2="470.7492767952489" y1="-71.06370202794588" y2="-63.67296881506749" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="734.1400100081272" x2="726.7492767952489" y1="-71.06370202794588" y2="-63.67296881506749" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="222.14001000812723" x2="214.74927679524885" y1="184.93629797205412" y2="192.3270311849325" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="478.1400100081272" x2="470.7492767952489" y1="184.93629797205412" y2="192.3270311849325" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="734.1400100081272" x2="726.7492767952489" y1="184.93629797205412" y2="192.3270311849325" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="94.5053997162397" x2="70.75040158737649" y1="189.34891488808958" y2="213.10391301695276" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="94.5053997162397" x2="70.75040158737649" y1="-322.65108511191045" y2="-298.8960869830472" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="350.5053997162397" x2="326.7504015873765" y1="-322.65108511191045" y2="-298.8960869830472" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="606.5053997162397" x2="582.7504015873765" y1="-322.65108511191045" y2="-298.8960869830472" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="94.5053997162397" x2="70.75040158737649" y1="-66.65108511191042" y2="-42.89608698304724" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="350.5053997162397" x2="326.7504015873765" y1="-66.65108511191042" y2="-42.89608698304724" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="606.5053997162397" x2="582.7504015873765" y1="-66.65108511191042" y2="-42.89608698304724" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="94.5053997162397" x2="70.75040158737649" y1="189.34891488808958" y2="213.10391301695276" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="350.5053997162397" x2="326.7504015873765" y1="189.34891488808958" y2="213.10391301695276" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="606.5053997162397" x2="582.7504015873765" y1="189.34891488808958" y2="213.10391301695276" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="240.4630259345023" x2="231.56970917886736" y1="156.5330886699764" y2="165.42640542561134" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="240.4630259345023" x2="231.56970917886736" y1="-355.4669113300236" y2="-346.57359457438866" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="496.4630259345023" x2="487.56970917886736" y1="-355.4669113300236" y2="-346.57359457438866" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="752.4630259345023" x2="743.5697091788674" y1="-355.4669113300236" y2="-346.57359457438866" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="240.4630259345023" x2="231.56970917886736" y1="-99.4669113300236" y2="-90.57359457438866" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="496.4630259345023" x2="487.56970917886736" y1="-99.4669113300236" y2="-90.57359457438866" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="752.4630259345023" x2="743.5697091788674" y1="-99.4669113300236" y2="-90.57359457438866" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="240.4630259345023" x2="231.56970917886736" y1="156.5330886699764" y2="165.42640542561134" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="496.4630259345023" x2="487.56970917886736" y1="156.5330886699764" y2="165.42640542561134" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="752.4630259345023" x2="743.5697091788674" y1="156.5330886699764" y2="165.42640542561134" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="220.1927623766455" x2="192.70359604397962" y1="195.89268440654897" y2="223.38185073921485" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="220.1927623766455" x2="192.70359604397962" y1="-316.10731559345106" y2="-288.6181492607851" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="476.19276237664553" x2="448.7035960439796" y1="-316.10731559345106" y2="-288.6181492607851" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="732.1927623766455" x2="704.7035960439796" y1="-316.10731559345106" y2="-288.6181492607851" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="220.1927623766455" x2="192.70359604397962" y1="-60.107315593451034" y2="-32.618149260785145" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="476.19276237664553" x2="448.7035960439796" y1="-60.107315593451034" y2="-32.618149260785145" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="732.1927623766455" x2="704.7035960439796" y1="-60.107315593451034" y2="-32.618149260785145" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="220.1927623766455" x2="192.70359604397962" y1="195.89268440654897" y2="223.38185073921485" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="476.19276237664553" x2="448.7035960439796" y1="195.89268440654897" y2="223.38185073921485" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="732.1927623766455" x2="704.7035960439796" y1="195.89268440654897" y2="223.38185073921485" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="127.07574299547043" x2="119.39898435001696" y1="237.04499922326178" y2="244.7217578687153" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="127.07574299547043" x2="119.39898435001696" y1="-274.9550007767382" y2="-267.27824213128474" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="383.0757429954704" x2="375.398984350017" y1="-274.9550007767382" y2="-267.27824213128474" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="639.0757429954705" x2="631.3989843500169" y1="-274.9550007767382" y2="-267.27824213128474" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="127.07574299547043" x2="119.39898435001696" y1="-18.955000776738217" y2="-11.278242131284713" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="383.0757429954704" x2="375.398984350017" y1="-18.955000776738217" y2="-11.278242131284713" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="639.0757429954705" x2="631.3989843500169" y1="-18.955000776738217" y2="-11.278242131284713" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="127.07574299547043" x2="119.39898435001696" y1="237.04499922326178" y2="244.7217578687153" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="383.0757429954704" x2="375.398984350017" y1="237.04499922326178" y2="244.7217578687153" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="639.0757429954705" x2="631.3989843500169" y1="237.04499922326178" y2="244.7217578687153" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line>
                <animateTransform attributeName="transform" type="translate" values="0 0;-256 256" keyTimes="0;1" repeatCount="indefinite" dur="5s"></animateTransform>
                </g><g>
                <line x1="25.425115978359784" x2="15.986830094362558" y1="60.26768293195407" y2="69.7059688159513" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="25.425115978359784" x2="15.986830094362558" y1="-451.7323170680459" y2="-442.2940311840487" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="281.42511597835977" x2="271.9868300943626" y1="-451.7323170680459" y2="-442.2940311840487" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="537.4251159783598" x2="527.9868300943625" y1="-451.7323170680459" y2="-442.2940311840487" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="25.425115978359784" x2="15.986830094362558" y1="-195.73231706804592" y2="-186.29403118404872" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="281.42511597835977" x2="271.9868300943626" y1="-195.73231706804592" y2="-186.29403118404872" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="537.4251159783598" x2="527.9868300943625" y1="-195.73231706804592" y2="-186.29403118404872" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="25.425115978359784" x2="15.986830094362558" y1="60.26768293195407" y2="69.7059688159513" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="281.42511597835977" x2="271.9868300943626" y1="60.26768293195407" y2="69.7059688159513" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="537.4251159783598" x2="527.9868300943625" y1="60.26768293195407" y2="69.7059688159513" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="123.4472906485699" x2="95.20034332189839" y1="237.00547765498277" y2="265.25242498165426" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="123.4472906485699" x2="95.20034332189839" y1="-274.99452234501723" y2="-246.74757501834574" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="379.4472906485699" x2="351.2003433218984" y1="-274.99452234501723" y2="-246.74757501834574" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="635.44729064857" x2="607.2003433218983" y1="-274.99452234501723" y2="-246.74757501834574" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="123.4472906485699" x2="95.20034332189839" y1="-18.99452234501723" y2="9.252424981654258" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="379.4472906485699" x2="351.2003433218984" y1="-18.99452234501723" y2="9.252424981654258" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="635.44729064857" x2="607.2003433218983" y1="-18.99452234501723" y2="9.252424981654258" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="123.4472906485699" x2="95.20034332189839" y1="237.00547765498277" y2="265.25242498165426" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="379.4472906485699" x2="351.2003433218984" y1="237.00547765498277" y2="265.25242498165426" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="635.44729064857" x2="607.2003433218983" y1="237.00547765498277" y2="265.25242498165426" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="220.6907009408146" x2="201.66243846579678" y1="160.2145369114278" y2="179.24279938644563" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="220.6907009408146" x2="201.66243846579678" y1="-351.7854630885722" y2="-332.75720061355435" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="476.6907009408146" x2="457.66243846579675" y1="-351.7854630885722" y2="-332.75720061355435" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="732.6907009408146" x2="713.6624384657968" y1="-351.7854630885722" y2="-332.75720061355435" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="220.6907009408146" x2="201.66243846579678" y1="-95.78546308857219" y2="-76.75720061355437" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="476.6907009408146" x2="457.66243846579675" y1="-95.78546308857219" y2="-76.75720061355437" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="732.6907009408146" x2="713.6624384657968" y1="-95.78546308857219" y2="-76.75720061355437" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="220.6907009408146" x2="201.66243846579678" y1="160.2145369114278" y2="179.24279938644563" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="476.6907009408146" x2="457.66243846579675" y1="160.2145369114278" y2="179.24279938644563" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="732.6907009408146" x2="713.6624384657968" y1="160.2145369114278" y2="179.24279938644563" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="9.534710596525265" x2="0.6859996957885448" y1="134.61377942544203" y2="143.46249032617874" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="9.534710596525265" x2="0.6859996957885448" y1="-377.38622057455797" y2="-368.53750967382126" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="265.53471059652526" x2="256.68599969578855" y1="-377.38622057455797" y2="-368.53750967382126" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="521.5347105965253" x2="512.6859996957885" y1="-377.38622057455797" y2="-368.53750967382126" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="9.534710596525265" x2="0.6859996957885448" y1="-121.38622057455797" y2="-112.53750967382126" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="265.53471059652526" x2="256.68599969578855" y1="-121.38622057455797" y2="-112.53750967382126" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="521.5347105965253" x2="512.6859996957885" y1="-121.38622057455797" y2="-112.53750967382126" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="9.534710596525265" x2="0.6859996957885448" y1="134.61377942544203" y2="143.46249032617874" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="265.53471059652526" x2="256.68599969578855" y1="134.61377942544203" y2="143.46249032617874" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="521.5347105965253" x2="512.6859996957885" y1="134.61377942544203" y2="143.46249032617874" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="184.17842132061045" x2="161.22397493325528" y1="90.63570653563428" y2="113.59015292298946" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="184.17842132061045" x2="161.22397493325528" y1="-421.3642934643657" y2="-398.40984707701057" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="440.1784213206105" x2="417.22397493325525" y1="-421.3642934643657" y2="-398.40984707701057" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="696.1784213206105" x2="673.2239749332552" y1="-421.3642934643657" y2="-398.40984707701057" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="184.17842132061045" x2="161.22397493325528" y1="-165.36429346436572" y2="-142.40984707701054" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="440.1784213206105" x2="417.22397493325525" y1="-165.36429346436572" y2="-142.40984707701054" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="696.1784213206105" x2="673.2239749332552" y1="-165.36429346436572" y2="-142.40984707701054" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="184.17842132061045" x2="161.22397493325528" y1="90.63570653563428" y2="113.59015292298946" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="440.1784213206105" x2="417.22397493325525" y1="90.63570653563428" y2="113.59015292298946" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="696.1784213206105" x2="673.2239749332552" y1="90.63570653563428" y2="113.59015292298946" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="220.94345686376246" x2="203.98535397419036" y1="71.71683833461653" y2="88.67494122418866" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="220.94345686376246" x2="203.98535397419036" y1="-440.2831616653835" y2="-423.3250587758113" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="476.94345686376244" x2="459.9853539741904" y1="-440.2831616653835" y2="-423.3250587758113" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="732.9434568637624" x2="715.9853539741904" y1="-440.2831616653835" y2="-423.3250587758113" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="220.94345686376246" x2="203.98535397419036" y1="-184.2831616653835" y2="-167.32505877581133" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="476.94345686376244" x2="459.9853539741904" y1="-184.2831616653835" y2="-167.32505877581133" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="732.9434568637624" x2="715.9853539741904" y1="-184.2831616653835" y2="-167.32505877581133" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="220.94345686376246" x2="203.98535397419036" y1="71.71683833461653" y2="88.67494122418866" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="476.94345686376244" x2="459.9853539741904" y1="71.71683833461653" y2="88.67494122418866" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="732.9434568637624" x2="715.9853539741904" y1="71.71683833461653" y2="88.67494122418866" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="128.38859228476176" x2="119.01778654263187" y1="83.134946586341" y2="92.50575232847088" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="128.38859228476176" x2="119.01778654263187" y1="-428.865053413659" y2="-419.49424767152914" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="384.3885922847618" x2="375.0177865426319" y1="-428.865053413659" y2="-419.49424767152914" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="640.3885922847618" x2="631.0177865426318" y1="-428.865053413659" y2="-419.49424767152914" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="128.38859228476176" x2="119.01778654263187" y1="-172.86505341365898" y2="-163.49424767152914" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="384.3885922847618" x2="375.0177865426319" y1="-172.86505341365898" y2="-163.49424767152914" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="640.3885922847618" x2="631.0177865426318" y1="-172.86505341365898" y2="-163.49424767152914" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="128.38859228476176" x2="119.01778654263187" y1="83.134946586341" y2="92.50575232847088" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="384.3885922847618" x2="375.0177865426319" y1="83.134946586341" y2="92.50575232847088" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="640.3885922847618" x2="631.0177865426318" y1="83.134946586341" y2="92.50575232847088" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="256.8295146188623" x2="243.38383657335814" y1="193.6426840737736" y2="207.08836211927778" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="256.8295146188623" x2="243.38383657335814" y1="-318.3573159262264" y2="-304.9116378807222" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="512.8295146188623" x2="499.38383657335817" y1="-318.3573159262264" y2="-304.9116378807222" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="768.8295146188623" x2="755.3838365733582" y1="-318.3573159262264" y2="-304.9116378807222" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="256.8295146188623" x2="243.38383657335814" y1="-62.35731592622639" y2="-48.911637880722225" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="512.8295146188623" x2="499.38383657335817" y1="-62.35731592622639" y2="-48.911637880722225" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="768.8295146188623" x2="755.3838365733582" y1="-62.35731592622639" y2="-48.911637880722225" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="256.8295146188623" x2="243.38383657335814" y1="193.6426840737736" y2="207.08836211927778" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="512.8295146188623" x2="499.38383657335817" y1="193.6426840737736" y2="207.08836211927778" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="768.8295146188623" x2="755.3838365733582" y1="193.6426840737736" y2="207.08836211927778" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="0.8295146188622766" x2="-12.616163426641862" y1="193.6426840737736" y2="207.08836211927778" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="239.0194285794738" x2="212.4471597419414" y1="73.0904961271814" y2="99.66276496471379" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="239.0194285794738" x2="212.4471597419414" y1="-438.9095038728186" y2="-412.3372350352862" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="495.0194285794738" x2="468.4471597419414" y1="-438.9095038728186" y2="-412.3372350352862" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="751.0194285794738" x2="724.4471597419414" y1="-438.9095038728186" y2="-412.3372350352862" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="239.0194285794738" x2="212.4471597419414" y1="-182.90950387281862" y2="-156.3372350352862" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="495.0194285794738" x2="468.4471597419414" y1="-182.90950387281862" y2="-156.3372350352862" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="751.0194285794738" x2="724.4471597419414" y1="-182.90950387281862" y2="-156.3372350352862" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="239.0194285794738" x2="212.4471597419414" y1="73.0904961271814" y2="99.66276496471379" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="495.0194285794738" x2="468.4471597419414" y1="73.0904961271814" y2="99.66276496471379" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="751.0194285794738" x2="724.4471597419414" y1="73.0904961271814" y2="99.66276496471379" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="110.64033967319878" x2="93.78807323043569" y1="243.39594742634833" y2="260.2482138691114" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="110.64033967319878" x2="93.78807323043569" y1="-268.60405257365164" y2="-251.7517861308886" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="366.6403396731988" x2="349.78807323043566" y1="-268.60405257365164" y2="-251.7517861308886" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="622.6403396731988" x2="605.7880732304357" y1="-268.60405257365164" y2="-251.7517861308886" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="110.64033967319878" x2="93.78807323043569" y1="-12.604052573651671" y2="4.248213869111396" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="366.6403396731988" x2="349.78807323043566" y1="-12.604052573651671" y2="4.248213869111396" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="622.6403396731988" x2="605.7880732304357" y1="-12.604052573651671" y2="4.248213869111396" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="110.64033967319878" x2="93.78807323043569" y1="243.39594742634833" y2="260.2482138691114" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="366.6403396731988" x2="349.78807323043566" y1="243.39594742634833" y2="260.2482138691114" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line><line x1="622.6403396731988" x2="605.7880732304357" y1="243.39594742634833" y2="260.2482138691114" stroke-width="5" stroke="#38e0f5" stroke-linecap="round"></line>
                <animateTransform attributeName="transform" type="translate" values="0 0;-256 256" keyTimes="0;1" repeatCount="indefinite" dur="2.5s"></animateTransform>
                </g><g>
                <line x1="209.0274401023449" x2="193.66653100172417" y1="32.715777601321534" y2="48.07668670194231" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="209.0274401023449" x2="193.66653100172417" y1="-479.2842223986785" y2="-463.9233132980577" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="465.02744010234494" x2="449.66653100172414" y1="-479.2842223986785" y2="-463.9233132980577" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="721.0274401023449" x2="705.6665310017241" y1="-479.2842223986785" y2="-463.9233132980577" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="209.0274401023449" x2="193.66653100172417" y1="-223.28422239867848" y2="-207.92331329805768" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="465.02744010234494" x2="449.66653100172414" y1="-223.28422239867848" y2="-207.92331329805768" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="721.0274401023449" x2="705.6665310017241" y1="-223.28422239867848" y2="-207.92331329805768" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="209.0274401023449" x2="193.66653100172417" y1="32.715777601321534" y2="48.07668670194231" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="465.02744010234494" x2="449.66653100172414" y1="32.715777601321534" y2="48.07668670194231" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="721.0274401023449" x2="705.6665310017241" y1="32.715777601321534" y2="48.07668670194231" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="38.76854689154438" x2="27.752364077827657" y1="242.89882873988628" y2="253.91501155360302" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="38.76854689154438" x2="27.752364077827657" y1="-269.1011712601137" y2="-258.084988446397" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="294.76854689154436" x2="283.7523640778277" y1="-269.1011712601137" y2="-258.084988446397" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="550.7685468915444" x2="539.7523640778277" y1="-269.1011712601137" y2="-258.084988446397" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="38.76854689154438" x2="27.752364077827657" y1="-13.101171260113716" y2="-2.0849884463969772" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="294.76854689154436" x2="283.7523640778277" y1="-13.101171260113716" y2="-2.0849884463969772" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="550.7685468915444" x2="539.7523640778277" y1="-13.101171260113716" y2="-2.0849884463969772" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="38.76854689154438" x2="27.752364077827657" y1="242.89882873988628" y2="253.91501155360302" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="294.76854689154436" x2="283.7523640778277" y1="242.89882873988628" y2="253.91501155360302" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="550.7685468915444" x2="539.7523640778277" y1="242.89882873988628" y2="253.91501155360302" stroke-width="5" stroke="#01cbe1" stroke-linecap="round"></line><line x1="190.62636672454448" x2="173.51132608352475" y1="64.23409210294979" y2="81.34913274396949" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="190.62636672454448" x2="173.51132608352475" y1="-447.7659078970502" y2="-430.6508672560305" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="446.6263667245445" x2="429.51132608352475" y1="-447.7659078970502" y2="-430.6508672560305" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="702.6263667245445" x2="685.5113260835248" y1="-447.7659078970502" y2="-430.6508672560305" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="190.62636672454448" x2="173.51132608352475" y1="-191.76590789705023" y2="-174.6508672560305" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="446.6263667245445" x2="429.51132608352475" y1="-191.76590789705023" y2="-174.6508672560305" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="702.6263667245445" x2="685.5113260835248" y1="-191.76590789705023" y2="-174.6508672560305" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="190.62636672454448" x2="173.51132608352475" y1="64.23409210294979" y2="81.34913274396949" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="446.6263667245445" x2="429.51132608352475" y1="64.23409210294979" y2="81.34913274396949" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="702.6263667245445" x2="685.5113260835248" y1="64.23409210294979" y2="81.34913274396949" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="169.37753709670196" x2="161.14822044301948" y1="250.44132120977432" y2="258.67063786345676" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="169.37753709670196" x2="161.14822044301948" y1="-261.5586787902257" y2="-253.32936213654324" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="425.377537096702" x2="417.14822044301945" y1="-261.5586787902257" y2="-253.32936213654324" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="681.377537096702" x2="673.1482204430195" y1="-261.5586787902257" y2="-253.32936213654324" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="169.37753709670196" x2="161.14822044301948" y1="-5.5586787902256845" y2="2.6706378634567614" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="425.377537096702" x2="417.14822044301945" y1="-5.5586787902256845" y2="2.6706378634567614" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="681.377537096702" x2="673.1482204430195" y1="-5.5586787902256845" y2="2.6706378634567614" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="169.37753709670196" x2="161.14822044301948" y1="250.44132120977432" y2="258.67063786345676" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="425.377537096702" x2="417.14822044301945" y1="250.44132120977432" y2="258.67063786345676" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="681.377537096702" x2="673.1482204430195" y1="250.44132120977432" y2="258.67063786345676" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="237.65667694033831" x2="229.3237645088582" y1="11.517104158474769" y2="19.8500165899549" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="237.65667694033831" x2="229.3237645088582" y1="-500.48289584152525" y2="-492.1499834100451" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="493.65667694033834" x2="485.3237645088582" y1="-500.48289584152525" y2="-492.1499834100451" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="749.6566769403383" x2="741.3237645088582" y1="-500.48289584152525" y2="-492.1499834100451" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="237.65667694033831" x2="229.3237645088582" y1="-244.48289584152522" y2="-236.1499834100451" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="493.65667694033834" x2="485.3237645088582" y1="-244.48289584152522" y2="-236.1499834100451" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="749.6566769403383" x2="741.3237645088582" y1="-244.48289584152522" y2="-236.1499834100451" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="237.65667694033831" x2="229.3237645088582" y1="11.517104158474769" y2="19.8500165899549" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="493.65667694033834" x2="485.3237645088582" y1="11.517104158474769" y2="19.8500165899549" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="749.6566769403383" x2="741.3237645088582" y1="11.517104158474769" y2="19.8500165899549" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="204.94591226641327" x2="197.0024539498203" y1="57.01301187632051" y2="64.9564701929135" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="204.94591226641327" x2="197.0024539498203" y1="-454.9869881236795" y2="-447.0435298070865" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="460.9459122664133" x2="453.0024539498203" y1="-454.9869881236795" y2="-447.0435298070865" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="716.9459122664133" x2="709.0024539498203" y1="-454.9869881236795" y2="-447.0435298070865" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="204.94591226641327" x2="197.0024539498203" y1="-198.98698812367948" y2="-191.0435298070865" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="460.9459122664133" x2="453.0024539498203" y1="-198.98698812367948" y2="-191.0435298070865" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="716.9459122664133" x2="709.0024539498203" y1="-198.98698812367948" y2="-191.0435298070865" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="204.94591226641327" x2="197.0024539498203" y1="57.01301187632051" y2="64.9564701929135" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="460.9459122664133" x2="453.0024539498203" y1="57.01301187632051" y2="64.9564701929135" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="716.9459122664133" x2="709.0024539498203" y1="57.01301187632051" y2="64.9564701929135" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="226.63848468988905" x2="197.70743125120637" y1="222.06358093373322" y2="250.9946343724159" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="226.63848468988905" x2="197.70743125120637" y1="-289.9364190662668" y2="-261.00536562758407" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="482.6384846898891" x2="453.70743125120634" y1="-289.9364190662668" y2="-261.00536562758407" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="738.6384846898891" x2="709.7074312512063" y1="-289.9364190662668" y2="-261.00536562758407" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="226.63848468988905" x2="197.70743125120637" y1="-33.93641906626678" y2="-5.005365627584098" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="482.6384846898891" x2="453.70743125120634" y1="-33.93641906626678" y2="-5.005365627584098" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="738.6384846898891" x2="709.7074312512063" y1="-33.93641906626678" y2="-5.005365627584098" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="226.63848468988905" x2="197.70743125120637" y1="222.06358093373322" y2="250.9946343724159" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="482.6384846898891" x2="453.70743125120634" y1="222.06358093373322" y2="250.9946343724159" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="738.6384846898891" x2="709.7074312512063" y1="222.06358093373322" y2="250.9946343724159" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="208.40338972813623" x2="188.84937764015973" y1="209.00371274308253" y2="228.55772483105903" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="208.40338972813623" x2="188.84937764015973" y1="-302.99628725691747" y2="-283.44227516894097" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="464.40338972813623" x2="444.84937764015973" y1="-302.99628725691747" y2="-283.44227516894097" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="720.4033897281363" x2="700.8493776401597" y1="-302.99628725691747" y2="-283.44227516894097" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="208.40338972813623" x2="188.84937764015973" y1="-46.99628725691747" y2="-27.442275168940967" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="464.40338972813623" x2="444.84937764015973" y1="-46.99628725691747" y2="-27.442275168940967" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="720.4033897281363" x2="700.8493776401597" y1="-46.99628725691747" y2="-27.442275168940967" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="208.40338972813623" x2="188.84937764015973" y1="209.00371274308253" y2="228.55772483105903" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="464.40338972813623" x2="444.84937764015973" y1="209.00371274308253" y2="228.55772483105903" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="720.4033897281363" x2="700.8493776401597" y1="209.00371274308253" y2="228.55772483105903" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="241.6070257938171" x2="220.85479512968553" y1="231.064453514858" y2="251.81668417898956" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="241.6070257938171" x2="220.85479512968553" y1="-280.935546485142" y2="-260.1833158210104" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="497.6070257938171" x2="476.8547951296855" y1="-280.935546485142" y2="-260.1833158210104" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="753.6070257938171" x2="732.8547951296855" y1="-280.935546485142" y2="-260.1833158210104" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="241.6070257938171" x2="220.85479512968553" y1="-24.935546485141998" y2="-4.183315821010439" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="497.6070257938171" x2="476.8547951296855" y1="-24.935546485141998" y2="-4.183315821010439" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="753.6070257938171" x2="732.8547951296855" y1="-24.935546485141998" y2="-4.183315821010439" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="241.6070257938171" x2="220.85479512968553" y1="231.064453514858" y2="251.81668417898956" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="497.6070257938171" x2="476.8547951296855" y1="231.064453514858" y2="251.81668417898956" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="753.6070257938171" x2="732.8547951296855" y1="231.064453514858" y2="251.81668417898956" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="249.77677792859487" x2="222.96888530706275" y1="53.11172287258284" y2="79.91961549411498" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="249.77677792859487" x2="222.96888530706275" y1="-458.88827712741715" y2="-432.08038450588504" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="505.77677792859487" x2="478.96888530706275" y1="-458.88827712741715" y2="-432.08038450588504" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="761.7767779285948" x2="734.9688853070627" y1="-458.88827712741715" y2="-432.08038450588504" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="249.77677792859487" x2="222.96888530706275" y1="-202.88827712741715" y2="-176.08038450588504" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="505.77677792859487" x2="478.96888530706275" y1="-202.88827712741715" y2="-176.08038450588504" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="761.7767779285948" x2="734.9688853070627" y1="-202.88827712741715" y2="-176.08038450588504" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="249.77677792859487" x2="222.96888530706275" y1="53.11172287258284" y2="79.91961549411498" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="505.77677792859487" x2="478.96888530706275" y1="53.11172287258284" y2="79.91961549411498" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line><line x1="761.7767779285948" x2="734.9688853070627" y1="53.11172287258284" y2="79.91961549411498" stroke-width="5" stroke="#a9f0f9" stroke-linecap="round"></line>
                <animateTransform attributeName="transform" type="translate" values="0 0;-256 256" keyTimes="0;1" repeatCount="indefinite" dur="1.6666666666666665s"></animateTransform>
                </g></g>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'pattern5',
                'contents': '''<pattern x="0" y="0" width="128" height="128" patternUnits="userSpaceOnUse">
                    <g transform="scale(0.5)"><g style="font-family:courier new;font-size:25.6"><g transform="translate(0 25.6)"><text fill="#34ff00" style="animation-delay:-1.0314824142826864s">???</text></g><g transform="translate(0 51.2)"><text fill="#34ff00" style="animation-delay:-0.9314824142826864s">???</text></g><g transform="translate(0 76.80000000000001)"><text fill="#34ff00" style="animation-delay:-0.8314824142826864s">???</text></g><g transform="translate(0 102.4)"><text fill="#34ff00" style="animation-delay:-0.7314824142826863s">???</text></g><g transform="translate(0 128)"><text fill="#34ff00" style="animation-delay:-0.6314824142826864s">???</text></g><g transform="translate(0 153.60000000000002)"><text fill="#34ff00" style="animation-delay:-0.5314824142826864s">???</text></g><g transform="translate(0 179.20000000000002)"><text fill="#34ff00" style="animation-delay:-0.4314824142826864s">???</text></g><g transform="translate(0 204.8)"><text fill="#34ff00" style="animation-delay:-0.3314824142826864s">???</text></g><g transform="translate(0 230.4)"><text fill="#34ff00" style="animation-delay:-0.2314824142826864s">???</text></g><g transform="translate(0 256)"><text fill="#34ff00" style="animation-delay:-0.1314824142826864s">???</text></g><g transform="translate(25.6 25.6)"><text fill="#34ff00" style="animation-delay:-1.1286869924674967s">???</text></g><g transform="translate(25.6 51.2)"><text fill="#34ff00" style="animation-delay:-1.0286869924674966s">???</text></g><g transform="translate(25.6 76.80000000000001)"><text fill="#34ff00" style="animation-delay:-0.9286869924674968s">???</text></g><g transform="translate(25.6 102.4)"><text fill="#34ff00" style="animation-delay:-0.8286869924674967s">???</text></g><g transform="translate(25.6 128)"><text fill="#34ff00" style="animation-delay:-0.7286869924674967s">???</text></g><g transform="translate(25.6 153.60000000000002)"><text fill="#34ff00" style="animation-delay:-0.6286869924674967s">???</text></g><g transform="translate(25.6 179.20000000000002)"><text fill="#34ff00" style="animation-delay:-0.5286869924674967s">???</text></g><g transform="translate(25.6 204.8)"><text fill="#34ff00" style="animation-delay:-0.4286869924674967s">???</text></g><g transform="translate(25.6 230.4)"><text fill="#34ff00" style="animation-delay:-0.3286869924674967s">???</text></g><g transform="translate(25.6 256)"><text fill="#34ff00" style="animation-delay:-0.2286869924674967s">???</text></g><g transform="translate(51.2 25.6)"><text fill="#34ff00" style="animation-delay:-1.0498625739923724s">???</text></g><g transform="translate(51.2 51.2)"><text fill="#34ff00" style="animation-delay:-0.9498625739923724s">???</text></g><g transform="translate(51.2 76.80000000000001)"><text fill="#34ff00" style="animation-delay:-0.8498625739923724s">???</text></g><g transform="translate(51.2 102.4)"><text fill="#34ff00" style="animation-delay:-0.7498625739923723s">???</text></g><g transform="translate(51.2 128)"><text fill="#34ff00" style="animation-delay:-0.6498625739923723s">???</text></g><g transform="translate(51.2 153.60000000000002)"><text fill="#34ff00" style="animation-delay:-0.5498625739923724s">???</text></g><g transform="translate(51.2 179.20000000000002)"><text fill="#34ff00" style="animation-delay:-0.4498625739923724s">???</text></g><g transform="translate(51.2 204.8)"><text fill="#34ff00" style="animation-delay:-0.34986257399237236s">???</text></g><g transform="translate(51.2 230.4)"><text fill="#34ff00" style="animation-delay:-0.24986257399237238s">???</text></g><g transform="translate(51.2 256)"><text fill="#34ff00" style="animation-delay:-0.14986257399237238s">???</text></g><g transform="translate(76.80000000000001 25.6)"><text fill="#34ff00" style="animation-delay:-1.3626229905627012s">???</text></g><g transform="translate(76.80000000000001 51.2)"><text fill="#34ff00" style="animation-delay:-1.262622990562701s">???</text></g><g transform="translate(76.80000000000001 76.80000000000001)"><text fill="#34ff00" style="animation-delay:-1.1626229905627012s">???</text></g><g transform="translate(76.80000000000001 102.4)"><text fill="#34ff00" style="animation-delay:-1.0626229905627012s">???</text></g><g transform="translate(76.80000000000001 128)"><text fill="#34ff00" style="animation-delay:-0.9626229905627012s">???</text></g><g transform="translate(76.80000000000001 153.60000000000002)"><text fill="#34ff00" style="animation-delay:-0.8626229905627012s">???</text></g><g transform="translate(76.80000000000001 179.20000000000002)"><text fill="#34ff00" style="animation-delay:-0.7626229905627012s">???</text></g><g transform="translate(76.80000000000001 204.8)"><text fill="#34ff00" style="animation-delay:-0.6626229905627012s">???</text></g><g transform="translate(76.80000000000001 230.4)"><text fill="#34ff00" style="animation-delay:-0.5626229905627012s">???</text></g><g transform="translate(76.80000000000001 256)"><text fill="#34ff00" style="animation-delay:-0.4626229905627012s">???</text></g><g transform="translate(102.4 25.6)"><text fill="#34ff00" style="animation-delay:-1.1109210725862784s">???</text></g><g transform="translate(102.4 51.2)"><text fill="#34ff00" style="animation-delay:-1.0109210725862785s">???</text></g><g transform="translate(102.4 76.80000000000001)"><text fill="#34ff00" style="animation-delay:-0.9109210725862784s">???</text></g><g transform="translate(102.4 102.4)"><text fill="#34ff00" style="animation-delay:-0.8109210725862783s">???</text></g><g transform="translate(102.4 128)"><text fill="#34ff00" style="animation-delay:-0.7109210725862783s">???</text></g><g transform="translate(102.4 153.60000000000002)"><text fill="#34ff00" style="animation-delay:-0.6109210725862784s">???</text></g><g transform="translate(102.4 179.20000000000002)"><text fill="#34ff00" style="animation-delay:-0.5109210725862784s">???</text></g><g transform="translate(102.4 204.8)"><text fill="#34ff00" style="animation-delay:-0.41092107258627836s">???</text></g><g transform="translate(102.4 230.4)"><text fill="#34ff00" style="animation-delay:-0.3109210725862784s">???</text></g><g transform="translate(102.4 256)"><text fill="#34ff00" style="animation-delay:-0.21092107258627837s">???</text></g><g transform="translate(128 25.6)"><text fill="#34ff00" style="animation-delay:-1.500113630541339s">???</text></g><g transform="translate(128 51.2)"><text fill="#34ff00" style="animation-delay:-1.4001136305413389s">???</text></g><g transform="translate(128 76.80000000000001)"><text fill="#34ff00" style="animation-delay:-1.300113630541339s">???</text></g><g transform="translate(128 102.4)"><text fill="#34ff00" style="animation-delay:-1.200113630541339s">???</text></g><g transform="translate(128 128)"><text fill="#34ff00" style="animation-delay:-1.100113630541339s">???</text></g><g transform="translate(128 153.60000000000002)"><text fill="#34ff00" style="animation-delay:-1.000113630541339s">???</text></g><g transform="translate(128 179.20000000000002)"><text fill="#34ff00" style="animation-delay:-0.900113630541339s">???</text></g><g transform="translate(128 204.8)"><text fill="#34ff00" style="animation-delay:-0.800113630541339s">???</text></g><g transform="translate(128 230.4)"><text fill="#34ff00" style="animation-delay:-0.7001136305413389s">???</text></g><g transform="translate(128 256)"><text fill="#34ff00" style="animation-delay:-0.6001136305413389s">???</text></g><g transform="translate(153.60000000000002 25.6)"><text fill="#34ff00" style="animation-delay:-1.1890601738765858s">???</text></g><g transform="translate(153.60000000000002 51.2)"><text fill="#34ff00" style="animation-delay:-1.089060173876586s">???</text></g><g transform="translate(153.60000000000002 76.80000000000001)"><text fill="#34ff00" style="animation-delay:-0.9890601738765858s">???</text></g><g transform="translate(153.60000000000002 102.4)"><text fill="#34ff00" style="animation-delay:-0.8890601738765858s">???</text></g><g transform="translate(153.60000000000002 128)"><text fill="#34ff00" style="animation-delay:-0.7890601738765858s">???</text></g><g transform="translate(153.60000000000002 153.60000000000002)"><text fill="#34ff00" style="animation-delay:-0.6890601738765858s">???</text></g><g transform="translate(153.60000000000002 179.20000000000002)"><text fill="#34ff00" style="animation-delay:-0.5890601738765858s">???</text></g><g transform="translate(153.60000000000002 204.8)"><text fill="#34ff00" style="animation-delay:-0.4890601738765858s">???</text></g><g transform="translate(153.60000000000002 230.4)"><text fill="#34ff00" style="animation-delay:-0.3890601738765858s">???</text></g><g transform="translate(153.60000000000002 256)"><text fill="#34ff00" style="animation-delay:-0.2890601738765858s">???</text></g><g transform="translate(179.20000000000002 25.6)"><text fill="#34ff00" style="animation-delay:-1.6043749735230437s">???</text></g><g transform="translate(179.20000000000002 51.2)"><text fill="#34ff00" style="animation-delay:-1.5043749735230438s">???</text></g><g transform="translate(179.20000000000002 76.80000000000001)"><text fill="#34ff00" style="animation-delay:-1.4043749735230437s">???</text></g><g transform="translate(179.20000000000002 102.4)"><text fill="#34ff00" style="animation-delay:-1.3043749735230437s">???</text></g><g transform="translate(179.20000000000002 128)"><text fill="#34ff00" style="animation-delay:-1.2043749735230436s">???</text></g><g transform="translate(179.20000000000002 153.60000000000002)"><text fill="#34ff00" style="animation-delay:-1.1043749735230437s">???</text></g><g transform="translate(179.20000000000002 179.20000000000002)"><text fill="#34ff00" style="animation-delay:-1.0043749735230438s">???</text></g><g transform="translate(179.20000000000002 204.8)"><text fill="#34ff00" style="animation-delay:-0.9043749735230437s">???</text></g><g transform="translate(179.20000000000002 230.4)"><text fill="#34ff00" style="animation-delay:-0.8043749735230437s">???</text></g><g transform="translate(179.20000000000002 256)"><text fill="#34ff00" style="animation-delay:-0.7043749735230437s">???</text></g><g transform="translate(204.8 25.6)"><text fill="#34ff00" style="animation-delay:-1.1842958537730555s">???</text></g><g transform="translate(204.8 51.2)"><text fill="#34ff00" style="animation-delay:-1.0842958537730554s">???</text></g><g transform="translate(204.8 76.80000000000001)"><text fill="#34ff00" style="animation-delay:-0.9842958537730555s">???</text></g><g transform="translate(204.8 102.4)"><text fill="#34ff00" style="animation-delay:-0.8842958537730554s">???</text></g><g transform="translate(204.8 128)"><text fill="#34ff00" style="animation-delay:-0.7842958537730554s">???</text></g><g transform="translate(204.8 153.60000000000002)"><text fill="#34ff00" style="animation-delay:-0.6842958537730555s">???</text></g><g transform="translate(204.8 179.20000000000002)"><text fill="#34ff00" style="animation-delay:-0.5842958537730555s">???</text></g><g transform="translate(204.8 204.8)"><text fill="#34ff00" style="animation-delay:-0.48429585377305545s">???</text></g><g transform="translate(204.8 230.4)"><text fill="#34ff00" style="animation-delay:-0.3842958537730555s">???</text></g><g transform="translate(204.8 256)"><text fill="#34ff00" style="animation-delay:-0.28429585377305544s">???</text></g><g transform="translate(230.4 25.6)"><text fill="#34ff00" style="animation-delay:-1.8747307249448155s">???</text></g><g transform="translate(230.4 51.2)"><text fill="#34ff00" style="animation-delay:-1.7747307249448157s">???</text></g><g transform="translate(230.4 76.80000000000001)"><text fill="#34ff00" style="animation-delay:-1.6747307249448156s">???</text></g><g transform="translate(230.4 102.4)"><text fill="#34ff00" style="animation-delay:-1.5747307249448155s">???</text></g><g transform="translate(230.4 128)"><text fill="#34ff00" style="animation-delay:-1.4747307249448154s">???</text></g><g transform="translate(230.4 153.60000000000002)"><text fill="#34ff00" style="animation-delay:-1.3747307249448155s">???</text></g><g transform="translate(230.4 179.20000000000002)"><text fill="#34ff00" style="animation-delay:-1.2747307249448157s">???</text></g><g transform="translate(230.4 204.8)"><text fill="#34ff00" style="animation-delay:-1.1747307249448156s">???</text></g><g transform="translate(230.4 230.4)"><text fill="#34ff00" style="animation-delay:-1.0747307249448155s">???</text></g><g transform="translate(230.4 256)"><text fill="#34ff00" style="animation-delay:-0.9747307249448155s">???</text></g><style type="text/css">
                @keyframes ldp-matrix {
                    0% { opacity: 1; fill: #c5ff10;}
                    10% { opacity: 1; fill: #34ff00; }
                    50% { opacity: 0}
                    100% { opacity: 0}
                }
                text {
                    animation: ldp-matrix 1s linear infinite;
                    transform: scaleX(-0.7);
                }
                </style></g></g>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'pattern6',
                'contents': '''<pattern x="0" y="0" width="76.80000000000001" height="76.80000000000001" patternUnits="userSpaceOnUse">
                    <g transform="scale(0.30000000000000004)"><defs><g id="stripe-0.7486950831029537">
                <path d="M256 -128 L384 -128 L-128 384 L-128 256 Z" fill="#ff4800"></path>
                <path d="M384 0 L384 128 L128 384 L0 384 Z" fill="#ff4800"></path>
                </g></defs>

                <g>
                <use xlink:href="#stripe-0.7486950831029537" x="-256" y="0"></use>
                <use xlink:href="#stripe-0.7486950831029537" x="0" y="0"></use>
                <animateTransform attributeName="transform" type="translate" keyTimes="0;1" repeatCount="indefinite" dur="0.5s" values="0 0; 256 0"></animateTransform>
                </g></g>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'pattern8',
                'contents': '''
                <pattern id="pid-0.40637369613407737" x="0" y="0" width="217.6" height="217.6" patternUnits="userSpaceOnUse">
                    <g transform="scale(0.85)"><defs>
                <filter id="pat-0.8962203095919483" x="-100%" y="-100%" width="300%" height="300%" color-interpolation-filters="sRGB">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="10"></feGaussianBlur>
                    <feComponentTransfer result="cutoff">
                    <feFuncA type="linear" slope="60" intercept="-40"></feFuncA>
                    </feComponentTransfer>
                </filter>
                </defs><g filter="url(#f)"><g style="isolation:isolate" filter="url(#pat-0.8962203095919483)">
                <rect x="0" y="0" width="256" height="256" fill="none"></rect><g>
                <circle cx="-51.645194860071626" cy="232.92812369480106" r="22.109367520509846" fill="undefined"></circle> <circle cx="204.35480513992837" cy="232.92812369480106" r="22.109367520509846" fill="undefined"></circle> <circle cx="460.3548051399284" cy="232.92812369480106" r="22.109367520509846" fill="undefined"></circle> <circle cx="-51.645194860071626" cy="488.92812369480106" r="22.109367520509846" fill="undefined"></circle> <circle cx="204.35480513992837" cy="488.92812369480106" r="22.109367520509846" fill="undefined"></circle> <circle cx="460.3548051399284" cy="488.92812369480106" r="22.109367520509846" fill="undefined"></circle> <circle cx="-51.645194860071626" cy="744.9281236948011" r="22.109367520509846" fill="undefined"></circle> <circle cx="204.35480513992837" cy="744.9281236948011" r="22.109367520509846" fill="undefined"></circle> <circle cx="460.3548051399284" cy="744.9281236948011" r="22.109367520509846" fill="undefined"></circle> <circle cx="-168.82514171766587" cy="-23.963958943501893" r="32.16005687656317" fill="undefined"></circle> <circle cx="87.17485828233413" cy="-23.963958943501893" r="32.16005687656317" fill="undefined"></circle> <circle cx="343.1748582823341" cy="-23.963958943501893" r="32.16005687656317" fill="undefined"></circle> <circle cx="-168.82514171766587" cy="232.0360410564981" r="32.16005687656317" fill="undefined"></circle> <circle cx="87.17485828233413" cy="232.0360410564981" r="32.16005687656317" fill="undefined"></circle> <circle cx="343.1748582823341" cy="232.0360410564981" r="32.16005687656317" fill="undefined"></circle> <circle cx="-168.82514171766587" cy="488.0360410564981" r="32.16005687656317" fill="undefined"></circle> <circle cx="87.17485828233413" cy="488.0360410564981" r="32.16005687656317" fill="undefined"></circle> <circle cx="343.1748582823341" cy="488.0360410564981" r="32.16005687656317" fill="undefined"></circle> <circle cx="-168.82514171766587" cy="744.0360410564981" r="32.16005687656317" fill="undefined"></circle> <circle cx="87.17485828233413" cy="744.0360410564981" r="32.16005687656317" fill="undefined"></circle> <circle cx="343.1748582823341" cy="744.0360410564981" r="32.16005687656317" fill="undefined"></circle> <circle cx="-250.35297829233258" cy="149.40509863803857" r="3.6482620417032154" fill="undefined"></circle> <circle cx="5.64702170766742" cy="149.40509863803857" r="3.6482620417032154" fill="undefined"></circle> <circle cx="261.6470217076674" cy="149.40509863803857" r="3.6482620417032154" fill="undefined"></circle> <circle cx="-250.35297829233258" cy="405.40509863803857" r="3.6482620417032154" fill="undefined"></circle> <circle cx="5.64702170766742" cy="405.40509863803857" r="3.6482620417032154" fill="undefined"></circle> <circle cx="261.6470217076674" cy="405.40509863803857" r="3.6482620417032154" fill="undefined"></circle> <circle cx="-250.35297829233258" cy="661.4050986380386" r="3.6482620417032154" fill="undefined"></circle> <circle cx="5.64702170766742" cy="661.4050986380386" r="3.6482620417032154" fill="undefined"></circle> <circle cx="261.6470217076674" cy="661.4050986380386" r="3.6482620417032154" fill="undefined"></circle> <circle cx="-13.484656576945554" cy="164.98115665478082" r="43.575160794250316" fill="undefined"></circle> <circle cx="242.51534342305445" cy="164.98115665478082" r="43.575160794250316" fill="undefined"></circle> <circle cx="498.51534342305445" cy="164.98115665478082" r="43.575160794250316" fill="undefined"></circle> <circle cx="-13.484656576945554" cy="420.9811566547808" r="43.575160794250316" fill="undefined"></circle> <circle cx="242.51534342305445" cy="420.9811566547808" r="43.575160794250316" fill="undefined"></circle> <circle cx="498.51534342305445" cy="420.9811566547808" r="43.575160794250316" fill="undefined"></circle> <circle cx="-13.484656576945554" cy="676.9811566547808" r="43.575160794250316" fill="undefined"></circle> <circle cx="242.51534342305445" cy="676.9811566547808" r="43.575160794250316" fill="undefined"></circle> <circle cx="498.51534342305445" cy="676.9811566547808" r="43.575160794250316" fill="undefined"></circle> <circle cx="-104.80424333690877" cy="171.39101541585376" r="4.0269388590723505" fill="undefined"></circle> <circle cx="151.19575666309123" cy="171.39101541585376" r="4.0269388590723505" fill="undefined"></circle> <circle cx="407.19575666309123" cy="171.39101541585376" r="4.0269388590723505" fill="undefined"></circle> <circle cx="-104.80424333690877" cy="427.39101541585376" r="4.0269388590723505" fill="undefined"></circle> <circle cx="151.19575666309123" cy="427.39101541585376" r="4.0269388590723505" fill="undefined"></circle> <circle cx="407.19575666309123" cy="427.39101541585376" r="4.0269388590723505" fill="undefined"></circle> <circle cx="-104.80424333690877" cy="683.3910154158538" r="4.0269388590723505" fill="undefined"></circle> <circle cx="151.19575666309123" cy="683.3910154158538" r="4.0269388590723505" fill="undefined"></circle> <circle cx="407.19575666309123" cy="683.3910154158538" r="4.0269388590723505" fill="undefined"></circle> <circle cx="-36.771643087224504" cy="44.028287255280304" r="33.555911139885666" fill="undefined"></circle> <circle cx="219.2283569127755" cy="44.028287255280304" r="33.555911139885666" fill="undefined"></circle> <circle cx="475.2283569127755" cy="44.028287255280304" r="33.555911139885666" fill="undefined"></circle> <circle cx="-36.771643087224504" cy="300.0282872552803" r="33.555911139885666" fill="undefined"></circle> <circle cx="219.2283569127755" cy="300.0282872552803" r="33.555911139885666" fill="undefined"></circle> <circle cx="475.2283569127755" cy="300.0282872552803" r="33.555911139885666" fill="undefined"></circle> <circle cx="-36.771643087224504" cy="556.0282872552802" r="33.555911139885666" fill="undefined"></circle> <circle cx="219.2283569127755" cy="556.0282872552802" r="33.555911139885666" fill="undefined"></circle> <circle cx="475.2283569127755" cy="556.0282872552802" r="33.555911139885666" fill="undefined"></circle> 
                <animateTransform attributeName="transform" type="translate" dur="3.3333333333333335s" repeatCount="indefinite" keyTimes="0;1" values="0 0;0 -256"></animateTransform>
                </g><g>
                <circle cx="-217.51364959371494" cy="36.829634525431516" r="42.55349182953784" fill="undefined"></circle> <circle cx="38.486350406285055" cy="36.829634525431516" r="42.55349182953784" fill="undefined"></circle> <circle cx="294.48635040628506" cy="36.829634525431516" r="42.55349182953784" fill="undefined"></circle> <circle cx="-217.51364959371494" cy="292.8296345254315" r="42.55349182953784" fill="undefined"></circle> <circle cx="38.486350406285055" cy="292.8296345254315" r="42.55349182953784" fill="undefined"></circle> <circle cx="294.48635040628506" cy="292.8296345254315" r="42.55349182953784" fill="undefined"></circle> <circle cx="-217.51364959371494" cy="548.8296345254315" r="42.55349182953784" fill="undefined"></circle> <circle cx="38.486350406285055" cy="548.8296345254315" r="42.55349182953784" fill="undefined"></circle> <circle cx="294.48635040628506" cy="548.8296345254315" r="42.55349182953784" fill="undefined"></circle> <circle cx="-173.03686389174072" cy="25.21169978199083" r="23.86675532882513" fill="undefined"></circle> <circle cx="82.96313610825928" cy="25.21169978199083" r="23.86675532882513" fill="undefined"></circle> <circle cx="338.9631361082593" cy="25.21169978199083" r="23.86675532882513" fill="undefined"></circle> <circle cx="-173.03686389174072" cy="281.21169978199083" r="23.86675532882513" fill="undefined"></circle> <circle cx="82.96313610825928" cy="281.21169978199083" r="23.86675532882513" fill="undefined"></circle> <circle cx="338.9631361082593" cy="281.21169978199083" r="23.86675532882513" fill="undefined"></circle> <circle cx="-173.03686389174072" cy="537.2116997819908" r="23.86675532882513" fill="undefined"></circle> <circle cx="82.96313610825928" cy="537.2116997819908" r="23.86675532882513" fill="undefined"></circle> <circle cx="338.9631361082593" cy="537.2116997819908" r="23.86675532882513" fill="undefined"></circle> <circle cx="-240.56477046240286" cy="17.919254001085164" r="15.888931409409324" fill="undefined"></circle> <circle cx="15.435229537597138" cy="17.919254001085164" r="15.888931409409324" fill="undefined"></circle> <circle cx="271.43522953759714" cy="17.919254001085164" r="15.888931409409324" fill="undefined"></circle> <circle cx="-240.56477046240286" cy="273.91925400108516" r="15.888931409409324" fill="undefined"></circle> <circle cx="15.435229537597138" cy="273.91925400108516" r="15.888931409409324" fill="undefined"></circle> <circle cx="271.43522953759714" cy="273.91925400108516" r="15.888931409409324" fill="undefined"></circle> <circle cx="-240.56477046240286" cy="529.9192540010852" r="15.888931409409324" fill="undefined"></circle> <circle cx="15.435229537597138" cy="529.9192540010852" r="15.888931409409324" fill="undefined"></circle> <circle cx="271.43522953759714" cy="529.9192540010852" r="15.888931409409324" fill="undefined"></circle> <circle cx="-248.50850429088484" cy="94.98497567382697" r="5.255735852842664" fill="undefined"></circle> <circle cx="7.491495709115156" cy="94.98497567382697" r="5.255735852842664" fill="undefined"></circle> <circle cx="263.49149570911516" cy="94.98497567382697" r="5.255735852842664" fill="undefined"></circle> <circle cx="-248.50850429088484" cy="350.98497567382697" r="5.255735852842664" fill="undefined"></circle> <circle cx="7.491495709115156" cy="350.98497567382697" r="5.255735852842664" fill="undefined"></circle> <circle cx="263.49149570911516" cy="350.98497567382697" r="5.255735852842664" fill="undefined"></circle> <circle cx="-248.50850429088484" cy="606.984975673827" r="5.255735852842664" fill="undefined"></circle> <circle cx="7.491495709115156" cy="606.984975673827" r="5.255735852842664" fill="undefined"></circle> <circle cx="263.49149570911516" cy="606.984975673827" r="5.255735852842664" fill="undefined"></circle> <circle cx="-158.07254638742432" cy="-19.53843547724466" r="38.742905834568646" fill="undefined"></circle> <circle cx="97.92745361257568" cy="-19.53843547724466" r="38.742905834568646" fill="undefined"></circle> <circle cx="353.9274536125757" cy="-19.53843547724466" r="38.742905834568646" fill="undefined"></circle> <circle cx="-158.07254638742432" cy="236.46156452275534" r="38.742905834568646" fill="undefined"></circle> <circle cx="97.92745361257568" cy="236.46156452275534" r="38.742905834568646" fill="undefined"></circle> <circle cx="353.9274536125757" cy="236.46156452275534" r="38.742905834568646" fill="undefined"></circle> <circle cx="-158.07254638742432" cy="492.46156452275534" r="38.742905834568646" fill="undefined"></circle> <circle cx="97.92745361257568" cy="492.46156452275534" r="38.742905834568646" fill="undefined"></circle> <circle cx="353.9274536125757" cy="492.46156452275534" r="38.742905834568646" fill="undefined"></circle> <circle cx="-158.07254638742432" cy="748.4615645227553" r="38.742905834568646" fill="undefined"></circle> <circle cx="97.92745361257568" cy="748.4615645227553" r="38.742905834568646" fill="undefined"></circle> <circle cx="353.9274536125757" cy="748.4615645227553" r="38.742905834568646" fill="undefined"></circle> <circle cx="-62.86363707703492" cy="179.247490899321" r="10.691527993130778" fill="undefined"></circle> <circle cx="193.13636292296508" cy="179.247490899321" r="10.691527993130778" fill="undefined"></circle> <circle cx="449.1363629229651" cy="179.247490899321" r="10.691527993130778" fill="undefined"></circle> <circle cx="-62.86363707703492" cy="435.247490899321" r="10.691527993130778" fill="undefined"></circle> <circle cx="193.13636292296508" cy="435.247490899321" r="10.691527993130778" fill="undefined"></circle> <circle cx="449.1363629229651" cy="435.247490899321" r="10.691527993130778" fill="undefined"></circle> <circle cx="-62.86363707703492" cy="691.2474908993211" r="10.691527993130778" fill="undefined"></circle> <circle cx="193.13636292296508" cy="691.2474908993211" r="10.691527993130778" fill="undefined"></circle> <circle cx="449.1363629229651" cy="691.2474908993211" r="10.691527993130778" fill="undefined"></circle> 
                <animateTransform attributeName="transform" type="translate" dur="1.6666666666666667s" repeatCount="indefinite" keyTimes="0;1" values="0 0;0 -256"></animateTransform>
                </g><g>
                <circle cx="-140.1918747367261" cy="215.8281656560165" r="13.73491306839033" fill="undefined"></circle> <circle cx="115.8081252632739" cy="215.8281656560165" r="13.73491306839033" fill="undefined"></circle> <circle cx="371.8081252632739" cy="215.8281656560165" r="13.73491306839033" fill="undefined"></circle> <circle cx="-140.1918747367261" cy="471.8281656560165" r="13.73491306839033" fill="undefined"></circle> <circle cx="115.8081252632739" cy="471.8281656560165" r="13.73491306839033" fill="undefined"></circle> <circle cx="371.8081252632739" cy="471.8281656560165" r="13.73491306839033" fill="undefined"></circle> <circle cx="-140.1918747367261" cy="727.8281656560165" r="13.73491306839033" fill="undefined"></circle> <circle cx="115.8081252632739" cy="727.8281656560165" r="13.73491306839033" fill="undefined"></circle> <circle cx="371.8081252632739" cy="727.8281656560165" r="13.73491306839033" fill="undefined"></circle> <circle cx="-149.8468003118531" cy="137.81843909930075" r="38.016759487810226" fill="undefined"></circle> <circle cx="106.15319968814691" cy="137.81843909930075" r="38.016759487810226" fill="undefined"></circle> <circle cx="362.1531996881469" cy="137.81843909930075" r="38.016759487810226" fill="undefined"></circle> <circle cx="-149.8468003118531" cy="393.81843909930075" r="38.016759487810226" fill="undefined"></circle> <circle cx="106.15319968814691" cy="393.81843909930075" r="38.016759487810226" fill="undefined"></circle> <circle cx="362.1531996881469" cy="393.81843909930075" r="38.016759487810226" fill="undefined"></circle> <circle cx="-149.8468003118531" cy="649.8184390993008" r="38.016759487810226" fill="undefined"></circle> <circle cx="106.15319968814691" cy="649.8184390993008" r="38.016759487810226" fill="undefined"></circle> <circle cx="362.1531996881469" cy="649.8184390993008" r="38.016759487810226" fill="undefined"></circle> <circle cx="-87.34469702694548" cy="-20.384886061106215" r="39.24280026203973" fill="undefined"></circle> <circle cx="168.65530297305452" cy="-20.384886061106215" r="39.24280026203973" fill="undefined"></circle> <circle cx="424.6553029730545" cy="-20.384886061106215" r="39.24280026203973" fill="undefined"></circle> <circle cx="-87.34469702694548" cy="235.61511393889378" r="39.24280026203973" fill="undefined"></circle> <circle cx="168.65530297305452" cy="235.61511393889378" r="39.24280026203973" fill="undefined"></circle> <circle cx="424.6553029730545" cy="235.61511393889378" r="39.24280026203973" fill="undefined"></circle> <circle cx="-87.34469702694548" cy="491.6151139388938" r="39.24280026203973" fill="undefined"></circle> <circle cx="168.65530297305452" cy="491.6151139388938" r="39.24280026203973" fill="undefined"></circle> <circle cx="424.6553029730545" cy="491.6151139388938" r="39.24280026203973" fill="undefined"></circle> <circle cx="-87.34469702694548" cy="747.6151139388937" r="39.24280026203973" fill="undefined"></circle> <circle cx="168.65530297305452" cy="747.6151139388937" r="39.24280026203973" fill="undefined"></circle> <circle cx="424.6553029730545" cy="747.6151139388937" r="39.24280026203973" fill="undefined"></circle> <circle cx="-18.70404839142583" cy="-18.4708846271796" r="43.58343370157131" fill="undefined"></circle> <circle cx="237.29595160857417" cy="-18.4708846271796" r="43.58343370157131" fill="undefined"></circle> <circle cx="493.29595160857417" cy="-18.4708846271796" r="43.58343370157131" fill="undefined"></circle> <circle cx="-18.70404839142583" cy="237.5291153728204" r="43.58343370157131" fill="undefined"></circle> <circle cx="237.29595160857417" cy="237.5291153728204" r="43.58343370157131" fill="undefined"></circle> <circle cx="493.29595160857417" cy="237.5291153728204" r="43.58343370157131" fill="undefined"></circle> <circle cx="-18.70404839142583" cy="493.5291153728204" r="43.58343370157131" fill="undefined"></circle> <circle cx="237.29595160857417" cy="493.5291153728204" r="43.58343370157131" fill="undefined"></circle> <circle cx="493.29595160857417" cy="493.5291153728204" r="43.58343370157131" fill="undefined"></circle> <circle cx="-18.70404839142583" cy="749.5291153728203" r="43.58343370157131" fill="undefined"></circle> <circle cx="237.29595160857417" cy="749.5291153728203" r="43.58343370157131" fill="undefined"></circle> <circle cx="493.29595160857417" cy="749.5291153728203" r="43.58343370157131" fill="undefined"></circle> <circle cx="-222.558926957504" cy="10.083677616641978" r="7.8494628679411464" fill="undefined"></circle> <circle cx="33.44107304249599" cy="10.083677616641978" r="7.8494628679411464" fill="undefined"></circle> <circle cx="289.441073042496" cy="10.083677616641978" r="7.8494628679411464" fill="undefined"></circle> <circle cx="-222.558926957504" cy="266.083677616642" r="7.8494628679411464" fill="undefined"></circle> <circle cx="33.44107304249599" cy="266.083677616642" r="7.8494628679411464" fill="undefined"></circle> <circle cx="289.441073042496" cy="266.083677616642" r="7.8494628679411464" fill="undefined"></circle> <circle cx="-222.558926957504" cy="522.083677616642" r="7.8494628679411464" fill="undefined"></circle> <circle cx="33.44107304249599" cy="522.083677616642" r="7.8494628679411464" fill="undefined"></circle> <circle cx="289.441073042496" cy="522.083677616642" r="7.8494628679411464" fill="undefined"></circle> 
                <animateTransform attributeName="transform" type="translate" dur="1.1111111111111112s" repeatCount="indefinite" keyTimes="0;1" values="0 0;0 -256"></animateTransform>
                </g></g></g><filter id="f">
                <feDiffuseLighting lighting-color="#fafbfd" surfaceScale="0.5" result="light">
                <feDistantLight azimuth="45" elevation="60"></feDistantLight>
                </feDiffuseLighting>
                </filter></g>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'pattern12',
                'contents': '''
                <pattern width="1" height="1" 
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid meet">
                    <rect width="1" height="1">
                    <animate attributeName="fill" values="red;blue;red" dur="3s" repeatCount="indefinite" />
                    </rect>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'pattern13',
                'contents': '''
                <pattern width="1" height="1" 
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid meet">
                    <rect width="1" height="1">
                    <animate attributeName="fill" values="red;yellow;red" dur="3s" repeatCount="indefinite" />
                    </rect>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'pattern14',
                'contents': '''
                <pattern width="1" height="1" 
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid meet">
                    <rect width="1" height="1">
                    <animate attributeName="fill" values="green;red;greed" dur="3s" repeatCount="indefinite" />
                    </rect>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif1',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/L5w1.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif2',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/aesthetic-shapes.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif3',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/chevron.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif4',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/circleline.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif5',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/flowers.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif6',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/giphy.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif7',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/hexagon.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif8',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/kaleidoscope-starseeds.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif9',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/mandara.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif11',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/nova.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif12',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/patterns-colors.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif13',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/snow01.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif14',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/yule-log-fireplace.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif15',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/santa-icegif-12.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif16',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/5c677d9ac66cfda7921d02c94a9c8e6f.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif17',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/13039.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif18',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/13045.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif18',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/AffectionateWeeBullfrog-size_restricted.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif19',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/giphy_1.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif20',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/giphy_2.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif21',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/giphy_11.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif22',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/giphy_4.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif23',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/giphy_5.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif24',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/giphy_9.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'svg-pattern',
                'name': 'gif25',
                'contents': '''
                <pattern width="100%" height="100%"
                    patternContentUnits="objectBoundingBox"
                    preserveAspectRatio="xMidYMid slice">
                    <image xlink:href="https://club-dosomething.github.io/temp/AdmiredImpressiveJohndory.gif" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid slice"/>
                </pattern>
                '''
            },
            {
                'type': 'css-pattern',
                'name': 'lineanimation1',
                'contents': '''
                .lineanimation1 {
                    filter: blur(3px);
                    stroke:#ff6700;
                    stroke-width:3;
                    stroke-linecap: round;
                    stroke-miterlimit:3;
                    stroke-dasharray:1600;
                    stroke-dashoffset:1600;
                    animation: lineanimation1_keyframes 3s forwards infinite;
                    animation-direction:alternate-reverse;
                }

                @keyframes lineanimation1_keyframes {
                    to {
                        stroke-dashoffset: 0;
                        stroke: #00f9ff;
                    }
                }
                '''
            },
            {
                'type': 'css-pattern',
                'name': 'lineanimation2',
                'contents': '''
                .lineanimation2 {
                    filter: blur(3px);
                    stroke:#cc231e;
                    stroke-width:3;
                    stroke-linecap: round;
                    stroke-miterlimit:3;
                    stroke-dasharray:1600;
                    stroke-dashoffset:1600;
                    animation: lineanimation2_keyframes 3s forwards infinite;
                    animation-direction:alternate-reverse;
                }

                @keyframes lineanimation2_keyframes {
                    to {
                        stroke-dashoffset: 0;
                        stroke: #edff00;
                    }
                }
                '''
            },
            {
                'type': 'css-pattern',
                'name': 'lineanimation3',
                'contents': '''
                .lineanimation3 {
                    filter: blur(3px);
                    stroke:#34A65F;
                    stroke-width:3;
                    stroke-linecap: round;
                    stroke-miterlimit:3;
                    stroke-dasharray:1600;
                    stroke-dashoffset:1600;
                    animation: lineanimation2_keyframes 3s forwards infinite;
                    animation-direction:alternate-reverse;
                }

                @keyframes lineanimation3_keyframes {
                    to {
                        stroke-dashoffset: 0;
                        stroke: #cc231e;
                    }
                }
                '''
            }
        ]

import redis

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
REDIS_CHAN = 'screen'
redis = redis.from_url(REDIS_URL)

screenParser = app.parser()
screenParser.add_argument('data')

screenAPI = app.namespace('screen', description='Screen APIs')
@screenAPI.route('/<string:screen_id>')
@screenAPI.expect(screenParser)
class ScreenClass(Resource):
    def post(self, screen_id):
        args = screenParser.parse_args()
        data = args['data']
        redis.set(screen_id, data)
        redis.publish(REDIS_CHAN, str(screen_id))
        return { 'result': screen_id }

from flask_sockets import Sockets

sockets = Sockets(application)

class ScreenBackend(object):
    def __init__(self):
        self.screens = {}
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)
    
    def __iter_data(self):
        for msg in self.pubsub.listen():
            screen_id = msg.get('data')
            if msg['type'] == 'message':
                application.logger.info(u'Sending message: {}'.format(screen_id))
                yield screen_id
    
    def register(self, screen, screen_id):
        self.screens[screen_id] = screen
    
    def send(self, screen, screen_id):
        try:
            data = redis.get(screen_id)
            screen.send(data.decode('utf-8'))
        except Exception:
            del self.screens[screen]

    def run(self):
        for key in self.__iter_data():
            screen_id = key.decode('ascii')
            if screen_id in self.screens:
                screen = self.screens[screen_id]
                gevent.spawn(self.send, screen, screen_id)
    
    def start(self):
        gevent.spawn(self.run)

screenBackend = ScreenBackend()
screenBackend.start()

from random import randint

@sockets.route('/register')
def screen_register_event(ws):
    while not ws.closed:
        screen_id = ws.receive()
        if not screen_id or not screen_id.strip():
            screen_id = str(randint(1000, 9999))
        screenBackend.register(ws, screen_id)
        # ws.send(screen_id)

if __name__ == '__main__':
    #application.run(host='0.0.0.0', port=8090, debug=True)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 8090), application, handler_class=WebSocketHandler)
    server.serve_forever()
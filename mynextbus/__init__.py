from flask import (Flask, request, g)
from flask_autodoc import Autodoc
from flask_restful import Api
from mynextbus.common.util import (output_both, output_json, output_xml)
from mynextbus.resources.agencies import Agencies
from mynextbus.resources.favicon import Favicon
from mynextbus.resources.inactiveroutes import InActiveRoutes
from mynextbus.resources.predictions import Predictions
from mynextbus.resources.routeconfig import RouteConfig
from mynextbus.resources.routemessages import RouteMessages
from mynextbus.resources.routes import Routes
from mynextbus.resources.routeschedule import RouteSchedule
from mynextbus.resources.vehiclelocations import VehicleLocations
from operator import itemgetter
from os import environ
from sys import version_info
from time import time
from xml.sax.saxutils import escape
from flask_restful import Resource


# WARNING! These two variables are being used as globals in non thread safe manner.
slow_queries = []
endpoint_counter = dict()


app = Flask(__name__)
api = Api(app)
auto = Autodoc(app)


#
# Config
#
app.config.from_object('mynextbus.config')

# Allow overriding the default config via the MYNEXTBUS_CONFIG environment variable:
if 'MYNEXTBUS_CONFIG' in environ:
    app.config.from_envvar('MYNEXTBUS_CONFIG')


#
# Request statistics
#
@app.before_request
def before_request():
    global endpoint_counter

    g.time_started = time()
    if request.url_rule is not None:
        endpoint = request.url_rule.rule
        if endpoint in endpoint_counter:
            endpoint_counter[endpoint] += 1
        else:
            endpoint_counter[endpoint] = 1


@app.after_request
def after_request(response):
    global slow_queries
    g.time_stopped = time()
    g.time_taken = g.time_stopped - g.time_started
    if g.time_taken >= app.config['NEXTBUS_SLOW_REQUEST_THRESHOLD']:
        slow_queries.append((request.path, g.time_taken))
        slow_queries.sort(key=itemgetter(1), reverse=True)
        if len(slow_queries) > app.config['NEXTBUS_SLOW_REQUESTS_LIST_SIZE']:
            slow_queries = slow_queries[:app.config['NEXTBUS_SLOW_REQUESTS_LIST_SIZE']]
    return response


class SlowQueries(Resource):
    """A list of slow requests."""
    def get(self):
        global slow_queries

        data = '<body>'

        if slow_queries is not None:
            for endpoint, time_taken in slow_queries:
                data += '<query><endpoint>' + escape(endpoint) + '</endpoint><timetaken>' + str(
                        time_taken) + '</timetaken></query>'

        data += '</body>'
        code = 200
        return data, code


class TotalQueries(Resource):
    """The total number of queries made to each of the endpoints."""
    def get(self):
        global endpoint_counter

        data = '<body>'

        if endpoint_counter is not None:
            if version_info > (3, 0):
                for endpoint, count in endpoint_counter.items():
                    data += '<query><endpoint>' + escape(endpoint) + '</endpoint><count>' + str(
                        count) + '</count></query>'
            else:
                for endpoint, count in endpoint_counter.iteritems():
                    data += '<query><endpoint>' + escape(endpoint) + '</endpoint><count>' + str(
                        count) + '</count></query>'

        data += '</body>'
        code = 200
        return data, code


#
# Representations
#
api.representations['application/json'] = output_json
api.representations['application/x-xml'] = output_xml
api.representations['application/xml'] = output_xml
api.representations['misc/both'] = output_both
api.representations['text/xml'] = output_xml


#
# Resources
#
api.add_resource(Agencies, '/agencies')
api.add_resource(Favicon, '/favicon.ico')
api.add_resource(InActiveRoutes, '/inactiveroutes/<string:agency_tag>/<int:epoch_time>')
api.add_resource(Predictions,
                 '/predictions/<string:prediction_type>/<string:agency_tag>/<int:stop_id>',
                 '/predictions/<string:prediction_type>/<string:agency_tag>/<int:stop_id>/<string:route_tag>',
                 '/predictions/<string:prediction_type>/<string:agency_tag>/<string:stop_tag>/<string:route_tag>',
                 '/predictions/<string:prediction_type>/<string:agency_tag>/<string:route_stop_tuples>')
api.add_resource(RouteConfig, '/routeconfig/<string:agency_tag>/<string:route_tag>')
api.add_resource(RouteMessages, '/messages/<string:agency_tag>/', '/messages/<string:agency_tag>/<string:route_tags>')
api.add_resource(RouteSchedule, '/schedule/<string:agency_tag>/<string:route_tag>')
api.add_resource(Routes, '/routes/<string:agency_tag>')
api.add_resource(VehicleLocations, '/vehiclelocations/<string:agency_tag>/<string:route_tag>/<int:epoch_time>')
api.add_resource(TotalQueries, '/totalqueries')
api.add_resource(SlowQueries, '/slowqueries')




# Decorate all endpoints with Autodoc.doc():
if version_info > (3, 0):
    for endpoint, function in app.view_functions.items():
        app.view_functions[endpoint] = auto.doc()(function)
else:
    for endpoint, function in app.view_functions.iteritems():
        app.view_functions[endpoint] = auto.doc()(function)


@app.route('/')
def doc():
    return auto.html(title='MyNextBus API', template="autodoc_custom.html")

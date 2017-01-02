from flask_restful import (Resource, reqparse)
from mynextbus.common.util import (build_error_xml, get_nextbusxmlfeed_response)


class Predictions(Resource):
    """Obtain arrival/departure predictions for a stop or a set of stops.<br>
    <br>
    Note: prediction_types can be one of:
    <ul>
        <li>all_routes - Requires: agency_tag + stop_id</li>
        <li>single_route - Requires: agency_tag + stop_id + route_tag</li>
        <li>specific_stop - Requires: agency_tag + route_tag + stop_tag</li>
        <li>multiple_stops - Requires: agency_tag + route_stop_tuples. Where route_stop_tuples are of the form
        route_tag|stop_tag seperated by commas. e.g. /predictions/multiple_stops/sf-muni/E|5184,38R|7620</li>
    </ul>
    """
    def get(self, prediction_type, agency_tag='', stop_id='', stop_tag='', route_tag='', route_stop_tuples=''):

        # Handle requests where short titles are required.
        parser = reqparse.RequestParser()
        parser.add_argument('useShortTitles', type=bool, default=False, required=False, help='Return short titles intended for display devices with small screens')
        args = parser.parse_args()
        short_title = args['useShortTitles']

        if prediction_type == 'all_routes':
            if agency_tag == '':
                data = build_error_xml('Agency parameter "a" must be specified in query string.')
                code = 500
            elif stop_id == '':
                data = build_error_xml('Stop id parameter "stopId" must be specified in query string.')
                code = 500
            else:
                data, code = get_nextbusxmlfeed_response('?command=predictions&a=' + str(agency_tag) + '&stopId=' + str(stop_id) + '&useShortTitles=' + str(short_title))
        elif prediction_type == 'single_route':
            if agency_tag == '':
                data = build_error_xml('Agency parameter "a" must be specified in query string.')
                code = 500
            elif stop_id == '':
                data = build_error_xml('Stop id parameter "stopId" must be specified in query string.')
                code = 500
            elif route_tag == '':
                data = build_error_xml('Route parameter "r" must be specified in query string.')
                code = 500
            else:
                data, code = get_nextbusxmlfeed_response('?command=predictions&a=' + str(agency_tag) + '&stopId=' + str(stop_id) + '&routeTag=' + str(route_tag) + '&useShortTitles=' + str(short_title))
        elif prediction_type == 'specific_stop':
            if agency_tag == '':
                data = build_error_xml('Agency parameter "a" must be specified in query string.')
                code = 500
            elif route_tag == '':
                data = build_error_xml('Route parameter "r" must be specified in query string.')
                code = 500
            elif stop_tag == '':
                data = build_error_xml('Stop parameter "s" must be specified in query string.')
                code = 500
            else:
                data, code = get_nextbusxmlfeed_response('?command=predictions&a=' + str(agency_tag) + '&routeTag=' + str(route_tag) + '&s=' + str(stop_tag) + '&useShortTitles=' + str(short_title))
        elif prediction_type == 'multiple_stops':
            if agency_tag == '':
                data = build_error_xml('Agency parameter "a" must be specified in query string.')
                code = 500
            elif route_stop_tuples == '':
                data = build_error_xml('Route parameter "r" must be specified in query string.')
                code = 500
            else:
                stops = '&stops='.join(route_stop_tuples.split(','))
                data, code = get_nextbusxmlfeed_response('?command=predictionsForMultiStops&a=' + str(agency_tag) + '&stops=' + str(stops) + '&useShortTitles=' + str(short_title))
        else:
            data = build_error_xml('Prediction type must be specified in query string.')
            code = 500
        return data, code

from flask_restful import Resource
from mynextbus.common.util import get_nextbusxmlfeed_response


class RouteMessages(Resource):
    """Obtains messages currently active for a route or a group of routes.<br>
    <br>
    Note: route_tags is optional and is composed of one or more route_tags seperated by commas.
    e.g. /messages/sf-muni/E,38R
    """
    def get(self, agency_tag, route_tags = ''):
        routes = '&r='.join(route_tags.split(','))
        if route_tags == '':
            data, code = get_nextbusxmlfeed_response('?command=messages&a=' + str(agency_tag))
        else:
            data, code = get_nextbusxmlfeed_response('?command=messages&a=' + str(agency_tag) + '&r=' + str(routes))
        return data, code

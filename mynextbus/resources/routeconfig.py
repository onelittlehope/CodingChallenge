from flask_restful import Resource
from mynextbus.common.util import get_nextbusxmlfeed_response


class RouteConfig(Resource):
    """
    Obtains detailed route data for an agency. The route data returned includes lists of stops, lists of directions,
    and lists of paths.
    """
    def get(self, agency_tag, route_tag):
        data, code = get_nextbusxmlfeed_response('?command=routeConfig&a=' + str(agency_tag) + '&r=' + str(route_tag))
        return data, code

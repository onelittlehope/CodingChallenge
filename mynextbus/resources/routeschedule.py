from flask_restful import Resource
from mynextbus.common.util import get_nextbusxmlfeed_response


class RouteSchedule(Resource):
    """Obtains schedule information for a route."""
    def get(self, agency_tag, route_tag):
        data, code = get_nextbusxmlfeed_response('?command=schedule&a=' + str(agency_tag) + '&r=' + str(route_tag))
        return data, code

from flask_restful import Resource
from mynextbus.common.util import get_nextbusxmlfeed_response


class Routes(Resource):
    """Obtains a list of routes for an agency."""
    def get(self, agency_tag):
        data, code = get_nextbusxmlfeed_response('?command=routeList&a=' + str(agency_tag))
        return data, code

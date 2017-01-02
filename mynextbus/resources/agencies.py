from flask_restful import Resource
from mynextbus.common.util import get_nextbusxmlfeed_response


class Agencies(Resource):
    """Obtains a list of agencies."""
    def get(self):
        data, code = get_nextbusxmlfeed_response('?command=agencyList')
        return data, code

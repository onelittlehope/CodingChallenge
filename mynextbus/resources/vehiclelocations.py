from flask_restful import Resource
from mynextbus.common.util import get_nextbusxmlfeed_response


class VehicleLocations(Resource):
    """Obtains a list of vehicle locations that have changed since the time specified."""
    def get(self, agency_tag, route_tag, epoch_time):
        data, code = get_nextbusxmlfeed_response('?command=vehicleLocations&a=' + str(agency_tag) + '&r=' + str(route_tag) + '&t=' + str(epoch_time))
        return data, code

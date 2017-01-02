from flask_restful import Resource
from mynextbus.common.util import (build_error_xml, get_nextbusxmlfeed_response)
from mynextbus.common.util import minmax
import time
import xml.etree.ElementTree as ET
import xmltodict


class InActiveRoutes(Resource):
    """Obtains a list of routes that are not running at a specified time."""
    def get(self, agency_tag, epoch_time):

        try:
            # We convert the specified epoch time to a format that we can use with the route schedules from the
            # NextBusXMLFeed XML feed. The epoch time in NextBusXMLFeed schedules is of the form: 19140000
            # Which is 05:19:00 on 01/01/1970 if you remove the trailing three zeroes. i.e. 19140000 --> 19140
            # (I don't understand why they have those trailing zeroes. :-|)
            time_hms = time.strftime("%H:%M:%S", time.gmtime(epoch_time))
            time_epoch_int =  int(time.mktime(time.strptime('1970-01-01 ' + time_hms, '%Y-%m-%d %H:%M:%S')))
            time_epoch_str = str(time_epoch_int) + '000'
            time_epoch_int = int(time_epoch_str)

            # We convert the specified epoch time to ascertain the weekday in a form we can use with the route schedules
            # from the NextBusXMLFeed XML feed.
            time_weekday_int = int(time.strftime("%w", time.gmtime(epoch_time)))
            if time_weekday_int == 0:
                time_weekday = 'sun'
            elif time_weekday_int == 6:
                time_weekday = 'sat'
            else:
                time_weekday = 'wkd'
        except ValueError:
            code = 500
            data = build_error_xml(str(code) + ' Invalid value specified for parameter "epoch_time".')
            return data, code

        # Used to store the list of inactive routes.
        inactive_routes_list = []

        # Get a list of current routes for the specified agency
        routes_xml, code = get_nextbusxmlfeed_response('?command=routeList&a=' + str(agency_tag))
        if code == 500:
            data = build_error_xml(str(code) + ' Could not get a list of routes for agency: "{}".'.format(str(agency_tag)))
            return data, code

        routes = xmltodict.parse(routes_xml)

        if 'route' in routes['body'] and routes['body']['route']:

            # For each route:
            for route in routes['body']['route']:
                #print('DEBUG: Processing route: {} - {}'.format(route['@tag'], route['@title']))

                # Get its schedule:
                schedule_xml, code = get_nextbusxmlfeed_response('?command=schedule&a=' + str(agency_tag) + '&r=' + str(route['@tag']))

                #print('DEBUG: Got the route schedule. Parsing XML.')
                schedule_tree = ET.fromstring(schedule_xml)

                #print('DEBUG: Finding stops for: ' + time_weekday)

                # Find all stops which have an epochTime attribute, in routes where serviceClass = time_weekday:
                route_stops_tree = schedule_tree.findall('.//route/[@serviceClass="' + time_weekday + '"]//stop/[@epochTime]')

                # If we found some stops...
                if route_stops_tree:

                    #print('DEBUG: Making a list of the stop epochtimes.')

                    # Make a list of the stop epochtimes in the schedule
                    stop_epochtimes = []
                    for route_stop in route_stops_tree:
                        if route_stop.attrib['epochTime'] != '-1':
                            stop_epochtimes.append(route_stop.attrib['epochTime'])

                    # The min stop epochtime is the route's start time, the max is its finish time.
                    min_stop_time_str, max_stop_time_str = minmax(stop_epochtimes)
                    min_stop_time = int(min_stop_time_str)
                    max_stop_time = int(max_stop_time_str)

                    #print('DEBUG: Route start time is {} and finish time is {}'.format(min_stop_time_str, max_stop_time_str))

                    # The finish time can extend onto the next day and so we account for this:
                    if max_stop_time >= 86400000:
                        # As the finish time ran into the next day, remove a days worth of epoch time from it
                        # and adjust the logic that checks whether the route is inactive.
                        max_stop_time = max_stop_time - 86400000
                        #print('DEBUG: The route''s finish time extended into the next day. Adjusting it to {}'.format(max_stop_time))
                        if time_epoch_int >= max_stop_time and time_epoch_int <= min_stop_time:
                            inactive_routes_list.append(route)
                            #print('DEBUG: Route "{}" was inactive at the specified time {}'.format(route['@tag'], time_epoch_str))
                    else:
                        if time_epoch_int <= min_stop_time or time_epoch_int >= max_stop_time:
                            inactive_routes_list.append(route)
                            #print('DEBUG: Route "{}" was inactive at the specified time {}'.format(route['@tag'], time_epoch_str))

            # Assign the inactive route list to the routes dict and build the XML that is to be sent back
            routes['body']['route'] = inactive_routes_list
            data = xmltodict.unparse(routes)
            code = 200
        else:
            code = 500
            data = build_error_xml(str(code) + ' No routes returned for agency: "{}".'.format(str(agency_tag)))
        return data, code

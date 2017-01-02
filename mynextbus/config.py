from os import path

# Define the application directory
NEXTBUS_BASE_DIR = path.abspath(path.dirname(__file__))

# - NextBusXMLFeed Service URL.
#   NextBus provides a real-time data feed that exposes bus and train service
#   information to the public. The instructions for using the real-time data
#   feed are here: http://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf
NEXTBUS_WEBSERVICE_URI = 'http://webservices.nextbus.com/service/publicXMLFeed'

# If you need to use a proxy:
NEXTBUS_WEBSERVICE_PROXIES = {}

# - In seconds, how long do we wait for a response from the NextBusXMLFeed
#   service
NEXTBUS_WEBSERVICE_TIMEOUT = 10

# How many slow requests to keep track of.
NEXTBUS_SLOW_REQUESTS_LIST_SIZE = 10

# - Queries that take more than SLOW_REQUEST_THRESHOLD seconds to process are
#   kept track of up to a maximum of SLOW_REQUESTS_LIST_SIZE entries.
NEXTBUS_SLOW_REQUEST_THRESHOLD = 1

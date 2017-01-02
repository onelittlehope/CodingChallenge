from flask import (json, make_response)
from xml.sax.saxutils import escape
import requests
import xmltodict
from mynextbus.config import (NEXTBUS_WEBSERVICE_PROXIES, NEXTBUS_WEBSERVICE_URI, NEXTBUS_WEBSERVICE_TIMEOUT)


def build_error_xml(msg):
    return '<body><Error>' + escape(str(msg)) + '</Error></body>'


def get_nextbusxmlfeed_response(svc_url_params):
    svc_url = NEXTBUS_WEBSERVICE_URI + svc_url_params
    try:
        response = requests.get(svc_url, timeout=NEXTBUS_WEBSERVICE_TIMEOUT, proxies=NEXTBUS_WEBSERVICE_PROXIES)
        response.raise_for_status()
        try:
            # We check if valid XML was returned by the NextBusXMLFeed service:
            xml_dict = xmltodict.parse(response.content)
        except xmltodict.expat.ExpatError as xml_err:
            code = 500
            data = build_error_xml(str(code) + ' Server Error: ' + str(xml_err) +
                                   ': Invalid XML was returned for url: ' + str(svc_url))
        else:
            # It was valid XML but it is still possible that the NextBusXMLFeed
            # service returned an Error XML object.
            data = response.content
            code = response.status_code
    except requests.exceptions.HTTPError as err:
        # The web request to the NextBusXMLFeed service failed:
        data = build_error_xml(str(err))
        code = 500
    except requests.exceptions.RequestException as err:
        # A lower level connection issue occurred:
        data = build_error_xml(str(err))
        code = 500
    return data, code


# An O(n) way of getting the min/max values from a list.
# Source: http://stackoverflow.com/a/15150820
def minmax(x):
    # this function fails if the list length is 0
    minimum = maximum = x[0]
    for i in x[1:]:
        if i < minimum:
            minimum = i
        else:
            if i > maximum:
                maximum = i
    return minimum, maximum


# Expects data to be valid xml!
def output_both(data, code, headers=None):
    xml_dict = xmltodict.parse(data)
    resp = make_response(json.jsonify(xml_dict).data + data, code)
    resp.headers.extend(headers or {})
    return resp


# Expects data to be valid xml!
def output_json(data, code, headers=None):
    xml_dict = xmltodict.parse(data)
    resp = make_response(json.jsonify(xml_dict).data, code)
    resp.headers.extend(headers or {})
    return resp


# Expects data to be valid xml!
def output_xml(data, code, headers=None):
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp

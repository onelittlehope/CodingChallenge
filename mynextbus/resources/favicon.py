from flask import send_from_directory
from flask_restful import Resource
from os import path
from mynextbus.config import NEXTBUS_BASE_DIR


class Favicon(Resource):
    """Fallback for when a favicon isn't setup in the website's root."""
    def get(self):
        return send_from_directory(path.join(NEXTBUS_BASE_DIR, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

from datetime import datetime
import socket

from flask_restful import Resource

from . import api


@api.resource('/hostname')
class HostnameAPI(Resource):
    def get(self):
        return {'hostname': socket.gethostname()}


@api.resource('/time')
class TimeAPI(Resource):
    def get(self):
        return {'time': str(datetime.now())}

from flask import send_file
from flask_restful import Resource

class HealthCheck(Resource):
    def get(self):
        """
        Application is working
        ---
        responses:
          200:
            description: Success
        """
        return {"message": "Working!!!  :)"}


class CheckSocket(Resource):
    def get(self):
        return send_file('index.html')

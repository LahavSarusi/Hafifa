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
        return "Working!!!  :)"

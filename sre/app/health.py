from flask import Response

def check_health(app):
    """
    Creates a simple Flask endpoint that checks the overall health of the service.
    """
    @app.route('/health')
    def health_check():
        """
        Returns a 200 OK status if the service is operational.
        """
        return Response("OK", status=200)
    return app

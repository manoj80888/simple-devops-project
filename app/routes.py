import socket


def register_routes(app):

    @app.get("/")
    def home():
        return {
            "application": "DevOps Demo Application",
            "status": "UP",
            "version": "1.0.0",
            "environment": "Development",
            "hostname": socket.gethostname()
        }

    @app.get("/health")
    def health():
        return {
            "status": "UP"
        }
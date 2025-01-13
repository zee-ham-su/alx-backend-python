import logging
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        with open("requests.log", "a") as log_file:
            log_file.write(log_message + "\n")

        response = self.get_response(request)
        return response
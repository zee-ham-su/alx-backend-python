import logging
from datetime import datetime, time
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden


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


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time(21, 0)
        end_time = time(6, 0)

        from datetime import datetime
        now = datetime.now().time()

        if start_time <= now or now <= end_time:
            return HttpResponseForbidden("Access to the messaging app is restricted between 9 PM and 6 AM.")

        response = self.get_response(request)
        return response

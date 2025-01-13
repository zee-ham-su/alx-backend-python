import logging
from datetime import datetime, time, timedelta
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from collections import defaultdict

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



class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_count = defaultdict(list)
        self.MESSAGE_LIMIT = 5
        self.TIME_WINDOW = timedelta(minutes=1)

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')

        if request.method == 'POST':
            now = datetime.now()
            self.ip_message_count[ip_address] = [
                timestamp for timestamp in self.ip_message_count[ip_address]
                if now - timestamp < self.TIME_WINDOW
            ]
            if len(self.ip_message_count[ip_address]) >= self.MESSAGE_LIMIT:
                return HttpResponseForbidden("You have exceeded the message limit. Please try again later.")
            self.ip_message_count[ip_address].append(now)
        response = self.get_response(request)
        return response


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ALLOWED_ROLES = ['admin', 'host'] 
        user = request.user
        if hasattr(user, 'role'):
            user_role = user.role
        else:
            user_role = 'guest'
        if user_role not in ALLOWED_ROLES:
            return HttpResponseForbidden("You do not have permission to perform this action.")
        response = self.get_response(request)
        return response
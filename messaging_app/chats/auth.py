from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        user, token = super().authenticate(request)
        if user:
            print(f"User {user.email} authenticated successfully with token {token}")
        return user, token

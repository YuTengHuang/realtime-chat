from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from channels.db import database_sync_to_async
from django.conf import settings

import jwt
from datetime import datetime

from django.contrib.auth import get_user_model
User = get_user_model()



class CustomAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            token_str = scope["query_string"].decode('utf-8').split('=')[1]
            user_id = AccessToken(token_str)["user_id"]

            payload = jwt.decode(token_str, settings.SECRET_KEY, algorithms=["HS256"])
            exp_timestamp = payload.get("exp")
            exp_time = datetime.fromtimestamp(exp_timestamp)

            scope['exp_time'] = exp_time
            scope['user'] = await get_user(user_id)
        except TokenError:
            scope['error'] = '連線逾時，請重新登入!'
        return await self.app(scope, receive, send)

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken


User = get_user_model()
class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        try:
            headers = dict(scope['headers'])
            if b'authorization' in headers:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name.lower() == 'bearer':
                    validated_token = await self.validate_token(token_key)
                    scope['user'] = await self.get_user(validated_token)
            else:
                print('Authorization Token was not provided')
                scope['user'] = None
        except InvalidToken:
            print('Invalid token')
            scope['user'] = None
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def validate_token(self, token_key):
        authentication = JWTAuthentication()
        validated_token = authentication.get_validated_token(token_key)
        return validated_token

    @database_sync_to_async
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            user = User.objects.filter(id=user_id, is_active=True).first()
            return user
        except (User.DoesNotExist, KeyError):
            return AnonymousUser()
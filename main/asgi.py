import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from notification import consumers

from django.urls import re_path,path
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(
    URLRouter(
    [re_path(r'ws/notification/(?P<room_name>\w+)/$', consumers.NotificationConsumer.as_asgi()),]
    ))
    
    
    
})
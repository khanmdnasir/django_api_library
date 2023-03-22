from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/ticket/(?P<group_name>\w+)/(?P<room_name>\w+)/$", consumers.TicketConsumer.as_asgi()),
    
    #group_name = 'admin' , room_id = "admin
    #group_name = 'agent' , room_id = agent_id
    #group_name = 'details' , room_id = ticket_id
]
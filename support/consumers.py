# chat/consumers.py
import json
from .models import *
from .serializers import *
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.separator = "_"

        if self.group_name=='user' and ("@" in self.room_name):
            self.room_group_name = "ticket_%s_%s" % (str(self.group_name) , str(self.room_name).replace('@','') )
        else:
            self.room_group_name = "ticket_%s_%s" % (str(self.group_name), self.room_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        

        user = self.scope['user']

        if user is None:
            await self.send(json.dumps({"message": "Unauthenticated User"}))
            print('disconnected')
            await self.close()


        # # group_name =[admin/agent/user/details], room_name = [None/agent_id/user's_email/ticket_id]
        # data = await self.get_queryset(self.group_name, self.room_name) 
        # # sending data when channel is connected
        # await self.channel_layer.group_send(
        #     self.room_group_name, {"type": "send_ticket_data", "message": data}
        # )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "send_ticket_data", "message": data}
        )

    async def send_ticket_data(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
    


    async def send_comment_data(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def get_queryset(self, source, source_id=None):
        data = None

        if source=='admin':
            tickets = TicketModel.objects.filter(is_active=True).all()
            data = TicketSerializer(tickets, many=True).data

        elif source=='agent' and source_id!=None:
            tickets = TicketModel.objects.filter(is_active=True,support_agent__id=source_id).all()
            data = TicketSerializer(tickets, many=True).data

        elif source=='user' and source_id!=None:
            tickets = TicketModel.objects.filter(is_active=True,email=source_id).all()
            data = TicketSerializer(tickets, many=True).data

        elif source=='details' and source_id!=None:
            tickets = TicketModel.objects.filter(is_active=True,id=source_id).first()
            data = TicketSerializer(tickets, many=False).data

        return data



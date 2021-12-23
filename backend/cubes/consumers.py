import json

from channels.generic.websocket import AsyncWebsocketConsumer

from config.rooms import free_room_ids, open_room_ids, closed_room_ids


class PlayerConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.room_id = None
        self.room_group_name = None
        self.is_creator = False
        super().__init__(*args, **kwargs)

    async def connect(self):

        command = self.scope['url_route']['kwargs']['command']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'room_%d' % self.room_id

        if command == "create":
            if self.room_id not in free_room_ids:
                await self.disconnect(401)

            else:
                self.is_creator = True
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.accept()
                open_room_ids.append(self.room_id)

        elif command == "join":

            if self.room_id not in open_room_ids:
                await self.disconnect(401)

            else:
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        if self.is_creator:
            if self.room_id in closed_room_ids:
                closed_room_ids.remove(self.room_id)

            if self.room_id not in open_room_ids:
                open_room_ids.append(self.room_id)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        if self.is_creator:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_to_players',
                    'message': text_data
                }
            )
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_to_creator',
                    'message': text_data
                }
            )

    async def send_to_creator(self, event):
        if self.is_creator:
            await self.send(event['message'])

    async def send_to_players(self, event):
        if not self.is_creator:
            await self.send(event['message'])

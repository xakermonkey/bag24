from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from bag_admin.models import *
from sab_api.serializers import *


class sendItemConsumer(WebsocketConsumer):
    def connect(self):
        self.lg_id = self.scope['url_route']['kwargs']['pk']
        self.lg_group = 'lg_' + str(self.lg_id)

        async_to_sync(self.channel_layer.group_add)(
            self.lg_group,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.lg_group,
            self.channel_name
        )

    def receive(self, text_data=None):
        async_to_sync(self.channel_layer.group_send)(
            self.lg_group,
            {
                'type': 'send_item',
                'id': text_data
            }
        )

    def send_item(self, event):
        id = int(event['id'])
        item = SABItem.objects.get(pk=id)
        name = WorkerInfo.objects.get(user=item.user).name
        item_ser = SABItemSerializer(item)
        lg_ser = LGSerializer(item.place)
        photo = Photos.objects.filter(item=item)
        photo_arr = [i.photo.url for i in photo]
        self.send(text_data=json.dumps({
            'event': 'Send',
            'name': name,
            'item': item_ser.data,
            'photos': photo_arr,
            'lg': lg_ser.data
        }))


class acceptItemConsumer(WebsocketConsumer):
    def connect(self):
        self.worker = self.scope['url_route']['kwargs']['user']
        self.lg_group = 'worker' + str(self.worker)

        async_to_sync(self.channel_layer.group_add)(
            self.lg_group,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.lg_group,
            self.channel_name
        )

    def receive(self, text_data=None):
        info = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.lg_group,
            {
                'type': 'send_item',
                'status': info.get('status'),
                'id': info.get('id')
            }
        )

    def send_item(self, event):
        id = event["id"]
        status = event["status"]
        self.send(text_data=json.dumps({
            'event': 'Send',
            'id': id,
            "status": status
        }))

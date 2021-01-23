import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.contrib.auth import get_user_model
import base64
from django.core.files.base import ContentFile

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    
    def fetch_messages(self, data):
        # print('messageeeeqqqqe',data)
        messages = Message.last_10_messages()
        content = {
            'command':'messages',
            'messages': self.messages_to_json(messages)
        }
        # print('contentttt',content)

        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        print('typeeeeee',data['msg_type'])
        file_type = data['msg_type'][:5]
        print(file_type)
        # print('messageeeee',data)
        if file_type == 'image' or file_type == 'audio' or file_type == 'video':
            print('insideeee')
            # print(data['message'])
            file_data = data['message']
            format, filestr = file_data.split(';base64,')
            ext = format.split('/')[-1]
            print('formatttttt',ext)
            file_decoded = ContentFile(base64.b64decode(filestr), name='temp.' + ext)
            content_msg = ""
            print('fileeeeeeee',file_decoded)
            msg_type = file_type
            author_user = User.objects.filter(username = author)[0]
            message = Message.objects.create(author = author_user,content=content_msg,file_uploaded=file_decoded,file_type=file_type) 

        else:
            content_msg = data['message']
            msg_type = data['msg_type']
            author_user = User.objects.filter(username = author)[0]
            message = Message.objects.create(author = author_user,content=content_msg,file_type=msg_type)   
     
        # print('base644444',data['message'])
        # msg_type = data['msg_type']
        content = {
            'command':'new_message',
            'message':self.message_to_json(message)
        }
        return self.send_chat_message(content)


    def messages_to_json(self, messages):
        result =[]
        for message in messages:
            result.append(self.message_to_json(message))
        return result


    def message_to_json(self,message):
        if message.content == "":
            return{
                'author': message.author.username,
                'content':message.file_uploaded.url,
                'timestamp': str(message.timestamp),
                'msg_type' : message.file_type
            }
        else:
            return{
            'author': message.author.username,
            'content':message.content,
            'timestamp': str(message.timestamp),
            'msg_type' : message.file_type
        }
                    


    commands = {
        'fetch_messages':fetch_messages,
        'new_message' : new_message
     }
    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # print(self.channel_name)
        # print('layer...',self.channel_layer)
        # print('groupname....',self.room_group_name)
        # print(self.room_name)
        # print(self.scope["user"])
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)

    def send_chat_message(self,message):    
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
                
            }
        )

    def send_message(self,message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

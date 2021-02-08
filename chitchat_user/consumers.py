import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message,OneToOneChat,UserDetails
from django.contrib.auth import get_user_model
import base64
from django.core.files.base import ContentFile

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    
    def fetch_messages(self, data):
        # author = data['from']
        # logged_user = self.scope["user"]
        # print('authorrrr',author)
        # print('loggedd userrr',logged_user)
        # if  author == logged_user :
        
            print('fetch data ....',self.room_name)
            messages = Message.objects.filter(room_name = self.room_name).order_by('-timestamp').all()[:10]
            content = {
                'command':'messages',
                'messages': self.messages_to_json(messages)
            }
            # print('contentttt',content)

            self.send_message(content)

    def new_message(self, data):
        author = data['from']
        logged_user =self.scope["user"]
        print('typeeeeee',data['msg_type'])
        file_type = data['msg_type'][:5]
        print(file_type)
        print(self.room_name)
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
            userdetail = UserDetails.objects.get(user = logged_user )
            author_user = User.objects.filter(username = author)[0]
            message = Message.objects.create(author = author_user,chat_icon = userdetail.ImageURL,content=content_msg,file_uploaded=file_decoded,file_type=file_type,room_name=self.room_name) 

        else:
            content_msg = data['message']
            msg_type = data['msg_type']
            userdetail = UserDetails.objects.get(user = logged_user )
            author_user = User.objects.filter(username = author)[0]
            message = Message.objects.create(author = author_user,chat_icon = userdetail.ImageURL,content=content_msg,file_type=msg_type,room_name=self.room_name)   
     
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
            print( message.chat_icon)
            return{
                'author': message.author.username,
                'content':message.file_uploaded.url,
                'timestamp': str(message.timestamp),
                'msg_type' : message.file_type,
                'user_image' : message.chat_icon
            }
        else:
            print( message.chat_icon)
            return{
            'author': message.author.username,
            'content':message.content,
            'timestamp': str(message.timestamp),
            'msg_type' : message.file_type,
            'user_image' : message.chat_icon
        }
                    


    commands = {
        'fetch_messages':fetch_messages,
        'new_message' : new_message
     }
    
    def connect(self):
        print('dshbbbbbbbbbbbjdbbdd ') 

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # print(self.channel_name)
        # print('layer...',self.channel_layer)
        # print('groupname....',self.room_group_name)
        one_to_one = OneToOneChat.objects.get(room_name = self.room_name)
        print(one_to_one.user_1,one_to_one.user_2)
        print(self.room_name)
        print(self.scope["user"])
        if one_to_one.user_1 ==  str(self.scope["user"]) or one_to_one.user_2 ==  str(self.scope["user"])  :
            print('authenticated user')
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

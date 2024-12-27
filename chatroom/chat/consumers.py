import json
import base64
import secrets
from datetime import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from accounts.models import Account
from accounts.serializers import AccountSerializer

from friends.models import FriendRequest, FriendsList, FriendshipStatus
from friends.serializers import FriendRequestSerializer, FriendsListSerializer, NewFriendSerializer

from .models import Room, RoomInvite, Message
from .serializers import RoomSerializer, MessageSerializer, RoomInviteSerializer

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action_map = {
            'get.all.rooms': self.get_all_rooms,
            'get.all.users': self.get_all_users,
            'get.friends.list': self.get_friend_list,
            'get.friend.request': self.get_friend_requests,
            'get.room.invite': self.get_room_invite,
            'send.friend.request': self.send_friend_request,
            'agree.friend.request': self.agree_friend_request,
            'reject.friend.request': self.reject_friend_request,
            'get.or.create.room': self.get_or_create_room,
            'send.message': self.send_message,
            'get.all.message': self.get_all_message,
            'block.friend': self.block_friend,
            'unblock.friend': self.unblock_friend,
            'remove.friend': self.remove_friend,
            'quit.chat': self.quit_chat,
            'create.group.chat': self.create_group_chat,
            'invite.join.group.chat': self.invite_join_group_chat,
            'agree.invite': self.agree_invite,
            'reject.invite': self.reject_invite,
            'update.user.info': self.update_user_info,
            'remove.avatar': self.remove_avatar
        }

    def connect(self):
        try:
            token_error = self.scope.get('error')
            if token_error:
                self.close_with_token_expired(token_error)
                return

            self.user = self.scope.get('user')
            if self.user:
                self.id = str(self.user.id)
        except Exception:
            return
        else:
            async_to_sync(self.channel_layer.group_add)(self.id, self.channel_name)
            self.accept()


    def close_with_token_expired(self, msg):
        self.accept()
        self.send(text_data=json.dumps({
            "action": "token.expired",
            "data": msg,
        }))
        self.close(code=4000)


    def disconnect(self, code):
        if hasattr(self, 'id'):
            async_to_sync(self.channel_layer.group_discard)(self.id, self.channel_name)

    
    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        now = datetime.now()
        if (now > self.scope['exp_time']):
            self.send(text_data=json.dumps({
                "action": "token.expired",
                "data": '連線逾時，請重新登入!',
            }))
            self.close(code=4000)
            return
        if action in self.action_map:
            self.action_map[action](data)
        else:
            self.send(text_data=json.dumps({
                "action": "unknow.action",
                "data": 'Unknown action!',
            }))
            self.close(code=4001)
            return
        

    def get_all_users(self, data):
        user = Account.objects.exclude(id=self.id).exclude(username='admin')
        serializers = AccountSerializer(user, many=True)
        self.send_group(self.id, 'get.all.users', serializers.data)


    def get_friend_list(self, data):
        friends_list = FriendsList.objects.get(user=self.user)
        serializer = FriendsListSerializer(friends_list)
        self.send_group(self.id, 'get.friends.list', serializer.data)

        
    def get_friend_requests(self, data):
        receiver_list = FriendRequest.objects.filter(receiver=self.user, is_active=True)
        sender_list = FriendRequest.objects.filter(sender=self.user, is_active=True)
        who_sent_me_serializers = FriendRequestSerializer(receiver_list, many=True, context={'just_get_sender': True})
        i_sent_who_serializers = FriendRequestSerializer(sender_list, many=True, context={'just_get_receiver': True})
        response_data = {
            'receivedRequests': who_sent_me_serializers.data,
            'sentRequests': i_sent_who_serializers.data,
        }
        self.send_group(self.id, 'get.friend.request', response_data)

    
    def get_room_invite(self, data):
        invites = RoomInvite.objects.filter(receiver=self.user.id)
        serializers = RoomInviteSerializer(invites, many=True)
        self.send_group(self.id, 'get.room.invite', serializers.data)
        

    
    def send_friend_request(self, data):
        id = data['receiver']
        receiver = User.objects.get(id=id)
        req, _= FriendRequest.objects.get_or_create(
            sender = self.user,
            receiver = receiver
        )
        who_sent_me_serializer = FriendRequestSerializer(req, context={'just_get_sender': True})
        i_sent_who_serializer = FriendRequestSerializer(req, context={'just_get_receiver': True})
        try:
            self.send_group(self.id, 'send.friend.request', {'sentRequests': i_sent_who_serializer.data })
            self.send_group(id, 'send.friend.request', {'receivedRequests': who_sent_me_serializer.data })
        except Exception as e:
            print(f"Error in send_group method: {e}", flush=True)


    def agree_friend_request(self, data):
        request = data['request']
        request_id = request['id']
        friend_request = FriendRequest.objects.get(id=request_id)
        senderId = str(friend_request.sender.id)
        receiverId = str(friend_request.receiver.id)
        
        sender_friend_list = FriendsList.objects.get(user=friend_request.sender)
        receiver_friend_list = FriendsList.objects.get(user=friend_request.receiver)
        try:
            receiver_friend_list.add_friend(friend_request.sender)
        except ValueError as e:
            self.send_group(receiverId, 'agree.friend.request', {'error': str(e)})
            return
        else:
            sender_friend_list.add_friend(friend_request.receiver)
            friend_request.delete()

            sender_friend_serializer = NewFriendSerializer(sender_friend_list, context={'id': receiverId})
            receiver_friend_serializer = NewFriendSerializer(receiver_friend_list, context={'id': senderId})

            for_sender_data = {
                'request': request_id,
                'friend': sender_friend_serializer.data['friend']
            }

            for_receiver_data = {
                'request': request_id,
                'friend': receiver_friend_serializer.data['friend']
            }

            self.send_group(senderId, 'agree.friend.request', for_sender_data)
            self.send_group(receiverId, 'agree.friend.request', for_receiver_data)
        


    def reject_friend_request(self, data):
        '''
        self.id是拒絕或取消的用戶
        有2種情況,self.id寄給誰邀請 或者 誰寄給self.id邀請

        '''
        request = data['request']
        request_id = request['id']
        sender = request.get('sender')
        receiver = request.get('receiver')
        ## 誰寄給self.id邀請
        if sender:
            sender = sender['id']

        ## self.id寄給誰邀請
        if receiver:
            receiver = receiver['id']

        friend_request = FriendRequest.objects.get(id=request_id)
        friend_request.delete()
        self.send_group(self.id, 'reject.friend.request', {'request':request_id, 'reject': True})
        self.send_group(receiver if receiver else sender, 'reject.friend.request', {'request':request_id})


    def get_all_rooms(self, data):
        rooms = Room.objects.get_all_rooms(self.user)
        serializers = RoomSerializer(rooms, many=True, context={'request': self.user})
        self.send_group(self.id, 'get.all.rooms', serializers.data)


    def get_or_create_room(self, data):
        id = data['receiver']
        receiver = Account.objects.get(id=id)
        room = Room.objects.get_or_create_personal_room(self.user, receiver)
        serializer = RoomSerializer(room, context={'request': self.user})
        self.send_group(self.id, 'get.or.create.room', serializer.data)


    def send_message(self, msg_data):
        data = msg_data['data']
        room = Room.objects.prefetch_related('users').get(id=data['room'])
        imgDict = data['img']
        if imgDict and imgDict['format']:
            file_str, file_ext = imgDict['data'],imgDict['format']
            img_data = ContentFile(
                base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
            )
            message = Message.objects.create(room=room, sender=self.user, content=data['message'], img=img_data)
        else:
            message = Message.objects.create(room=room, sender=self.user, content=data['message'])
        
        msg_serializer = MessageSerializer(message)
        for user in room.users.all():
            room_serializer = RoomSerializer(room, context={'request': user})
            self.send_group(str(user.id), 'send.message', {'message':msg_serializer.data, 'room': room_serializer.data})


    def get_all_message(self, data):
        id = data['room']
        room = Room.objects.get(id=id)
        messages = room.messages.select_related('sender').all()
        serializers = MessageSerializer(messages, many=True)
        self.send_group(self.id, 'get.all.message', serializers.data)


    def block_friend(self, data):
        id = data['receiver']
        friend_list = FriendsList.objects.get(user=self.user)
        friend_list.block_user(id)
        target_user_update_data = {
            'id': self.id,
            'AmIBlocked': True,
            'sender': False,
        }
        self.send_group(self.id, 'block.friend', { 'id': id, 'sender': True })
        self.send_group(id, 'block.friend', target_user_update_data)


    def unblock_friend(self, data):
        id = data['receiver']
        friend_list = FriendsList.objects.get(user=self.user)
        friend_list.unblock_user(id)
        my_friend_ship = FriendshipStatus.objects.get(user__id=self.id, friend__id=id)
        target_friend_ship = FriendshipStatus.objects.get(user__id=id, friend__id=self.id)

        target_user_update_data = {
            'id': self.id,
            'AmIBlocked': my_friend_ship.is_blocked,
            'sender': False
        }

        new_friend_data = {
            'friend': {
                **AccountSerializer(my_friend_ship.friend).data,
                'AmIBlocked': target_friend_ship.is_blocked,
                'IsFriend': target_friend_ship.is_friend
            },
            'sender': True
        }
        self.send_group(self.id, 'unblock.friend', new_friend_data)
        self.send_group(id, 'unblock.friend', target_user_update_data)


    def remove_friend(self, data):
        id = data['receiver']
        target_user = User.objects.get(id=id)
        target_user_list = FriendsList.objects.get(user=target_user)
        target_user_list.remove_user(self.user)

        friend_list = FriendsList.objects.get(user=self.user)
        friend_list.remove_user(target_user)

        self.send_group(self.id, 'remove.friend', { 'id': id })
        self.send_group(id, 'remove.friend', { 'id': self.id })


    def quit_chat(self, data):
        id = data['room']
        room = Room.objects.prefetch_related('users').get(id=id)
        system_message = Room.objects.quit_out_group_user(self.id, id)
        try:
            updete_room = Room.objects.get(id=id)
            room_serializer = RoomSerializer(updete_room, context={'request': self.user})
            if system_message:
                messate_serializer = MessageSerializer(system_message)
                for user in room.users.exclude(id=self.id):
                    data = {
                        'userId': self.id,
                        'message': messate_serializer.data,
                        'updateRoom': room_serializer.data
                    }
                    self.send_group(str(user.id), 'quit.chat', data)
        except:
            pass

        self.send_group(self.id, 'quit.chat', {'roomId': id})

        
    def create_group_chat(self, data):
        name = data['name']
        users = data['users']
        room = Room.objects.create_group_thread(name, self.user)

        for user in users:
            invitee = User.objects.get(id=user['id'])
            invite = RoomInvite.objects.create(room=room, sender=self.user, receiver=invitee)
            serializer = RoomInviteSerializer(invite)
            self.send_group(user['id'], 'create.group.chat', {'roomInvite' : serializer.data})
            
        serializer = RoomSerializer(room, context={'request': self.user})
        self.send_group(self.id, 'create.group.chat', {'room' : serializer.data})

    
    def invite_join_group_chat(self, data):
        id = data['id']
        users = data['users']
        room = Room.objects.get(id=id)

        for user in users:
            invitee = User.objects.get(id=user['id'])
            invite = RoomInvite.objects.create(room=room, sender=self.user, receiver=invitee)
            serializer = RoomInviteSerializer(invite)
            self.send_group(user['id'], 'invite.join.group.chat', {'roomInvite' : serializer.data})

        self.send_group(self.id, 'invite.join.group.chat', {'message' : '成功寄送邀請!'})


    def agree_invite(self, data):
        id = data['invite']
        try:
            invite = RoomInvite.objects.get(id=id)
            msg = invite.join_room(self.user, invite.room)
            msg_serializer = MessageSerializer(msg)
            room_serializer = RoomSerializer(invite.room, context={'request': self.user})
            for user in invite.room.users.all():
                self.send_group(str(user.id), 'agree.invite', {'room' : room_serializer.data, 'message': msg_serializer.data})
            invite.delete()
            self.send_group(self.id, 'agree.invite', {'room' : room_serializer.data, 'id': id})
        except:
            self.send_group(self.id, 'agree.invite', {'error': id})


    def reject_invite(self, data):
        id = data['invite']
        try:
            invite = RoomInvite.objects.get(id=id)
            invite.delete()
            self.send_group(self.id, 'reject.invite', {'id': id})
        except:
            self.send_group(self.id, 'reject.invite', {'id': id})


    def update_user_info(self, update_data):
        data = update_data['updateData']
        user = self.user
        user.username = data['username']
        user.profile = data['profile']
        if data['avatar']:
            file_str, file_ext = data['avatar']['data'],data['avatar']['format']
            img_data = ContentFile(
                base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
            )
            user.avatar = img_data
        user.save()
        update_user = AccountSerializer(user).data
        data = {
            'message': '更新成功!',
            'user': update_user
        }
        friend_data = {
            'friend': update_user
        }
        self.send_group(self.id, 'update.user.info', data)
        for friend in user.friend_list.friends.all():
            self.send_group(str(friend.id), 'update.user.info', friend_data)

    def remove_avatar(self, data):
        self.user.avatar = ''
        self.user.save()
        user_info = AccountSerializer(self.user).data
        data = {
            'message': '成功移除!',
            'avatar': user_info['avatar']
        }
        self.send_group(self.id, 'remove.avatar', data)
        for friend in self.user.friend_list.friends.all():
            self.send_group(str(friend.id), 'update.user.info', { 'friend': user_info})



    ## -------------------------------
    ## tools
    ## -------------------------------
    def send_group(self, group, action, data):
        try:
            async_to_sync(self.channel_layer.group_send)(
                group, {   
                    'type': 'group_message',
                    'action': action,
                    'data': data,
                }
            )
        except Exception as e:
            print(f"Error in send_group method. Action: {action}, Error: {e}", flush=True)

    def group_message(self, event):
        action = event['action']
        data = event['data']
        
        self.send(text_data=json.dumps({
            'action': action,
            'data': data
        }))
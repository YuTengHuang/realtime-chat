from rest_framework import serializers
from .models import Room, Message, RoomInvite



class RoomSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_type', 'users']

    def get_users(self, obj):
        current_user = self.context['request']
        another_user = obj.users.exclude(id=current_user.id).first()
        if obj.room_type == 'personal':
            return {
                'sender': self.get_sender(current_user),
                'receiver': self.get_receiver(another_user)
            }
        
        elif obj.room_type == 'group':
            return [
                {
                    'id': str(user.id),
                    'username': user.username,
                    'avatar': user.avatar.url
                } for user in obj.users.all()
            ] 

    def get_sender(self, user):
        return {
            'id': str(user.id),
            'username': user.username,
            'avatar': user.avatar.url
        }

    def get_receiver(self, user):
        return {
            'id': str(user.id),
            'username': user.username,
            'avatar': user.avatar.url
        }
    
class MessageSerializer(serializers.ModelSerializer):
    room = serializers.CharField(source='room.id')
    sender = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format='%Y/%m/%d-%H:%M', read_only=True)

    class Meta:
        model = Message
        fields = ['room', 'sender', 'content', 'date', 'img', 'is_system']
    

    def get_sender(self, obj):
        if obj.is_system:
            return None
        
        sender = obj.sender
        return{
            'id': str(sender.id),
            'username': sender.username,
            'avatar': sender.avatar.url
        }
    

class RoomInviteSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(format='%Y/%m/%d-%H:%M', read_only=True)

    class Meta:
        model = RoomInvite
        fields = ['id', 'room', 'sender', 'timestamp']

    def get_id(self, obj):
        return str(obj.id)
    
    def get_room(self, obj):
        return str(obj.room.name)
    
    def get_sender(self, obj):
        return str(obj.sender.username)
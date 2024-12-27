from rest_framework import serializers
from accounts.serializers import AccountSerializer
from .models import FriendsList, FriendRequest, FriendshipStatus
from django.contrib.auth import get_user_model
User = get_user_model()
            

class FriendsListSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()
    blocked = serializers.SerializerMethodField()
    class Meta:
        model = FriendsList
        fields = ['friends', 'blocked']

    def get_friends(self, obj):
        friend_ids = obj.friends.values_list('id', flat=True)
        friendship_status = FriendshipStatus.objects.filter(user=obj.user, friend__id__in=friend_ids)
        return [
            {  
                **AccountSerializer(friend_status.friend).data,
                'AmIBlocked': friend_status.is_blocked,
                'IsFriend': friend_status.is_friend
            } for friend_status  in friendship_status
        ]

    def get_blocked(self, obj):
        return AccountSerializer(obj.blocked.all(), many=True).data
    
    
class NewFriendSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()
    class Meta:
        model = FriendsList
        fields = ['friend']

    def get_friend(self, obj):
        friend_id = self.context.get('id', None)
        friend_ship = FriendshipStatus.objects.get(user=obj.user, friend__id=friend_id)
        if friend_ship:
            return {  
                    **AccountSerializer(friend_ship.friend).data,
                    'AmIBlocked': friend_ship.is_blocked,
                    'IsFriend': friend_ship.is_friend
                }
            
            
class FriendRequestSerializer(serializers.ModelSerializer):
    sender = AccountSerializer()
    receiver = AccountSerializer()
    timestamp = serializers.DateTimeField(format='%Y/%m/%d-%H:%M', read_only=True)
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'timestamp']
    
    def to_representation(self, obj):
        data = super().to_representation(obj)
        if self.context.get('just_get_sender', False):
            data.pop('receiver', None)
        elif self.context.get('just_get_receiver', False):
            data.pop('sender', None)
        return data
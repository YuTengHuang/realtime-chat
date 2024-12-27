from django.db import models
from django.db.models import Count
from storages.backends.s3boto3 import S3Boto3Storage
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from uuid import uuid4
User = get_user_model()

class RoomManger(models.Manager):

    def get_or_create_personal_room(self, user1, user2):
        room = Room.objects.annotate(user_count=Count('users')
        ).filter(user_count=2, users=user1
        ).filter(users=user2)

        if room.exists():
            return room.first()
        else:
            room = self.create(room_type='personal')
            room.users.add(user1, user2)
            return room
    
    def create_group_thread(self, name, creator):
        room = self.create(room_type='group', name=name)
        room.users.add(creator)
        return room
    
    def quit_out_group_user(self, userId, roomId):
        try:
            room = Room.objects.get(id=roomId)
            user = User.objects.get(id=userId)
            room.users.remove(user)
            if room.users.count() == 0:
                room.delete()
                return True
            return Message.objects.create(room=room, content=f'{user.username} 退出群組', is_system=True)
        except User.DoesNotExist:
            return False
        except Room.DoesNotExist:
            return False
        

    def get_all_rooms(self, user):
        return self.get_queryset().filter(users__in=[user]).distinct()

class BaseChatModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Room(BaseChatModel):

    ROOM_TYPE = {
        'personal': 'Personal',
        'group' : 'Group'
    }

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE, default='personal')
    users = models.ManyToManyField(User)

    objects = RoomManger()

    def __str__(self):
        if self.room_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}---{self.id}'
        return self.name
    
class RoomInvite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='invites')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_invite")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_invite")
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.room.id} -> {self.receiver.username} -- {self.id}'
    
    def join_room(self, target_user, room):
        self.room.users.add(target_user.id)
        return Message.objects.create(room=room, content=f'{target_user.username} 加入群組', is_system=True)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='my_messages', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(blank=True)
    img = models.ImageField(blank=True, upload_to='message/', storage=S3Boto3Storage)
    date = models.DateTimeField(auto_now_add=True)
    is_system = models.BooleanField(default=False)

    def __str__(self):
        return f'Room - {self.room} - {self.date}'


@receiver(post_delete, sender=Message)
def delete_image_from_s3(instance, **kwargs):
    if instance.img:
        storage = instance.img.storage
        storage.delete(instance.img.name)

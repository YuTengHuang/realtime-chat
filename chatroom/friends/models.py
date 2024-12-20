from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model

User = get_user_model()

class FriendsList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='friend_list')
    friends = models.ManyToManyField(User, blank=True, related_name='friends', editable=False)
    blocked = models.ManyToManyField(User, blank=True, related_name='blocked_users', editable=False)
    
    def add_friend(self, target_user):
        if target_user.id == self.user:
            raise ValueError({'error': '無法添加自己為好友'})
        
        if self.blocked.filter(id=target_user.id).exists():
            raise ValueError(f'{target_user.username} 已在黑名單內，無法添加好友')
        self.friends.add(target_user)
        FriendshipStatus.objects.update_or_create(
            user=self.user,
            friend=target_user,
            defaults={'is_friend': True, 'is_blocked': False}
        )


    def remove_user(self, target_user):
        self.friends.remove(target_user)
        FriendshipStatus.objects.update_or_create(
            user=self.user,
            friend=target_user,
            defaults={'is_friend': False}
        )

    def block_user(self, target_user):
        self.friends.remove(target_user)
        self.blocked.add(target_user)
        FriendshipStatus.objects.update_or_create(
            user=self.user,
            friend=target_user,
            defaults={'is_friend': False, 'is_blocked': True}
        )

    def unblock_user(self, target_user):
        status = FriendshipStatus.objects.get(user=target_user, friend=self.user)
        if status.is_friend == False and status.is_blocked == False:
            self.blocked.remove(target_user)
            self.friends.add(target_user)
            FriendshipStatus.objects.update_or_create(
                user=self.user,
                friend=target_user,
                defaults={'is_friend': False, 'is_blocked': False}
            )

        else:
            self.blocked.remove(target_user)
            self.friends.add(target_user)
            FriendshipStatus.objects.update_or_create(
                user=self.user,
                friend=target_user,
                defaults={'is_friend': True, 'is_blocked': False}
            )


class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class FriendshipStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_status')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    is_friend = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user} - {self.friend} -- Friend: {self.is_friend} Blocked: {self.is_blocked}"

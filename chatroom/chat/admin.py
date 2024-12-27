from django.contrib import admin
from .models import Room, RoomInvite, Message


admin.site.register(Room)
admin.site.register(RoomInvite)
admin.site.register(Message)
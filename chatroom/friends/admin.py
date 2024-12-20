from django.contrib import admin
from django.utils.html import format_html
from .models import FriendsList, FriendRequest, FriendshipStatus

class FriendsListAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Friends', {'fields': ('formatted_friends',)}),
        ('Blocked', {'fields': ('formatted_blocked',)}),
    )

    list_display = ('user', 'user_username', 'user_id')
    readonly_fields = ('user', 'formatted_friends', 'formatted_blocked')
    search_fields = ('user__username', 'user__id')

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = 'User ID'

    def formatted_friends(self, obj):
        return format_html("<br/>".join([friend.username for friend in obj.friends.all()]))
    formatted_friends.short_description = 'Friends'

    def formatted_blocked(self, obj):
        return format_html("<br/>".join([blocked_user.username for blocked_user in obj.blocked.all()]))
    formatted_blocked.short_description = 'Blocked'

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'timestamp',)
    ordering = ('-timestamp',)


admin.site.register(FriendsList, FriendsListAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(FriendshipStatus)
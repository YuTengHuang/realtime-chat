from django.urls import path
from .views import FriendRequestView, FriendsListView, BlockUserView

urlpatterns = [
    path('friendRequest/', FriendRequestView.as_view(), name='friend_request'),
    path('friendList/', FriendsListView.as_view(), name='friendList'),
    path('friendRequest/<uuid:id>/', FriendRequestView.as_view(), name='friend_request'),
    path('friendList/<uuid:id>/', FriendsListView.as_view(), name='friendList'),
    path('blockUser/<uuid:id>/', BlockUserView.as_view(), name='blockUser'),
]
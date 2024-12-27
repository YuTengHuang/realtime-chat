from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import FriendsList, FriendRequest
from .serializers import FriendsListSerializer, FriendRequestSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class FriendsListView(GenericAPIView):
    serializer_class = FriendsListSerializer

    def get_object(self, user):
        return FriendsList.objects.get(user=user)

    def get(self, request):
        friends_list = self.get_object(request.user)
        serializer = self.serializer_class(friends_list)
        return Response(serializer.data)

    def delete(self, request, id):
        friends_list = self.get_object(request.user)
        target_user = User.objects.get(id=id)
        friends_list.remove_friend(target_user)
        return Response({'message': '好友刪除成功'}, status=status.HTTP_200_OK)

class BlockUserView(GenericAPIView):
    serializer_class = FriendsListSerializer

    def post(self, request, id):
        friends_list = FriendsList.objects.get(user=request.user)
        target_user = User.objects.get(id=id)
        friends_list.block_user(target_user)
        return Response({'message': '使用者已封鎖'}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        friends_list = FriendsList.objects.get(user=request.user)
        target_user = User.objects.get(id=id)
        friends_list.unblock_user(target_user)
        return Response({'message': '使用者已解除封鎖'}, status=status.HTTP_200_OK)

class FriendRequestView(GenericAPIView):
    serializer_class = FriendRequestSerializer

    def get(self, request):
        receiver_list = FriendRequest.objects.filter(receiver=request.user, is_active=True)
        sender_list = FriendRequest.objects.filter(sender=request.user, is_active=True)
        receiver_serializer = self.serializer_class(receiver_list, many=True)
        sender_serializer = self.serializer_class(sender_list, many=True)
        response_data = {
            'receivedRequests': receiver_serializer.data,
            'sentRequests': sender_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, id):
        if request.user.id == id:
            return Response({'message': '不能對自己發送請求!'}, status=status.HTTP_200_OK)                
        serializer = self.serializer_class(data={
            'sender': request.user.id,
            'receiver': id
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        friend_request = FriendRequest.objects.get(id=id)
        serializer = self.serializer_class(friend_request)
        if request.data == 'yes':
            response = serializer.accept(friend_request)
        else:
            response = serializer.decline(friend_request)
        return Response(response, status=status.HTTP_200_OK)
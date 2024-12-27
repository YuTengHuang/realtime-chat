from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer, AccountSerializer
from .models import Account


class SignupView(GenericAPIView):
    permission_classes = []
    authentication_classes=[]
    serializer_class = SignUpSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': '註冊成功',
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetAllAccountView(GenericAPIView):
    serializer_class = AccountSerializer
    def get(self, request):
        cur_user = request.user
        user = Account.objects.exclude(id=cur_user.id).exclude(username='admin')
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
from .models import Account
from friends.models import FriendsList

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate


class SignUpSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=45)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
    confirmPassword = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model = Account
        fields = [
            "email", 
            "username", 
            "password",
            "confirmPassword"
        ]
    
    def validate(self, attrs):
        email_exists = Account.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise serializers.ValidationError("信箱已被註冊!")
        
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError("密碼不相符!")
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop("confirmPassword")
        user = Account.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        FriendsList.objects.create(user=user)
        return user
    
''' ----------------------------------------------------------------- '''

class CustomTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if user is None:
            if not Account.objects.filter(email=email).exists():
                raise serializers.ValidationError("用戶不存在!")
            else:
                raise serializers.ValidationError("密碼錯誤!")
        data = super().validate(attrs)
        data.update({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "avatar": user.avatar.url,
            "profile": '' if user.profile == None else user.profile,
            "is_default": user.is_default,
        })
        return data


class LoginSerializer(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            msg = e.detail['non_field_errors'][0]
            return Response({'detail': msg}, status=status.HTTP_401_UNAUTHORIZED)
        
        response_data = {
            'user':  serializer.validated_data
        }
        return Response(response_data, status=status.HTTP_200_OK)

''' ----------------------------------------------------------------- '''

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ['id', 'username', 'avatar', 'profile']
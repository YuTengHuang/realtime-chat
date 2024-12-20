from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .serializers import SignUpSerializer

User = get_user_model()

class CustomUserModelTes(TestCase):
    '''
    Admin管理頁面
    自定義的CustomUserManager新增超級用戶及普通用戶測試
    
    '''

    def test_create_user(self):
        user = User.objects.create_user(
            email = 'test@test.com',
            username = 'test',
            password = 'test123456789'
        )

        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.username, 'test')
        self.assertTrue(user.check_password('test123456789'))


    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email = 'super@super.com',
            username = 'super',
            password = 'super123456789'
        )

        self.assertEqual(user.email, 'super@super.com')
        self.assertEqual(user.username, 'super')
        self.assertTrue(user.check_password('super123456789'))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class SignUpSerializerTests(TestCase):

    '''
    註冊序列化器測試

    '''

    def test_valid_data(self):
        valid_data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'test123456789',
            'confirmPassword': 'test123456789'
        }
        serializer = SignUpSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_passwords_must_match(self):
        invalid_data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'test123456789',
            'confirmPassword': 'asdasdsadsdadasds'
        }
        serializer = SignUpSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class LoginSerializerTest(APITestCase):
    '''
    登入並獲取token以及用戶資料測試
    '''

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test123456789',
            username='testuser',
        )

    def test_login_success(self):
        valid_data = {
            'email': 'test@test.com',
            'password': 'test123456789',
        }
        
        response = self.client.post(reverse('login'), valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('access', response.data['user'])
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.user.email)

    def test_login_invalid_email(self):
        invalid_data = {
            'email': 'invalid@test.com',
            'password': 'test123456789',
        }
        
        response = self.client.post(reverse('login'), invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "用戶不存在!")

    def test_login_invalid_password(self):
        invalid_data = {
            'email': 'test@test.com',
            'password': 'wrongpassword',
        }

        response = self.client.post(reverse('login'), invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "密碼錯誤!")
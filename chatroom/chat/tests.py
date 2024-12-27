from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Room

User = get_user_model()

class ThreadManagerTests(TestCase):
    
    def setUp(self):
        # 創建測試用戶
        self.user1 = User.objects.create_user(username='user1', password='password1', email='user@user.com1')
        self.user2 = User.objects.create_user(username='user2', password='password2', email='user@user.com2')
        self.user3 = User.objects.create_user(username='user3', password='password3', email='user@user.com3')

    def test_get_or_create_personal_room_existing(self):
        # 手動創建一個聊天室
        room = Room.objects.create(room_type='personal')
        room.users.add(self.user1, self.user2)

        # 查找聊天室
        found_room = Room.objects.get_or_create_personal_room(self.user1, self.user2)

        self.assertEqual(found_room, room)

    def test_get_or_create_personal_room_new(self):
        # 創建聊天室
        found_room = Room.objects.get_or_create_personal_room(self.user1, self.user2)

        # 創建一個新的聊天室
        self.assertIsNotNone(found_room)
        self.assertEqual(found_room.room_type, 'personal')
        self.assertIn(self.user1, found_room.users.all())
        self.assertIn(self.user2, found_room.users.all())

    def test_get_or_create_personal_room_with_different_users(self):
        # 測試不同用戶查找不同聊天室
        found_room = Room.objects.get_or_create_personal_room(self.user1, self.user3)

        self.assertIsNotNone(found_room)
        self.assertEqual(found_room.room_type, 'personal')
        self.assertIn(self.user1, found_room.users.all())
        self.assertIn(self.user3, found_room.users.all())

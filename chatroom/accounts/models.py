from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from uuid import uuid4

class CustomUserManager(UserManager):

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("請輸入電子郵件!")

        email = self.normalize_email(email)
        username = username.strip()

        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):

        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):

        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, username, password, **extra_fields)
    
class Account(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=45, unique=True)
    username = models.CharField(max_length=45)
    register = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(
        max_length=255, upload_to='avatar/', blank=True, null=True, 
        default='avatar/default.svg',
        storage=S3Boto3Storage
    )
    profile = models.CharField(max_length=50, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('-register',)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):

        if not self.avatar:
            self.avatar = 'avatar/default.svg'

        try:
            user = Account.objects.get(id=self.id)
            if user.avatar != self.avatar:
                if 'avatar/default.svg'not in user.avatar.url:
                    user.avatar.delete(save=False)
        except ObjectDoesNotExist: pass

        super(Account, self).save(*args, **kwargs)
    
    def get_username(self):
        return self.username
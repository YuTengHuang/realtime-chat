from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2",)

    def save(self, *args, **kwargs):
        user = super(CustomUserCreationForm, self).save(*args, **kwargs)
        user.email = self.cleaned_data.get('email', user.email)
        user.username = self.cleaned_data.get('username', user.username)
        return user
    

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Account
        fields = '__all__'

    def save(self, *args, **kwargs):
        user = super(CustomUserChangeForm, self).save(*args, **kwargs)
        user.email = self.cleaned_data.get('email', user.email)
        user.username = self.cleaned_data.get('username', user.username)
        return user
from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = Account

    ''' 皆可用 = ()空值,代表全預設內容 '''
    fieldsets = (
        (None, {'fields': ('id', 'email', 'username', 'password')}),  
        ('Personal Info', {'fields': ('avatar', 'profile', 'is_default')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'register')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', )}
        ),
    )

    readonly_fields = ('id', 'password', 'register', 'last_login') 

    list_display = ('email', 'is_admin', 'register')
    list_filter = ('is_admin', )
    search_fields = ('email', 'username')
    ordering = ('-register',)

admin.site.register(Account, CustomUserAdmin)
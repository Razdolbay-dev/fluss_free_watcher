from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *

# Кастомная модель пользователя

from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'ip_address', 'dvr','update_cam')
    fieldsets = (
        (None, {'fields': ('username','email', 'ip_address', 'password', 'members')}),
        ('Привилегии', {'fields': ('is_staff','is_superuser','is_active','dvr','update_cam')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'members', 'password1', 'password2', 'is_staff','is_superuser', 'is_active','ip_address', 'dvr','update_cam')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.

admin.site.register(Cameras)
admin.site.register(CustomGroup)
admin.site.register(Storage)
admin.site.register(Settings)
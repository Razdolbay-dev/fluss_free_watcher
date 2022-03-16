from django import forms 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField

from .models import *

import urllib3

class CameraForm(forms.ModelForm):
    class Meta:
        model = Cameras
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class ConfigsForm(forms.ModelForm):
    class Meta:
        model = Configs
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class GroupForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username','password')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'members', 'ip_address', 'is_staff','is_superuser', 'is_active', 'dvr','update_cam')
        
class UpdatePassword(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('password1', 'password2')
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AddUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'ip_address', 'password')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# Custom User Model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        #fields = '__all__'
        fields = ('username', 'email', 'members', 'ip_address', 'is_staff','is_superuser', 'is_active', 'dvr','update_cam')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        #fields = '__all__'
        fields = ('username', 'email', 'password', 'members', 'ip_address', 'is_staff','is_superuser', 'is_active', 'dvr','update_cam')

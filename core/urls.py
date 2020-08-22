from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

from core import views
from .views import *

urlpatterns = [
    #path('delcam/<int:pk>', DelCamera.as_view(), name='delcam'),
    #path('', Home.as_view(), name='home'),
    #path('test/', views.home, name='homeles'),
    #path('auth', views.user_login, name='auth'),
    path('auth', views.HydraLoginView.as_view(), name='auth'),
    #path('register', views.RegisterUserView.as_view(), name='register_page'),
    path('', views.home, name='home'),
    path('detail/<str:slug>', DVR.as_view(), name='detail'),
    #Cameras
    path('cameras/', AddCamera.as_view(), name='cameras'),
    path('editcam/<str:slug>', UpdateCamera.as_view(), name='editcam'),
    path('delcam/<str:slug>', DelCamera.as_view(), name='delcam'),
    #Users
    #path('auth', views.login_page, name='auth'),
    path('logout', views.HydraLogout.as_view(), name='logout'),
    path('users/', views.AddUser.as_view(), name='users'),
    path('users/<int:pk>', UpdateUser.as_view(), name='update_usr_page'),
    path('users/<int:pk>', views.UpdatePass.as_view(), name='users'),
    path('delusr/<int:pk>', DelUser.as_view(), name='delusr'),
    #Groups
    path('groups/', AddGRP.as_view(), name='groups'),
    path('delgrp/<int:pk>', DelGRP.as_view(), name='delgrp'),
    path('editgrp/<int:pk>', UpdateGRP.as_view(), name='editgrp'),
    path('groups/<str:slug>', views.group_detail, name='group_page'),
    path('myhome/', myHome.as_view(), name='myhome'),
    path('myhome/<str:slug>', views.group_detail, name='myhome_page'),
    path('settings/<int:id>', Setting.as_view(), name='settings'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#if settings.DEBUG:
#    urlpatterns += [
#        url('media/', serve, {
#            'document_root': settings.MEDIA_ROOT,
#        }),
#    ]
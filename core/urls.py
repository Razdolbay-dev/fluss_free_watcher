from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

from core import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('public_all/', views.public_all, name='publics'),
    path('privat_all/', views.privat_all, name='privats'),
    #Cameras
    path('cam/<int:id>', views.Cam, name='cam'),
    path('detail/<int:id>', views.DVR, name='detail'),
    path('cameras/', AddCamera.as_view(), name='cameras'),
    path('editcam/<str:slug>', UpdateCamera.as_view(), name='editcam'),
    path('delcam/<str:slug>', DelCamera.as_view(), name='delcam'),
    #Users
    path('auth', views.HydraLoginView.as_view(), name='auth'),
    path('logout', views.HydraLogout.as_view(), name='logout'),
    path('users/', views.AddUser.as_view(), name='users'),
    path('users/<int:pk>', UpdateUser.as_view(), name='update_usr_page'),
    path('users/<int:pk>', views.UpdatePass.as_view(), name='users'),
    path('delusr/<int:pk>', DelUser.as_view(), name='delusr'),
    #Storage
    path('addstor/', AddStorage.as_view(), name='addstor'),
    path('delstor/<str:slug>', DelStorage.as_view(), name='delstor'),
    path('updstor/<str:slug>', UpdateStorage.as_view(), name='updstor'),
    #Groups
    path('groups/', AddGRP.as_view(), name='groups'),
    path('delgrp/<int:pk>', DelGRP.as_view(), name='delgrp'),
    path('editgrp/<int:pk>', UpdateGRP.as_view(), name='editgrp'),
    path('groups/<str:slug>', views.group_detail, name='group_page'),
    path('myhome/', myHome.as_view(), name='myhome'),
    path('myhome/<str:slug>', views.group_detail, name='myhome_page'),
    path('configs/', GetConfigs.as_view(), name='configs'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


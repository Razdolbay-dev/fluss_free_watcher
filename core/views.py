from pickle import NONE
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from ipaddress import IPv4Address
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from .models import *
from .forms import *

import transliterate
import requests
import os
import sys
import locale

#def handle_not_found(request,exceptions):
#    return render(request,'includes/404.html')

def page_not_found_view(request, exception):
    return render(request, 'includes/404.html', status=404)

# Create your views here.
def home(request):
    
    #list_cameras = Cameras.objects.all()
    list_cameras_pub = Cameras.objects.filter(camera_type='PU')[:8]
    list_cameras_priv = Cameras.objects.filter(camera_type='PR')[:8]
    print(list_cameras_pub)
    for obj in Configs.objects.filter(id=1):
        ip = obj.ip_addr
        port = obj.port_f
      
    context = {
        #'list_cameras':list_cameras,
        'list_cameras_pub':list_cameras_pub,
        'list_cameras_priv':list_cameras_priv,
        'obj':obj,
    }
    template = 'index.html'

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
# Забираем IP клиента и авторизируем если находим в базе
    if request.user == AnonymousUser():
        try:
            ip = get_client_ip(request)
            #print(ip)
            ip_chk = IPv4Address(str(ip))
            for obj2 in CustomUser.objects.all():
                ipindb = obj2.ip_address
                count = obj2.count_addr
                start_ip = IPv4Address(str(ipindb))
                end_ip = start_ip + int(count)
                if start_ip <= ip_chk <= end_ip:
                    ipforauth = str(start_ip)
                    user = CustomUser.objects.get(ip_address=ipforauth)
                    #print("ONO --> "+str(user))
                    login(request,user)
                else:
                    pass
            
            
            
            return render(request, template, context)
        except ObjectDoesNotExist:
            return render(request, template, context)
    else:
        return render(request, template, context)

def DVR(request,id):
    get_cameras = Cameras.objects.get(id=id)
    for obj in Configs.objects.filter(id=1):
        ip = obj.ip_addr
        port = obj.port_f
    context = {
        'get_cameras':get_cameras,
        'obj':obj
    }
    template = 'cameras/detail.html'

    return render(request, template, context)

def Cam(request,id):
    get_cameras = Cameras.objects.get(id=id)
    for obj in Configs.objects.filter(id=1):
        ip = obj.ip_addr
        port = obj.port_f
    context = {
        'get_cameras':get_cameras,
        'obj':obj
    }
    template = 'cameras/view.html'

    return render(request, template, context)


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False
    def form_valid(self,form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)

#Камеры 
class AddCamera(CustomSuccessMessageMixin, CreateView):
    model = Cameras
    template_name = 'cameras/cameras.html'
    form_class = CameraForm
    success_url = reverse_lazy('cameras')
    success_msg = 'Камера добавлена'
    def get_context_data(self,**kwargs):
        kwargs['list_cameras'] = Cameras.objects.all().order_by('title')
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            model = Storage, Configs
            for e in Configs.objects.filter(id=1):
                a = e.user_f
                b = e.pass_f
                c = e.port_f
            slug_1 = transliterate.translit(request.POST['title'].lower().replace(' ', ''), reversed=True)
            slug = slug_1.lower().replace('\'', '')
            url = request.POST['url']
            dvr = request.POST['dvr']
            auth =(str(a),str(b))
            title = transliterate.translit(request.POST['title'], reversed=True)
            try:
                path = Storage.objects.get(id=int(request.POST['storage']))
                data = '{"inputs":[{"url":"' + str(url) + '"}],"title":"' + str(slug) + '","dvr":{"dvr_limit":"'+ str(dvr) +'","root":"'+ str(path) +'"}}'
            except MultiValueDictKeyError:
                data = '{"inputs":[{"url":"' + str(url) + '"}],"title":"' + str(slug) + '"}'
            response = requests.put('http://127.0.0.1:'+ str(c) +'/flussonic/api/v3/streams/'+ str(slug) +'', data = data, auth=(str(a), str(b)), headers = {'content-type': 'application/json'})
            view = form.save()
            view.save()
            print(auth)
            return HttpResponseRedirect('/cameras')
        return render(request, self.template_name, {'form': form})

class UpdateCamera(CustomSuccessMessageMixin,View):
    model = Cameras
    template_name = 'cameras/cameras.html'
    form_class = CameraForm
    success_url = reverse_lazy('cameras')
    success_msg = 'Камера успешно обновлена'

    def get(self,request, slug):
        cam = Cameras.objects.get(slug__iexact=slug)
        form = CameraForm(instance=cam)
        template = 'cameras/editcam.html'
        context = {
            'form': form,
            'cam': cam
        }
        return render(request, template, context)

    def post(self, request, slug):
        cam = Cameras.objects.get(slug__iexact=slug)
        form = CameraForm(request.POST, instance=cam)
        if form.is_valid():
            model = Storage, Configs
            for e in Configs.objects.filter(id=1):
                a = e.user_f
                b = e.pass_f
                c = e.port_f
            name = transliterate.translit(request.POST['title'].lower().replace(' ', ''), reversed=True)
            url = request.POST['url']
            date = request.POST['dvr']
            title = transliterate.translit(request.POST['title'], reversed=True)

            auth = str(a),str(b)
            try:
                path = Storage.objects.get(id=int(request.POST['storage']))
                if date == "0":
                    data = '{"inputs":[{"url":"' + str(url) + '"}],"title":"' + str(slug) + '","dvr":{"dvr_limit":"0","dvr_offline":true,"root":"'+ str(path) +'"}}'
                else:
                    data = '{"inputs":[{"url":"' + str(url) + '"}],"title":"' + str(slug) + '","dvr":{"dvr_limit":"'+ str(date) +'","dvr_offline":false,"root":"'+ str(path) +'"}}'

            except MultiValueDictKeyError:
                data = '{"inputs":[{"url":"' + str(url) + '"}],"title":"' + str(slug) + '"}'
            
            response = requests.put('http://127.0.0.1:'+ str(c) +'/flussonic/api/v3/streams/'+ str(slug) +'', data = data, auth=(str(a), str(b)), headers = {'content-type': 'application/json'})
            form.save()

            return HttpResponseRedirect('/cameras')
        return render(request, self.template_name, success_msg, {'form': form})

class DelCamera(View):
    model = Cameras,Configs
    def get(self, request, slug):
        cam = Cameras.objects.get(slug__iexact=slug)
        template = 'cameras/delete_cam.html'
        context = {
            'cam': cam
        }
        return render(request, template, context)

    def post(self, request, slug):
        for e in Configs.objects.filter(id=1):
            a = e.user_f
            b = e.pass_f
            c = e.port_f
        cam = Cameras.objects.get(slug__iexact=slug)
        name = slug
        response = requests.delete('http://127.0.0.1:'+ str(c) +'/flussonic/api/v3/streams/' + str(name) +'', auth=(str(a), str(b)))
        cam.delete()

        return redirect(reverse('cameras'))

class myHome(ListView):
    model = Cameras
    template_name = 'cameras/myhome.html'
    context_object_name = 'list_cameras'

#Настройки
class GetConfigs(View):
    model = Configs, Storage
    def get(self,request, pk=id):
        setting = Configs.objects.get(id=1)
        storage = Storage.objects.all()
        form = ConfigsForm(instance=setting)
        template = 'settings.html'
        context = {
            'form': form,
            'setting': setting,
            'storage': storage
        }
        return render(request, template, context)

    def post(self, request, pk=id):
        setting = Configs.objects.get(id=1)
        form = ConfigsForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/configs/')
        return render(request, self.template_name, success_msg, {'form': form})

#Хранилища

class AddStorage(View):
    model = Storage
    def get(self,request):
        form = StorageForm()
        template = 'storage/add_stor.html'
        context = {
            'form': form
        }
        return render(request,template, context)
        
    def post(self, request):
        bound_form = StorageForm(request.POST)
        template = 'storage/add_stor.html'
        context = {
            'form': bound_form
        }
        if bound_form.is_valid():
            bound_form.save()
            return redirect(reverse('configs'))
        return render(request, template, context)

class DelStorage(View):
    model = Storage
    def get(self, request, slug):
        stor = Storage.objects.get(slug__iexact=slug)
        template = 'storage/del_stor.html'
        context = {
            'stor': stor
        }
        return render(request, template, context)

    def post(self, request, slug):
        stor = Storage.objects.get(slug__iexact=slug)
        stor.delete()

        return redirect(reverse('configs'))

class UpdateStorage(View):
    model = Storage
    template = 'storage/upd_stor.html'
    def get(self,request, slug):
        stor = Storage.objects.get(slug__iexact=slug)
        form = StorageForm(instance=stor)
        template = 'storage/upd_stor.html'
        context = {
            'form': form,
            'stor': stor
        }
        return render(request, template, context)

    def post(self, request, slug):
        stor = Storage.objects.get(slug__iexact=slug)
        form = StorageForm(request.POST, instance=stor)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/configs')
        return render(request, self.template_name, success_msg, {'form': form})

##Login/Logout пользователя
class HydraLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home')
    def get_success_url(self):
        return self.success_url

class HydraLogout(LogoutView):
    next_page = reverse_lazy('home')

#группы по анологии с тэгами

class DelGRP(DeleteView):
    model = CustomGroup
    template_name = 'groups/groups.html'
    success_url = reverse_lazy('groups')
    success_msg = 'Группа удалена'
    
    def post(self,request,*args,**kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

class AddGRP(CustomSuccessMessageMixin, CreateView):
    model = CustomGroup
    template_name = 'groups/groups.html'
    form_class = GroupForm
    success_url = reverse_lazy('groups')
    success_msg = 'Группа добавлена'
    def get_context_data(self,**kwargs):
        kwargs['list_groups'] = CustomGroup.objects.all().order_by('title')
        return super().get_context_data(**kwargs)

class UpdateGRP(CustomSuccessMessageMixin,UpdateView):
    model = CustomGroup
    template_name = 'groups/groups.html'
    form_class = GroupForm
    success_url = reverse_lazy('groups')
    success_msg = 'Группа успешно обновлена'
    def get_context_data(self,**kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

def group_detail(request, slug):
    group = CustomGroup.objects.get(slug__iexact=slug)
    for obj in Configs.objects.filter(id=1):
        ip = obj.ip_addr
        port = obj.port_f
    template = 'group_detail.html'
    context = {
        'group': group,
        'obj':obj
    }
    return render(request, template, context)

# Работа с пользователями

class AddUser(CustomSuccessMessageMixin, CreateView):
    model = CustomUser
    template_name = 'users.html'
    form_class = AddUserForm
    success_url = reverse_lazy('users')
    success_msg = 'Пользователь добавлен'
    def get_context_data(self,**kwargs):
        kwargs['list_users'] = CustomUser.objects.all().order_by('username')
        return super().get_context_data(**kwargs)

class UpdateUser(CustomSuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = 'users.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('users')
    success_msg = 'Пользователь успешно обновлен'
    def get_context_data(self,**kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

class DelUser(DeleteView):
    model = CustomUser
    template_name = 'users.html'
    success_url = reverse_lazy('users')
    success_msg = 'Пользователь удален'
    
    def post(self,request,*args,**kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

class UpdatePass(CustomSuccessMessageMixin,UpdateView):
    model = CustomUser
    template_name = 'users.html'
    form_class = UpdatePassword
    success_url = reverse_lazy('users')
    success_msg = 'Пароль успешно обновлен'
    def get_context_data(self,**kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

def public_all(request):
    list_cameras = Cameras.objects.filter(camera_type="PU")
    for obj in Configs.objects.filter(id=1):
        ip = obj.ip_addr
        port = obj.port_f
    
    paginator = Paginator(list_cameras, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'obj':obj,
        'page_obj': page_obj
    }
    template = 'cameras/public.html'
    return render(request, template, context)

def privat_all(request):
    list_cameras = Cameras.objects.filter(camera_type="PR")
    for obj in Configs.objects.filter(id=1):
        ip = obj.ip_addr
        port = obj.port_f
    
    paginator = Paginator(list_cameras, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'obj':obj,
        'page_obj': page_obj
    }
    template = 'cameras/private.html'
    return render(request, template, context)

#class Home(ListView):
#    model = Cameras
#    template_name = 'index.html'
#    context_object_name = 'list_cameras'

#def login_page(request):
#    if request.method == 'POST':
#        form = AuthUserForm(request.POST)
#        if form.is_valid():
#            username = request.POST['username']
#            password = request.POST['password']
#            user = authenticate(username=['username'], password=['password'])
#            if user is not None:
#                if user.is_active:
#                    login(request, user)
#                    return HttpResponse('Authenticated successfully')
#                else:
#                    return HttpResponse('Disabled account')
#            else:
#                return HttpResponse('Invalid login')
#    else:
#        form = AuthUserForm()
#    return render(request, 'login.html', {'form': form})

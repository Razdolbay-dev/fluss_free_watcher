from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
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

# Create your views here.
def home(request):
    list_cameras = Cameras.objects.all()
    context = {
        'list_cameras':list_cameras
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
            user = CustomUser.objects.get(ip_address=ip) #<-- Проверяет входит ли ip тот что мы получили
            login(request,user)
            return render(request, template, context)
        except ObjectDoesNotExist:
            return render(request, template, context)
    else:
        return render(request, template, context)
    
class DVR(DetailView):
    model = Cameras
    template_name = 'cameras/detail.html'
    context_object_name = 'get_cameras'

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
            slug = transliterate.translit(request.POST['title'].lower().replace(' ', ''), reversed=True)
            
            url = request.POST['url']
            dvr = request.POST['dvr']
            auth =(str(a),str(b))
            title = transliterate.translit(request.POST['title'], reversed=True)
            try:
                path = Storage.objects.get(id=int(request.POST['storage']))
                data = '{"inputs":[{"url":"' + str(url) + '"}],"title":"' + str(slug) + '"}'
            except MultiValueDictKeyError:
                data = '{"inputs":[{"url":"' + str(url) + '"}],"title":"' + str(slug) + '"}'
            response = requests.put('http://localhost:'+ str(c) +'/flussonic/api/v3/streams/'+ str(slug) +'', data = data, auth=(str(a), str(b)), headers = {'content-type': 'application/json'})
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
                port = e.port_f

            name = transliterate.translit(request.POST['title'].lower().replace(' ', '_'), reversed=True)
            url = request.POST['url']
            date = request.POST['dvr']
            title = transliterate.translit(request.POST['title'], reversed=True)

            auth = str(a),str(b)
            try:
                path = Storage.objects.get(id=int(request.POST['storage']))
                data = 'stream '+ str(name) +' { title "'+ str(title) +'"; url '+ str(url) +' aac=true; dvr '+ str(path) + ' '+ str (dvr) +' ; }'
            except MultiValueDictKeyError:
                data = 'stream '+ str(name) +' { title "'+ str(title) +'"; url '+ str(url) +' aac=true; }'
            
            response = requests.post('http://localhost:'+ str(port) +'/flussonic/api/config/stream_create', data=data, auth=auth)
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
        response = requests.delete('http://localhost:'+ str(c) +'/flussonic/api/v3/streams/' + str(name) +'', auth=(str(a), str(b)))
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
            return redirect(reverse('settings'))
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

        return redirect(reverse('settings'))

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
            return HttpResponseRedirect('/settings')
        return render(request, self.template_name, success_msg, {'form': form})
#class UpdateStorage(CustomSuccessMessageMixin,View):
  # model = Cameras
   # template_name = 'cameras.html'
    

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
    template = 'groups/group_detail.html'
    context = {
        'group': group
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

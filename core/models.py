from django.conf import settings
from django.db import models
from django.db.models import CharField, DateField, ForeignKey, Model
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser, User
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField
from autoslug.settings import slugify as default_slugify
from django_extensions.db.fields import AutoSlugField

import transliterate

# Create your models here.
def my_slugify_function(content):
    return transliterate.translit(content.replace(' ', '').lower(),reversed=True)

#Хранилища
class Storage(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя')
    slug = AutoSlugField(populate_from='title')
    path = models.CharField(max_length=250, null=True, verbose_name='URL')

    def __str__(self):
        return '{}'.format(self.path)

    class Meta:
        verbose_name='Хранилище'
        verbose_name_plural='Хранилища'
#Модель камер
class Cameras(models.Model):
    permission = (
        ('PU', 'Публичная'),
        ('PR', 'Частная'),
        ('OT', 'Другие'),
    )
    days = (
        ('0', 'Отключить'),
        ('86400', '1 день'),
        ('259200', '3 дня'),
        ('432000', '5 дней'),
        ('604800', '1 неделя'),
        ('1209600', '2 недели')
    ) 
    title = models.CharField(max_length=200, verbose_name='Имя')
    url = models.CharField(max_length=250, verbose_name='URL')
    slug = AutoSlugField(populate_from='title', slugify_function=my_slugify_function)
    camera_type = models.CharField(max_length=10, choices=permission, verbose_name='Тип доступа')
    groups = models.ManyToManyField('CustomGroup', blank=True, verbose_name='Группы', related_name='tags')
    storage = models.ManyToManyField('Storage', blank=True, verbose_name='Хранилище', related_name='storage')
    dvr = models.CharField(max_length=10, blank=True, choices=days, verbose_name='Тип доступа')

    def __str__(self):
        return (self.title)

    def get_delete_url(self):
        return reverse('delcam', kwargs={'slug': self.slug})

    class Meta:
        verbose_name='Камеру'
        verbose_name_plural='Камеры'
#группа 
class CustomGroup(models.Model):
    title = models.CharField(max_length=150, verbose_name='Имя группы')
    description = models.CharField(max_length=150, verbose_name='Описание', blank=True)
    slug = AutoSlugField(populate_from='title', max_length=150)
    
    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('group_detail', kwargs={'slug': self.slug})
        
    class Meta:
        verbose_name='Группу'
        verbose_name_plural='Группы'

# Custom User Model

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200, blank=True, verbose_name='Почта')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='Внутренний IP')
    members = models.ManyToManyField('CustomGroup', db_table='slug', blank=True, verbose_name='Группы', related_name='groups')
    dvr = models.BooleanField(default=False, verbose_name='Доступ к архиву')
    update_cam = models.BooleanField(default=False, verbose_name='Редактирование камер')

# Модель настроек
class Configs(models.Model): 
    title = models.CharField(max_length=150, verbose_name='Отображаемое имя')
    logo = models.ImageField(upload_to='logo/', blank=True)
    user_f = models.CharField(max_length=25, default='flussonic', verbose_name='Логин ( flussonic )', blank=False)
    pass_f = models.CharField(max_length=25, default='letmein!', verbose_name='Пароль ( flussonic )', blank=False)
    port_f = models.CharField(max_length=10, default='8080', verbose_name='Порт ( flussonic )', blank=False)
    ip_addr = models.CharField(max_length=15, default='127.0.0.1', verbose_name='IP Адресс сервера', blank=False)
    def __str__(self):
        return '{}'.format(self.title)
        
    class Meta:
        verbose_name='Настройка'
        verbose_name_plural='Настройки'

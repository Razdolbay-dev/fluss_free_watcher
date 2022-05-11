# Generated by Django 2.2.14 on 2022-03-31 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configs',
            name='ip_addr',
            field=models.CharField(default='127.0.0.1', max_length=15, verbose_name='IP Адресс сервера'),
        ),
        migrations.AlterField(
            model_name='cameras',
            name='dvr',
            field=models.CharField(blank=True, choices=[('0', 'Отключить'), ('86400', '1 день'), ('259200', '3 дня'), ('432000', '5 дней'), ('604800', '1 неделя'), ('1209600', '2 недели')], max_length=10, verbose_name='Тип доступа'),
        ),
    ]

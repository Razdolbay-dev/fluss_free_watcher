# Free Watcher with API Flussonic Media Server
Проект для личного пользования. Разработан на коленке в свободное время
## Функции
- Авторизация по IP 
- Интеграция (не полная) с Flussonic по API
- В целом вроде умеет все что Watcher , только бесплатный =)
Написан на Django 2.2.14
## Краткий инструктаж
### Если нужен чистый проект :

Выгружаем проект себе на сервер
```sh
https://github.com/somk3zzz/fluss_free_watcher.git
```
Переходим в каталог ```cd fluss_free_watcher```

Выполняем поэтапно:
```sh
rm db.sqlite3
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver 0:80
```
### Если оставить все как есть:

```sh
./manage.py runserver 0:80
```
# WARNING!!!
Морда должна работать от 80 порта. Значит после установки нужно убрать 80 порт в админке Flussonic Media Server
```
Логин: flussonic
Пароль: letmein!
```

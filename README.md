# Flussonic Watcher на Django 

Цель данной оболочки полный отказ от Watcher и переход на Media Server
Делается в целях экономии денежных средств

Installation
OS X & Linux & Windows:
```sh
git clone https://github.com/somk3zzz/fluss_free_watcher.git
cd fluss_free_watcher
pip install -r req.tx
```

## Next Steps
Проводим миграции
```sh
./manage.py makemigrations
./manage.py migrate
```
И запускаем для теста 
Внимание ! Flussonic должен висеть ТОЛЬКО на 8080 порту либо на альтернативном 88, так как морда должна работать на 80
```sh
./manage.py runserver 0:80
```

# Социальная сеть дневников.

## Пользватели могут:
- Зарегистрироваться и создать свою страницу.
- Публиковать и просматривать посты на своей странице.
  - Посты можно публиковать в группу по теме.
  - Можно загрузить картинку как обложку поста.
- Заходить на страницы других пользователей:
  - Просматривать их посты.
  - Оставлять комментарии к постам.
  - Подписываться на обновления.
- Во вкладке "Избранные авторы" на главной отображаются только посты от авторов, на которых подписан пользователь.

## Автоматическое создание постов
В проекте настроена автоматическая публикация постов при помощи очереди заданий Django-Q. Модуль `tasks` берет случайную циатату с [bash.im](http://www.bash.im/) и случайную вакансию с [hh.ru](http://www.hh.ru/) и публикует их. Расписание устанавливается через административную панель Django.
Если Вы хотите воспользоваться этим функционалом, запустите процесс `python manage.py qcluster`, затем в административной панели django зайдите в Scheduled tasks секции Django-Q и создайте задание:
```
Name: название задания
Func: tasks.posts.make_post
Args: 'hh' или 'bash'
Schedule type - задайте расписание
```
# Установка
Склонируйте репозиторий. Находясь в папке с кодом создайте виртуальное окружение `python -m venv venv`, активируйте его (Windows: `source venv\scripts\activate`; Linux/Mac: `sorce venv/bin/activate`), установите зависимости `python -m pip install -r requirements.txt`.

Для запуска сервера разработки, находясь в директории проекта, выполните команды:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Проект запущен и доступен по адресу [localhost:8000](http://localhost:8000/).

## Технологии

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Pillow](https://pypi.org/project/Pillow/)
- [Sorl-thumbnail](https://pypi.org/project/sorl-thumbnail/)
- [Django-debug-toolbar](https://pypi.org/project/django-debug-toolbar/)
- [Yandex Cloud](https://cloud.yandex.ru/)
- [PostgreSQL](https://www.postgresql.org/)
- [Gunicorn](https://gunicorn.org/)
- [Nginx](https://nginx.org/)

## Подготовлен к работе с
- [Django-Q](https://pypi.org/project/django-q/)
- [UptimeRobot](https://uptimerobot.com)
- [Sentry](https://sentry.io/)

# Social network for personal diaries.

## Users can
- Sign up and create their own page.
- Create and view posts on their page.
  - Posts can be placed in a group by subject.
  - A picture can be uploaded as the post's cover.
- Visit other users' pages:
  - View their posts
  - Comment their posts.
  - Subscribe to their updates.
- 'Favourites' section of main page shows only posts from followed authors.

## Automated posting
The project is set up with Django-Q task queue. The `tasks` module scrapes [bash.im](http://www.bash.im/) for a random quote and [hh.ru](http://www.hh.ru/) for a random vacancy and creates posts with results. Schedule is set up through Django Admin.
If you want to use this feature, start an instance of `python manage.py qcluster`.

## Installation
Clone the repo to your server, set up a python virtual environment for it and install dependancies from 'requirements.txt'

## Built with

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Pillow](https://pypi.org/project/Pillow/)
- [Sorl-thumbnail](https://pypi.org/project/sorl-thumbnail/)
- [Django-debug-toolbar](https://pypi.org/project/django-debug-toolbar/)
- [Yandex Cloud](https://cloud.yandex.ru/)
- [PostgreSQL](https://www.postgresql.org/)
- [Gunicorn](https://gunicorn.org/)
- [Nginx](https://nginx.org/)

## Set up to work with
- [Django-Q](https://pypi.org/project/django-q/)
- [UptimeRobot](https://uptimerobot.com)
- [Sentry](https://sentry.io/)

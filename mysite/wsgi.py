"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named
``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

# Импорт модуля для работы с операционной системой
# Позволяет управлять переменными окружения и путями
import os

# Импорт функции get_wsgi_application из Django
# WSGI (Web Server Gateway Interface) - стандартный интерфейс между веб-сервером
# и Python-приложениями для обработки HTTP-запросов
from django.core.wsgi import get_wsgi_application

# Установка переменной окружения DJANGO_SETTINGS_MODULE
# Критически важная настройка, которая указывает Django,
# какой файл настроек использовать (в данном случае mysite/settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Создание WSGI-приложения
# Это основная точка входа для WSGI-совместимых серверов:
# - Gunicorn
# - uWSGI
# - mod_wsgi (для Apache)
# - waitress
application = get_wsgi_application()

# Ключевые особенности:
# Назначение файла:

# Точка входа для WSGI-серверов

# Преобразует Django-проект в формат, понятный веб-серверам

# Обязателен для традиционного развертывания (не async)

# Сравнение WSGI и ASGI:
# # WSGI (синхронный)
# from django.core.wsgi import get_wsgi_application  # Для традиционных серверов

# # ASGI (асинхронный)
# from django.core.asgi import get_asgi_application  # Для async-серверов
# Переменная окружения:

# DJANGO_SETTINGS_MODULE должна указывать на Python-путь к файлу настроек

# Формат: 'пакет.пакет.settings' (в данном случае 'mysite.settings')

# Альтернативно можно задать через окружение перед запуском:

# bash

# export DJANGO_SETTINGS_MODULE=mysite.settings

# Использование с разными серверами:
# Для запуска через Gunicorn:
# bash

# # Gunicorn
# gunicorn mysite.wsgi:application
#Для запуска через uWSGI:
# # uWSGI
# uwsgi --module mysite.wsgi:application
# Для запуска через Apache с mod_wsgi:
# # Apache mod_wsgi
# WSGIScriptAlias / /path/to/mysite/wsgi.py
"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named
``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# Импорт модуля для работы с операционной системой
# Позволяет взаимодействовать с переменными окружения и другими функциями ОС
import os

# Импорт функции get_asgi_application из Django
# ASGI (Asynchronous Server Gateway Interface) - асинхронный интерфейс сервера,
# который пришел на смену WSGI в современных версиях Django
from django.core.asgi import get_asgi_application

# Установка переменной окружения DJANGO_SETTINGS_MODULE
# Эта переменная указывает Django, какой модуль настроек использовать
# В данном случае указываем на файл settings.py в проекте mysite
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Создание ASGI-приложения
# Функция get_asgi_application() инициализирует и возвращает ASGI-приложение Django
# Это основная точка входа для ASGI-серверов (Daphne, Uvicorn, Hypercorn и др.)
application = get_asgi_application()

# Ключевые особенности:
# Назначение файла:
# Точка входа для ASGI-серверов
# Используется для асинхронных серверов (вместо традиционных WSGI)
# Обязателен для работы с WebSockets и async-функциями
# Переменная окружения:
# DJANGO_SETTINGS_MODULE должна указывать на Python-путь к вашему файлу настроек
# Формат: 'имя_проекта.settings' (в данном случае 'mysite.settings')
# ASGI vs WSGI:
# # ASGI (асинхронный интерфейс)
# from django.core.asgi import get_asgi_application
# # WSGI (традиционный интерфейс)
# from django.core.wsgi import get_wsgi_application
# Использование:
# Для запуска через Daphne: daphne mysite.asgi:application
# Для запуска через Uvicorn: uvicorn mysite.asgi:application
# Дополнительные возможности:
# Можно добавлять middleware для ASGI
# Поддержка WebSockets при правильной настройке
# Интеграция с Channels для реального времени
# Пример расширенной версии (с Channels):
# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # "websocket": AuthMiddlewareStack(
#     #     URLRouter(
#     #         your_app.routing.websocket_urlpatterns
#     #     )
#     # ),
# })
# Когда использовать:
# Базовый вариант (как в примере):
# Для обычных Django-проектов
# При использовании ASGI-серверов
# Расширенный вариант:
# При работе с Django Channels
# Для WebSocket-соединений
# Для HTTP/2 и других современных протоколов
# Не требуется:
# При использовании традиционных WSGI-серверов (Gunicorn, uWSGI)
# Для простых проектов без async-функций
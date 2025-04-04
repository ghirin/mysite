# Импорт необходимых модулей Django
from django.contrib import admin  # Модуль административной панели
from django.urls import include, path  # Функции для работы с URL-маршрутами
from blog import views  # Импорт views из приложения blog

# Основной список URL-маршрутов проекта
urlpatterns = [
    # Маршрут к административной панели Django
    # Доступен по URL: /admin/
    path('admin/', admin.site.urls),
    
    # Подключение URL-маршрутов из приложения blog
    # Доступны по URL: /blog/
    # Используется функция include() для включения маршрутов из blog.urls
    # namespace='blog' создает пространство имен для URL приложения
    # Корректный синтаксис include() с передачей кортежа (blog.urls, 'blog')
    # где 'blog' - имя приложения (app_name)
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    
    # Главная страница сайта (корневой URL)
    # Вариант 1: Функциональное представление (закомментировано)
    # path('', views.post_list, name='post_list'),
    
    path('', views.PostListView.as_view(), name='post_list'), # Маршрут для списка постов
    # Использует класс PostListView для обработки запросов
    # as_view() преобразует класс в callable-объект для Django
    # name='post_list' позволяет ссылаться на этот URL в шаблонах
]
# # Ключевые особенности:
# Структура URL-маршрутов:
# /admin/ - стандартный маршрут административной панели
# /blog/ - все маршруты из приложения blog
# / - главная страница (отображает список постов)
# Пространства имен (namespace):
# namespace='blog' позволяет однозначно идентифицировать URL
# В шаблонах можно использовать {% url 'blog:post_detail' %}
# Разные типы представлений:
# admin.site.urls - встроенное админ-представление
# include() - подключение маршрутов из другого файла
# as_view() - преобразование класса в view-функцию
# Best Practices:
# Четкое разделение маршрутов приложения (blog/) и проекта
# Использование именованных URL (name='post_list')
# Комментирование альтернативных вариантов
# Важные нюансы:
# Корректный синтаксис include() с кортежем (urls, app_name)
# Пространство имен должно соответствовать app_name в blog.urls
# Класс-базированные views требуют вызова as_view()
# Дополнительные пояснения:
# include():
# Первый аргумент - путь к модулю с URL-шаблонами ('blog.urls')
# Второй аргумент - имя приложения ('blog') должно совпадать с app_name
# namespace позволяет иметь одинаковые имена URL в разных приложениях
# PostListView:
# Наследуется от django.views.generic.ListView
# Автоматически реализует пагинацию, сортировку
# Часто требует меньше кода, чем функциональный аналог
# Админка:
# Автоматически включает:
# Аутентификацию
# Управление пользователями
# CRUD для моделей
# Пример содержимого blog/urls.py для корректной работы:
# from django.urls import path
# from . import views
# app_name = 'blog'  # Должно совпадать с именем в include()
# urlpatterns = [
#     path('', views.post_list, name='post_list'),
#     # другие маршруты...
# ]
# Импорт функции path из модуля django.urls - основы для определения маршрутов URL
from django.urls import path

# Импорт модуля views из текущего пакета (директории) - содержит обработчики запросов
from . import views

# Определение пространства имен приложения 'blog' для уникальной идентификации URL
# Позволяет различать URL разных приложений с одинаковыми именами маршрутов
app_name = 'blog'


# Список URL-шаблонов (маршрутизация URL → представления)
urlpatterns = [
    # Альтернативный маршрут для списка постов:
    path('', views.post_list, name='post_list'),
    # Закомментированный маршрут для списка постов
    #path('', views.PostListView.as_view(), name='post_list'), # Маршрут для списка постов
    # Использует класс PostListView для обработки запросов
    # as_view() преобразует класс в callable-объект для Django
    # name='post_list' позволяет ссылаться на этот URL в шаблонах
    
    path(
    'tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'
    ),

    # Маршрут для отображения списка постов
    # Закомментированная альтернатива - использование функционального представления
    # path('', views.post_list, name='post_list'),
    # Обрабатывает корневой URL ('') с помощью PostListView
    # name='post_list' позволяет ссылаться на этот URL в шаблонах
    # Маршрут для детальной страницы поста с параметрами:
    # <int:year> - целочисленный параметр года (например 2023)
    # <int:month> - целочисленный параметр месяца (1-12)
    # <int:day> - целочисленный параметр дня (1-31)
    # <slug:post> - slug-идентификатор поста (URL-совместимая строка)
    # Пример URL: /blog/2023/10/25/my-awesome-post/
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'
    ),

    # Маршрут для функционала "Поделиться постом":
    # <int:post_id> - ID поста как целое число
    # Пример URL: /blog/42/share/
    path(
        '<int:post_id>/share/',  # Параметр post_id - ID поста
        views.post_share,        # Обработчик - функция post_share из views.py
        name='post_share'       # Имя маршрута для использования в шаблонах
    ),

    # Маршрут для добавления комментария к посту:
    # <int:post_id> - ID поста как целое число
    # Пример URL: /blog/post/42/comment/
    path(
        'post/<int:post_id>/comment/',  # Параметр post_id - ID поста
        views.post_comment,             # Обработчик - функция post_comment из views.py
        name='post_comment'             # Имя маршрута для использования в шаблонах
    ),
]

# Ключевые особенности:
# Структура URL:
# Четкое разделение: просмотр (detail) vs действие (share)
# Типы параметров:
# <int:param>  # Автоматическая конвертация в integer
# <slug:param> # Валидация по slug-стандарту (ASCII, дефисы, подчеркивания)
# Именованные маршруты:
# name='post_detail'  # Позволяет в шаблонах использовать:
# {% url 'blog:post_detail' year=2023 month=10 day=25 post='my-post' %}
# Гибкость представлений:
# Комбинация class-based (PostListView) и function-based (post_detail, post_share) views
# as_view() преобразует класс в callable-объект для Django
# Best Practices:
# Пространство имен (app_name) предотвращает коллизии URL
# Четкие имена маршрутов (post_list/detail/share) улучшают читаемость
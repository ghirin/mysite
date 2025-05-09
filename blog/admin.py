# Импорт модуля администратора Django
from django.contrib import admin
# Импорт модели Post из текущего приложения
from .models import Comment, Post

# Регистрация модели Post с кастомной админ-конфигурацией
# Декоратор @admin.register заменяет admin.site.register(Post, PostAdmin)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Post в админ-панели Django.
    Наследуется от admin.ModelAdmin.
    """
    
    # Поля, отображаемые в списке записей
    list_display = [
        'title',    # Заголовок поста
        'slug',     # URL-идентификатор
        'author',   # Автор (отображает __str__ модели User)
        'publish',  # Дата публикации
        'status'    # Статус (черновик/опубликован)
    ]
    
    # Фильтры в правой части админки (позволяют фильтровать записи)
    list_filter = [
        'status',    # Фильтр по статусу (Draft/Published)
        'created',   # Фильтр по дате создания (сегодня/неделя/месяц и т.д.)
        'publish',   # Фильтр по дате публикации
        'author'     # Фильтр по автору
    ]
    
    # Поля, по которым работает поиск (поисковая строка вверху списка)
    search_fields = [
        'title',  # Поиск по заголовку
        'body'    # Поиск по содержимому поста
    ]
    
    # Автоматическое заполнение slug на основе title при создании/редактировании
    prepopulated_fields = {
        'slug': ('title',)  # slug генерируется из title
    }
    
    # Поля, которые будут отображаться как виджет поиска (вместо выпадающего списка)
    raw_id_fields = [
        'author'  # Для автора (полезно при большом количестве пользователей)
    ]
    
    # Иерархическая навигация по датам (отображается над списком записей)
    date_hierarchy = 'publish'  # Позволяет фильтровать по году/месяцу/дню
    
    # Сортировка записей по умолчанию (сначала по статусу, затем по дате публикации)
    ordering = [
        'status',   # Сортировка по статусу (Draft -> Published)
        'publish'   # Затем по дате публикации (новые сверху)
    ]
    
    # Настройка отображения фацетов (группировок) - новое в Django 5.0+
    show_facets = admin.ShowFacets.ALWAYS  # Всегда показывать панель фильтров
    
    # Дополнительные часто используемые параметры (не показаны в этом коде):
    # list_editable = ['status']  # Позволяет редактировать статус прямо из списка
    # list_per_page = 50  # Количество записей на странице
    # exclude = ['created']  # Скрыть поля из формы редактирования
    # readonly_fields = ['updated']  # Только для чтения
#     # fieldsets = [...]  # Группировка полей в форме редактирования

@admin.register(Comment)
class CommentForm(admin.ModelAdmin):
    # Настройка отображения модели Comment в админ-панели Django    
    list_display = [
        'name',    # Имя комментатора
        'email',   # Email комментатора
        'post',    # Пост, к которому относится комментарий
        'created', # Дата создания комментария
        'active'   # Активен ли комментарий
    ]
    # Поля, которые будут отображаться как виджет поиска (вместо выпадающего списка)
    list_filter = [
        'active',   # Фильтр по активности комментария
        'created',  # Фильтр по дате создания
        'updated'   # Фильтр по дате обновления
    ]
    # Поля, по которым работает поиск (поисковая строка вверху списка)
    search_fields = [
        'name',     # Поиск по имени комментатора
        'email',    # Поиск по email
        'body'      # Поиск по тексту комментария
    ]
# Ключевые особенности:
# Оптимизация интерфейса:
# raw_id_fields ускоряет загрузку при многих пользователях
# prepopulated_fields автоматизирует заполнение slug
# date_hierarchy добавляет удобную навигацию по датам
# Функциональность поиска:
# Поиск по тексту (title и body)
# Фильтрация по статусу, датам и автору
# Сортировка и организация:
# Умная сортировка по умолчанию (status + publish)
# Гибкое отображение колонок (list_display)
# Новые возможности Django 5.0+:
# show_facets контролирует отображение панели фильтров
# Доступны варианты: ALWAYS, AUTO, NEVER
# Безопасность:
# Автоматическая проверка прав доступа
# Защита от XSS/CSRF атак
# Расширяемость:
# Можно добавить кастомные действия
# Переопределить методы save(), delete()
# Добавить inline-формы для связанных моделей
# Пример добавления кастомного действия:
# @admin.action(description='Mark selected posts as published')
# def make_published(modeladmin, request, queryset):
#     queryset.update(status=Post.Status.PUBLISHED)
# class PostAdmin(admin.ModelAdmin):
#     actions = [make_published]
# Импорт необходимых модулей Django
from django.conf import settings  # Доступ к настройкам проекта
from django.db import models  # Базовые классы для моделей
from django.utils import timezone  # Утилиты для работы с датой/временем
from django.urls import reverse  # Генерация URL по имени маршрута
from taggit.managers import TaggableManager

# Кастомный менеджер для опубликованных постов
class PublishedManager(models.Manager):
    def get_queryset(self):
        """Переопределяет стандартный queryset, фильтруя только опубликованные посты"""
        return (
            super().get_queryset()  # Базовый queryset
            .filter(status=Post.Status.PUBLISHED)  # Фильтр по статусу
        )
# Модель поста блога
class Post(models.Model):
    # Менеджер для работы с тегами
    tags = TaggableManager()  # Позволяет добавлять теги к постам

    # Класс для определения вариантов статуса поста
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'  # Черновик (код, человекочитаемое имя)
        PUBLISHED = 'PB', 'Published'  # Опубликован

    # Поля модели:
    title = models.CharField(max_length=250)  # Заголовок (макс. длина 250)
    slug = models.SlugField(
        max_length=250, 
        unique_for_date='publish'  # Уникальность вместе с датой публикации
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Ссылка на модель пользователя из настроек
        on_delete=models.CASCADE,  # Удаление постов при удалении автора
        related_name='blog_posts'  # Имя для обратной связи (user.blog_posts.all())
    )
    body = models.TextField()  # Основное содержимое поста
    publish = models.DateTimeField(
        default=timezone.now  # Дата публикации (по умолчанию сейчас)
    )
    created = models.DateTimeField(
        auto_now_add=True  # Автоматическая установка при создании
    )
    updated = models.DateTimeField(
        auto_now=True  # Автоматическое обновление при сохранении
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,  # Ограниченные варианты из класса Status
        default=Status.DRAFT  # Значение по умолчанию
    )

    # Менеджеры модели:
    objects = models.Manager()  # Стандартный менеджер (все записи)
    published = PublishedManager()  # Кастомный менеджер (только опубликованные)

    # Метаданные модели
    class Meta:
        ordering = ['-publish']  # Сортировка по убыванию даты публикации
        indexes = [
            models.Index(fields=['-publish']),  # Индекс для оптимизации запросов
        ]

    def __str__(self):
        """Строковое представление объекта (админка, shell)"""
        return self.title

    def get_absolute_url(self):
        """Генерирует канонический URL для поста"""
        return reverse(
            'blog:post_detail',  # Имя маршрута с namespace
            args=[
                self.publish.year,  # Год из даты публикации
                self.publish.month,  # Месяц
                self.publish.day,  # День
                self.slug  # Уникальный идентификатор
            ]
        )
# Модель комментариев блога
class Comment(models.Model):
    post = models.ForeignKey(
        Post,  # Связь с моделью Post
        on_delete=models.CASCADE,  # Удаление комментариев при удалении поста
        related_name='comments'  # Имя для обратной связи (post.comments.all())
    )
    name = models.CharField(max_length=80)  # Имя комментатора
    email = models.EmailField()  # Email комментатора
    body = models.TextField()  # Текст комментария
    created = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated = models.DateTimeField(auto_now=True)  # Дата обновления
    active = models.BooleanField(default=True)  # Активность комментария

    class Meta:
        ordering = ['created']  # Сортировка по дате создания
        indexes = [
            models.Index(fields=['created']),  # Индекс для оптимизации
        ]

    def __str__(self):
        """Строковое представление комментария"""
        return f'Comment by {self.name} on {self.post}'
#Ключевые особенности:
# Кастомный менеджер PublishedManager:
# Наследуется от models.Manager
# Фильтрует только посты со статусом PUBLISHED
# Используется как Post.published.all() вместо стандартного Post.objects.all()
# Поля модели:
# unique_for_date='publish' - гарантирует уникальность slug в пределах одной даты
# auto_now_add/auto_now - автоматическое управление датами
# ForeignKey с related_name - доступ к постам автора через user.blog_posts
# TextChoices для статуса:
# Современный способ (Django 3.0+) определения вариантов выбора
# Доступ через Post.Status.PUBLISHED и Post.Status.choices
# Оптимизации:
# Индекс по полю publish ускоряет сортировку и фильтрацию
# Правильный порядок сортировки в class Meta
# get_absolute_url():
# Реализует "канонический URL" для объекта
# Использует reverse() вместо жестко заданных URL
# Важно для SEO и правильных ссылок в админке
# Два менеджера:
# objects - стандартный (все записи, включая черновики)
# published - только опубликованные посты (использует кастомный менеджер)
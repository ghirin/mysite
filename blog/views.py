# Импорт необходимых модулей Django
from django.core.mail import send_mail  # Функция отправки email
from django.core.paginator import (
    EmptyPage,       # Исключение для пустой страницы
    PageNotAnInteger, # Исключение для нечисловой страницы
    Paginator        # Основной класс пагинации
)
from django.shortcuts import (
    get_object_or_404,  # Получение объекта или 404
    render              # Рендеринг шаблонов
)
from django.views.decorators.http import require_POST  # Декоратор для POST-запросов
from django.views.generic import ListView  # Класс для списковых представлений
from .forms import CommentForm, EmailPostForm  # Форма для отправки поста по email и отправки комментария
from .models import Post  # Импорт модели Post из текущего приложения
from taggit.models import Tag  # Импорт модели Tag из приложения taggit
from django.db.models import Count  # Импорт функции Count для подсчета тегов

def post_list(request, tag_slug=None):
    """Функциональное представление списка опубликованных постов с пагинацией"""
    # Получаем все опубликованные посты через кастомный менеджер
    post_list = Post.published.all()
    tag = None
    if tag_slug :
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # Настройка пагинации - 3 поста на страницу
    paginator = Paginator(post_list, 3)
    
    # Получаем номер страницы из GET-параметра 'page' (по умолчанию 1)
    page_number = request.GET.get('page', 1)
    
    try:
        # Пытаемся получить запрошенную страницу
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        # Если page не число - показываем первую страницу
        posts = paginator.get_page(1)
    except EmptyPage:
        # Если страница вне диапазона - показываем последнюю
        posts = paginator.get_page(paginator.num_pages)
    
    # Рендерим шаблон с передачей постов в контекст
    return render(
        request,
        'blog/post/list.html',
        {
            'posts': posts,
            'tag': tag,
        }
    )

def post_detail(request, year, month, day, post):
    """Детальное представление поста с проверкой даты и статуса"""
    # Получаем пост или 404, проверяя:
    # - статус (только опубликованные)
    # - slug поста
    # - точное совпадение даты публикации
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    
    # Получаем все комментарии к посту
    comments = post.comments.filter(active=True)  # Только активные комментарии Мы добавили QuerySet для извлечения всех активных комментариев к посту следующим образом.
    # Инициализируем форму для комментариев
    form = CommentForm()

    # Получаем список похожих постов по тегам

    post_tags_ids = post.tags.values_list('id', flat=True) # Получаем ID тегов поста
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids # Фильтруем посты по тегам
    ).exclude(id=post.id) # Исключаем текущий пост
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags') # Подсчитываем количество тегов
    ).order_by('-same_tags', '-publish')[:4] # Сортируем по количеству тегов и дате публикации

    # Рендерим шаблон детальной страницы
    return render(
        request, # Передаем объект запроса
        'blog/post/detail.html', # Путь к шаблону
        {
          'post': post, # Передаем пост
          'comments': comments, # Передаем комментарии
          'form': form, # Передаем комментарии и форму
          'similar_posts': similar_posts # Передаем похожие посты
        } 
        # Форма для отправки комментариев пользователем
    )

class PostListView(ListView):
    """
    Альтернативное класс-базированное представление списка постов.
    Наследует функциональность Django's ListView.
    """
    queryset = Post.published.all()  # Queryset всех опубликованных постов
    context_object_name = 'posts'    # Имя переменной в контексте шаблона
    paginate_by = 3                 # Количество постов на страницу
    template_name = 'blog/post/list.html'  # Путь к шаблону

def post_share(request, post_id):
    """Обработчик отправки поста по email"""
    # Получаем пост по ID, проверяя что он опубликован
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    
    # Инициализируем флаг отправки
    sent = False
    
    if request.method == 'POST':
        # Если POST-запрос - обрабатываем форму
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Если форма валидна - получаем очищенные данные
            cd = form.cleaned_data
            
            # Формируем абсолютный URL поста
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            
            # Создаем тему письма
            subject = f"{cd['name']} ({cd['email']}) рекомендует Вам для ознакомления {post.title}"
            
            # Формируем тело письма
            message = f"Ознакомьтесь {post.title} at {post_url}\n\n{cd['comments']}"
            
            # Отправляем email (реальная отправка требует настроек SMTP)
            send_mail(
                subject=subject,
                message=message,
                from_email=None,  # Используется DEFAULT_FROM_EMAIL из settings
                recipient_list=[cd['to']]
            )
            
            # Устанавливаем флаг успешной отправки
            sent = True
    else:
        # Для GET-запроса создаем пустую форму
        form = EmailPostForm()
    
    # Рендерим шаблон с формой, постом и статусом отправки
    return render(
        request,
        'blog/post/share.html',
        {   
            'post': post,
            'form': form,
            'sent': sent
        }
    )

@require_POST
def post_comment(request, post_id):
    """Обработчик отправки комментария к посту"""
    # Получаем пост по ID
    post = get_object_or_404(
        Post, # Проверяем что пост существует
        id=post_id, # ID поста из URL
        status=Post.Status.PUBLISHED #
    )
    # Инициализируем форму с данными из POST-запроса
    form = CommentForm(request.POST)
    # Проверяем валидность формы
    if form.is_valid():
        # Если форма валидна - создаем новый комментарий
        comment = form.save(commit=False)
        comment.post = post  # Привязываем комментарий к посту
        comment.save()
        # Cохраняем комментарий в базе данных

        # Редирект на страницу поста с добавленным комментарием
        return render(
            request,
            'blog/post/comment.html',
            {'post': post,
             'form': form,
             'comment': comment
            }
        )
# Ключевые особенности:
# Два подхода к списку постов:
# Функциональный (post_list) с ручной обработкой пагинации
# Класс-базированный (PostListView) с автоматической пагинацией
# Безопасность в post_detail:
# Проверка статуса публикации
# Точное соответствие даты публикации
# Защита от несуществующих постов (get_object_or_404)
# Отправка email:
# Использование Django форм (EmailPostForm)
# Валидация данных формы
# Формирование абсолютного URL (build_absolute_uri)
# Настройка темы и тела письма
# Интеграция с send_mail
# Шаблоны:
# Четкое разделение шаблонов по назначению (list/detail/share)
# Единая структура папок (blog/post/)
# Обработка ошибок:
# Пагинация с обработкой неверных номеров страниц
# 404 для несуществующих постов
# Валидация формы перед отправкой
# Разделение логики:
# Получение данных отделено от рендеринга
# Бизнес-логика (отправка email) отделена от представления
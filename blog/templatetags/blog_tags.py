from django import template
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag

def total_posts():
    # Фукнция возвращает общее количество постов в блоге
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    # Функция возвращает последние опубликованные посты
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    # Функция возвращает самые комментируемые посты
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    # Функция форматирует текст в Markdown
    return mark_safe(markdown.markdown(text))
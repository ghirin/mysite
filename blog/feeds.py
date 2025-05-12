import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html  # Импорт функции для обрезки текста
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):

    title= 'Мой блог'
    link = reverse_lazy('blog:post_list')
    description = 'Последние обновления на сайте'

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)
    
    def item_pubdate(self, item):
        return item.publish
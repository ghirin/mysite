from django.contrib import admin
from django.urls import include, path
from blog import views  # Import views from the blog application

urlpatterns = [
    # The admin interface is available at /admin/
    # The blog application is available at /blog/
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('', views.post_list, name='post_list'),
]

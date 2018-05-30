"""hyn_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.blog import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login),
    path('register/', views.register),
    path('retrieve/', views.retrieve),
    path('bye/', views.bye),
    path('comment/', views.comment),
    path('publish/', views.publish),
    path('search_title/', views.search_title),
    path('user_Post/', views.user_Post),
    path('imglook/', views.imglook),
    path('2048/', views.game_2048),
    path('modify_publish/', views.modify_publish),
    path('articles/<int:id>/', views.detail, name='detail'),
    path('category/<int:id>/', views.search_category, name='category_menu'),
    path('tag/<str:tag>/', views.search_tag, name='search_tag'),
    path('archives/<str:year>/<str:month>', views.archives, name='archives'),
    path('summernote/', include('django_summernote.urls')),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('cbv', views.CBV.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
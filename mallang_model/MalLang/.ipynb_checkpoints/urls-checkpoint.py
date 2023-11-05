"""
URL configuration for MalLang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home_view, name="home"),
    path("user/", include('user.urls'), name="login"),
    path("main/", views.main_view, name="main"),
    path("diary/", views.diary_view, name="diary"),
    path("mydiary/", views.mydiary_view, name="mydiary"),
    path("diaryshow/", views.diaryshow_view, name="diaryshow"),
    path("diarycheck/", views.diary_check, name="diarycheck"),
    path("diarysave/", views.diary_save, name="diarysave"),
    path("board/", views.board, name="board"),
    path("detail/<int:id>/", views.detail, name="detail"),
    path("boardwrite", views.boardwrite, name="boardwrite"),
    path("update/<int:id>/", views.update, name="update"),
    path("delete/<int:id>/", views.delete, name="delete"),
    path('searchengine/', views.search_engine, name="search"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
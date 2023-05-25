"""MusicRec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from MusicRecApp import views

urlpatterns = [
    path('', views.show_songs, name='show_songs'),
    path('init/', views.init, name='init'),
    path('upload/', views.upload_mp3, name='upload_mp3'),
    path('songs/<int:song_id>/delete/', views.delete_song, name='delete_song'),
    path('songs/<int:song_id>/similar/', views.show_similar_songs, name='show_similar_songs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

import numpy as np
from MusicRecApp.forms import MP3UploadForm
import os
from .models import Music
from django.shortcuts import render, redirect
from .helpers import process_mp3, initilization, save_uploaded_song, getSimilarSongs

# python manage.py flush
# python manage.py runserver
# songs = init()

def init(request):
    initilization()

    return render(request, template_name='init.html')
def upload_mp3(request):
    form = MP3UploadForm(request.POST, request.FILES)
    if form.is_valid():
        mp3_file = request.FILES['mp3_file']
        file_path = save_uploaded_song(mp3_file)
        process_mp3(file_path)

        uploadedSong = Music.objects.last()
        similarSongs = getSimilarSongs(uploadedSong)

        return render(request, 'upload_success.html', similarSongs)
    form = MP3UploadForm()
    return render(request, 'upload.html', {'form': form})

def show_songs(request):
    songs = Music.objects.all()
    formatted_songs = []

    for song in songs:
        path = os.path.splitext(os.path.basename(song.path))[0]
        formatted_songs.append((path, song.id))

    return render(request, 'show_songs.html', {'songs': formatted_songs})

def delete_song(request, song_id):
    song = Music.objects.get(id=song_id)
    song.delete()
    return redirect('show_songs')

def show_similar_songs(request, song_id):
    song = Music.objects.get(id=song_id)
    similarSongs = getSimilarSongs(song)

    return render(request, 'show_similar_songs.html', similarSongs)


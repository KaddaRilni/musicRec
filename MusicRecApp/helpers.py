import os
from sklearn.neighbors import NearestNeighbors
import numpy as np
import librosa
from collections import Counter
from keras.models import load_model
from pathlib import Path
from .models import Music
from tqdm import tqdm
from django.conf import settings
from keras.models import Model
from django.core.management import call_command

baseRoot = Path(__file__).resolve().parent.parent
MUSIC_ROOT = baseRoot / 'MusicRecApp/testSongs'

def process_mp3(path):
    signal, sr = librosa.load(path, duration=30)
    try:
        melspec = librosa.feature.melspectrogram(y=signal, sr=sr).T[:1280, ]
        if len(melspec) != 1280:
            return None
    except ValueError:
        return None

    # Создание объекта Music и сохранение данных в базе данных
    music = Music(path=path, melspec=np.asarray(np.split(melspec, 10)).tolist())
    music.save()

    return {'path': path, 'melspecs': np.asarray(np.split(melspec, 10))}

def initilization():
    if Music.objects.exists():
        # python manage.py flush
        call_command('flush', interactive=False)
        call_command('migrate')

    mp3s = []
    for root, subdirs, files in os.walk(MUSIC_ROOT):
        for fn in files:
            if fn.endswith('.mp3'):
                mp3s.append(os.path.join(root, fn))
    songs = [process_mp3(path) for path in tqdm(mp3s[:1000])]
    songs = [song for song in songs if song]

    return songs

def most_similar_songs(song_idx, nbrs, vectors):
    distances, indices = nbrs.kneighbors(vectors[song_idx * 10: song_idx * 10 + 10])
    c = Counter()
    for row in indices:
        for idx in row[1:]:
            c[idx // 10] += 1
    return c.most_common()

def save_uploaded_song(mp3_file):
    file_path = os.path.join(settings.MEDIA_ROOT, mp3_file.name)
    with open(file_path, 'wb') as f:
        for chunk in mp3_file.chunks():
            f.write(chunk)

    return file_path
def getAllSongsMelspecsFromMusic():
    all_songs = Music.objects.all()
    inputsDB = []
    for song in all_songs:
        inputsDB.extend(song.melspec)

    return np.array(inputsDB)

def getAllSongsDataFromMusic():
    all_songs = Music.objects.all()
    songs_data = [{'id': song.id, 'path': song.path} for song in all_songs]

    return songs_data

def getSimilarSongs(uploadedSong):
    songsMelspecs = getAllSongsMelspecsFromMusic()
    songsData = getAllSongsDataFromMusic()

    # модель в будущем переделать добавить новые жанры например
    cnn_model = load_model(baseRoot / 'MusicRecApp/song_classify1.h5')
    vectorize_model = Model(inputs=cnn_model.input, outputs=cnn_model.layers[-4].output)
    vectors = vectorize_model.predict(songsMelspecs)
    nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(vectors)

    song_idx = uploadedSong.id-1
    # uploaded song
    song_path = songsData[song_idx]['path']
    songName = os.path.splitext(os.path.basename(song_path))[0]

    # similar songs
    similar_songs = []
    for idx, score in most_similar_songs(song_idx, nbrs, vectors)[:5]:
        similar_song_path = songsData[idx]['path']
        similar_song_score = score
        path = os.path.splitext(os.path.basename(similar_song_path))[0]
        similar_song = {
            'path': path,
            'score': similar_song_score
        }
        similar_songs.append(similar_song)

    context = {
        'song_path': songName,
        'similar_songs': similar_songs
    }

    return context
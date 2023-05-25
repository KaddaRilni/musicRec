from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from MusicRecApp.forms import MP3UploadForm
import os
from sklearn.neighbors import NearestNeighbors
from collections import defaultdict
from keras.models import load_model
import librosa
from collections import Counter
import multiprocessing
from tqdm import tqdm
from keras.models import Model
import numpy as np

MUSIC_ROOT = 'testSongs'

mp3s = []
for root, subdirs, files in os.walk(MUSIC_ROOT):
    for fn in files:
        if fn.endswith('.mp3'):
            mp3s.append(os.path.join(root, fn))

def process_mp3(path):
    signal, sr = librosa.load(path, duration=30)
    try:
        melspec = librosa.feature.melspectrogram(y=signal, sr=sr).T[:1280,]
        if len(melspec) != 1280:
            return None
    except ValueError:
        return None
    return {'path': path,
            'melspecs': np.asarray(np.split(melspec, 10))}
            #по хорошему это хранить в базе ид\пас\мелспек чтобы каждый раз не проделывать это со всеми песнями таблица тест сонгс

songs = [process_mp3(path) for path in tqdm(mp3s[:1000])]
songs = [song for song in songs if song]

def most_similar_songs(song_idx, nbrs, vectors):
    distances, indices = nbrs.kneighbors(vectors[song_idx * 10: song_idx * 10 + 10])
    c = Counter()
    for row in indices:
        for idx in row[1:]:
            c[idx // 10] += 1
    return c.most_common()


def upload_mp3(request):
    if request.method == 'POST':
        form = MP3UploadForm(request.POST, request.FILES)
        if form.is_valid():
            mp3_file = request.FILES['mp3_file']
            file_path = os.path.join(settings.MEDIA_ROOT, mp3_file.name)

            with open(file_path, 'wb') as f:
                for chunk in mp3_file.chunks():
                    f.write(chunk)

            uploadedSong = process_mp3(file_path)
            songs.append(uploadedSong)
            # в ту же таблицу добавляем


            inputs = []
            # теперь можно сонги получить из таблицы
            for song in songs:
                inputs.extend(song['melspecs'])
            # здесь только спектрограммы?(массив циферок)
            inputs = np.array(inputs)

            # модель в будущем переделать добавить новые жанры например
            cnn_model = load_model('song_classify1.h5')
            vectorize_model = Model(inputs=cnn_model.input, outputs=cnn_model.layers[-4].output)
            vectors = vectorize_model.predict(inputs)

            nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(vectors)

            song_idx = len(songs) - 1
            print(songs[song_idx]['path'])
            print('---')
            for idx, score in most_similar_songs(song_idx, nbrs, vectors)[:5]:
                print(songs[idx]['path'], score)
            print('')

            return render(request, 'upload_success.html')
    else:
        form = MP3UploadForm()
    return render(request, 'upload.html', {'form': form})


def index(request):
    return render(request, "test.html")
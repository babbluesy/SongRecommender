import librosa
import librosa.display
import scipy.signal as signal
import pandas as pd
import numpy as np
import json
from glob import glob
import matplotlib.pyplot as plt
import sys

# <wav_fft>
def wav_fft(file_name):
    print("fft start")
    audio_sample, sampling_rate = librosa.load(file_name, sr = None)
    fft_result = librosa.stft(audio_sample, n_fft=1024, hop_length=512, win_length = 1024, window=signal.hann).T
    mag, phase = librosa.magphase(fft_result)
    print("fft end")
    return mag

# <normalize_function>
min_level_db = -100
def _normalize(S):
    return np.clip((S-min_level_db)/(-min_level_db), 0, 1)

# <wav files into DataFrame>
files = glob(r'D:\wav\*.wav')
song_info_df = pd.DataFrame(columns=["artist_name", "song_name", "file_path"])

for i in range(len(files)):
    # <seperate song information>
    terminator_start = files[i].index(' - ')
    terminator_end = files[i].index('.wav')
    sampling_rate = 48000

    s_info = pd.DataFrame({
        "artist_name": files[i][9:terminator_start],
        "song_name": files[i][terminator_start+3:terminator_end],
        "file_path": files[i],
    }, index=[i])

    song_info_df = song_info_df.append(s_info, sort=True)

for j in range(len(files)):
    # # <display spectrogram>
    # # mag = wav_fft("data/mp3/1TEAM - BOUT U.wav")
    # mag = wav_fft(song_info_df['file_path'][i])
    # mag_db = librosa.amplitude_to_db(mag)
    # mag_n = _normalize(mag_db)
    #
    # librosa.display.specshow(mag_n.T, y_axis='linear', x_axis='time', sr=sampling_rate)
    # plt.title('FFT result')
    # plt.show()

    # <pitch tracking>
    # y: 음원의 파형(waveform) 데이터
    # sr: sampling rate (주파수 분석 및 파형의 시간 간격을 결정)

    y, sr = librosa.load(song_info_df['file_path'][j], sr=sampling_rate)
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr, fmin=30, fmax=8000)

    # np.set_printoptions(threshold=sys.maxsize) -> see whole pitch
    pitch_lst = pitches[np.nonzero(pitches)]
    highest_pitch = int(max(pitch_lst))
    lowest_pitch = int(min(pitch_lst))

    # <load json file>
    with open('data/tracks/'+song_info_df['artist_name'][j]+'_tracks_info.json') as f:
        json_data = json.load(f)

    album_lst = list(json_data['albums'].keys())

    # <input highest pitch and lowest pitch to json files>
    for album in range(len(json_data['albums'])):
        for song in range(len(json_data['albums'][album_lst[album]])):
            if song_info_df['song_name'][j] == json_data['albums'][album_lst[album]][song]['name']:
                json_data['albums'][album_lst[album]][song].update({'highest_pitch': highest_pitch})
                json_data['albums'][album_lst[album]][song].update({'lowest_pitch': lowest_pitch})
    # json_data['albums'][album_lst[13]][4]

    with open('data/tracks/'+song_info_df['artist_name'][j]+'_tracks_info.json', 'w', encoding='utf-8') as make_file:
        json.dump(json_data, make_file, indent="\t")

    print('{}. {} ---- complete'.format(j, song_info_df['song_name'][j]))


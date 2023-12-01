import PySimpleGUI as sg
import sys, yt_dlp, music_tag

errors = 0
currently_downloading = False


def what_is(url):
    # Work around to printing errors to the console
    global errors
    errors = ""

    class ignoreErrors:
        @staticmethod
        def error(msg):
            global errors
            errors += msg

        @staticmethod
        def warning(msg):
            pass

        @staticmethod
        def debug(msg):
            pass

    ydl_opts = {'skip_download': True, 'ignoreerrors': True, 'quiet': True, "logger": ignoreErrors, 'extract_flat': True, 'playlistend': 2}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, False)

    if errors:
        return errors

    if 'playlist' in url:
        return 'playlist'
    else:
        return 'vid'


def set_audio_metadata(data, t):
    if t == 'v':
        f = music_tag.load_file(data['requested_downloads'][0]['filepath'])

        fields = ['track', 'artist', 'album', 'release_year']

        for i in fields:
            if data.get(f'{i}'):
                if i == 'track':
                    f['tracktitle'] = data['track']
                    print(data['track'])
                elif i == 'release_year':
                    f['year'] = data[f'{i}']
                    print(data[f'{i}'])
                else:
                    f[f'{i}'] = data[f'{i}']
                    print(data[f'{i}'])

        f.save()

    else:
        songs = data['entries']

        for song in songs:
            f = music_tag.load_file(song['requested_downloads'][0]['filepath'])

            fields = ['track', 'artist', 'album', 'release_year']

            for i in fields:
                if song.get(f'{i}'):
                    if i == 'track':
                        f['tracktitle'] = song['track']
                        print(song['track'])
                    elif i == 'release_year':
                        f['year'] = song[f'{i}']
                        print(song[f'{i}'])
                    else:
                        f[f'{i}'] = song[f'{i}']
                        print(song[f'{i}'])

            f.save()


def download_video(url, t, path):
    if t == 'Audio':
        ydl_opts = {
            'ffmpeg_location': 'C:/ffmpeg/bin',
            'format': 'bestaudio/best',
            'audioformat': 'mp3',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
    else:
        ydl_opts = {
            'format': 'mp4/bestvideo/best',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        metadata = ydl.extract_info(url)

    if t == 'Audio':
        set_audio_metadata(metadata, 'v')


def download_playlist(url, t, path, s, e):
    if t == 'Audio':
        ydl_opts = {
            'ffmpeg_location': 'C:/ffmpeg/bin',
            'format': 'bestaudio/best',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'audioformat': 'mp3',
            'playliststart': s,
            'playlistend': e,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
    else:
        ydl_opts = {
            'format': 'mp4/bestvideo/best',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'playliststart': s,
            'playlistend': e,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        metadata = ydl.extract_info(url)

    print(metadata)

    if t == 'Audio':
        set_audio_metadata(metadata, 'p')

import PySimpleGUI as sg
import sys, yt_dlp, music_tag

errors = 0
currently_downloading = False


def what_is(url):
    # Work around to printing errors to the console
    global errors
    errors = 0

    class ignoreErrors:
        @staticmethod
        def error(msg):
            global errors
            errors += 1

        @staticmethod
        def warning(msg):
            pass

        @staticmethod
        def debug(msg):
            pass

    ydl_opts = {'skip_download': True, 'ignoreerrors': True, 'quiet': True, "logger": ignoreErrors, 'extract_flat': True, 'playlistend': 2}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, False)

    if errors != 0:
        return False

    if 'playlist' in url:
        return 'playlist'
    else:
        return 'vid'


def set_audio_metadata(data):
    f = music_tag.load_file(data['requested_downloads'][0]['filepath'])

    fields = ['track', 'artist', 'album', 'release_year']

    for i in fields:
        if data[f'{i}']:
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

    print(metadata)
    set_audio_metadata(metadata)


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
        ydl.download([url])


# Create the Window
vid_layout = [[sg.Text('YouTube URL:', font=('Helvetica', 20)), sg.Input(key='url', font=('Helvetica', 20))]]
playlist_layout = [[sg.Text('Youtube Playlist:', font=('Helvetica', 20)),
                    sg.Input(key='list_url', font=('Helvetica', 20))],
                   [sg.Text('Start Index:', font=('Helvetica', 20)), sg.Push(),
                    sg.Input('Blank for first', key='start_idx', font=('Helvetica', 20), s=15), sg.Push(),
                    sg.Text('End Index:', font=('Helvetica', 20)), sg.Push(),
                    sg.Input('Blank for last', key='end_idx', font=('Helvetica', 20), s=15)]]

layout = [[sg.Text('Youtube Downloader', font=('Helvetica', 40))],
          [sg.Column(vid_layout, key='vid'), sg.Column(playlist_layout, key='playlist', visible=False)],
          [sg.Push(), sg.Text('Select Folder: ', font=('Helvetica', 20)),
           sg.Input(key='fpath', font=('Helvetica', 20), s=41), sg.FolderBrowse(font=('Helvetica', 15))],
          [sg.Combo(['Video', 'Audio'], key='type', font=('Helvetica', 20)),
           sg.Button('Download', font=('Helvetica', 15)),
           sg.Button('Playlist Toggle', key='toggle', font=('Helvetica', 15)),
           sg.Cancel('Exit', font=('Helvetica', 15))]]

window = sg.Window('Youtube Downloader', layout)
cur_layout = 'vid'

# Start loop
while True:
    # Read window
    event, values = window.read(timeout=1)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'toggle':
        if cur_layout == 'playlist':
            window['playlist'].update(visible=False)
            window['vid'].update(visible=True)
            cur_layout = 'vid'
        else:
            window['playlist'].update(visible=True)
            window['vid'].update(visible=False)
            cur_layout = 'playlist'

    if event == 'Download':
        if values['type'] and values['fpath']:
            if cur_layout == what_is(values['url']):
                download_video(values['url'], values['type'], values['fpath'])
            elif cur_layout == what_is(values['list_url']):
                print('yes')
                start = None
                end = None
                if not values['start_idx']:
                    start = 1
                if not values['end_idx']:
                    end = -1

                if start is None:
                    try: start = int(values['start_idx'])
                    finally: pass
                if end is None:
                    try: end = int(values['end_idx'])
                    finally: pass

                if start is not None and end is not None:
                    download_playlist(values['list_url'], values['type'], values['fpath'], start, end)


window.close()
sys.exit()

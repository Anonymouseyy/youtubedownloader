import sys, yt_dlp, music_tag
import customtkinter as ctk
currently_downloading = False


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

    elif t == 'p':
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


class Vid(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class Playlist(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")

        self.title("Youtube Downloader")
        self.geometry(f"{int(self.winfo_screenwidth())//2}x{int(self.winfo_screenheight())//2}")

        self.title = ctk.CTkLabel(self, text="Youtube Downloader", font=("Segoe UI Bold", 48))
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        self.grid_columnconfigure(0, weight=1)

        self.vid_frame = Vid(self)
        self.vid_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        self.playlist_frame = Playlist(self)
        self.playlist_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)


app = App()
app.mainloop()

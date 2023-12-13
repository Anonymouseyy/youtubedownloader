import yt_dlp, music_tag
import customtkinter as ctk
import threading
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


class DownloadOut(ctk.CTkFrame):
    def __init__(self, master, url):
        super().__init__(master)

        with yt_dlp.YoutubeDL() as ydl:
            title = ydl.extract_info(url, download=False)["title"]

        self.title = ctk.CTkLabel(self, text=title, font=("Segoe UI Bold", 24))
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.bar_label = ctk.CTkLabel(self, text="Progress", font=("Segoe UI Bold", 14))
        self.bar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.bar_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nw")
        self.bar.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="nw")

        self.text_label = ctk.CTkLabel(self, text="Output", font=("Segoe UI Bold", 14))
        self.text = ctk.CTkTextbox(self)
        self.text_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nw")
        self.text.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="nw")


class Vid(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title = ctk.CTkLabel(self, text="Video", font=("Segoe UI Bold", 24))
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.url_label = ctk.CTkLabel(self, text="URL: ", font=("Segoe UI Bold", 14))
        self.url = ctk.CTkEntry(self, placeholder_text="URL")
        self.url_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nw")
        self.url.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ne")


class Playlist(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title = ctk.CTkLabel(self, text="Playlist", font=("Segoe UI Bold", 24))
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.url_label = ctk.CTkLabel(self, text="URL: ", font=("Segoe UI Bold", 14))
        self.url = ctk.CTkEntry(self, placeholder_text="URL")
        self.url_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nw")
        self.url.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="nsew", columnspan=3)

        self.start_label = ctk.CTkLabel(self, text="Start Index: ", font=("Segoe UI Bold", 14))
        self.start = ctk.CTkEntry(self, placeholder_text="Leave Blank If First")
        self.end_label = ctk.CTkLabel(self, text="End Index: ", font=("Segoe UI Bold", 14))
        self.end = ctk.CTkEntry(self, placeholder_text="Leave Blank If Last")
        self.start_label.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nw")
        self.start.grid(row=3, column=1, padx=10, pady=(0, 10), sticky="nsew")
        self.end_label.grid(row=3, column=2, padx=10, pady=(0, 10), sticky="nw")
        self.end.grid(row=3, column=3, padx=10, pady=(0, 10), sticky="nsew")


class Options(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title = ctk.CTkLabel(self, text="Download", font=("Segoe UI Bold", 24))
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        def browse_folder():
            folder_path = ctk.filedialog.askdirectory()
            if folder_path:
                self.folder.delete(0, ctk.END)
                self.folder.insert(ctk.END, folder_path)

        self.folder_label = ctk.CTkLabel(self, text="Folder: ", font=("Segoe UI Bold", 14))
        self.folder = ctk.CTkEntry(self, placeholder_text="Folder")
        self.browse = ctk.CTkButton(self, text="Browse", command=browse_folder)
        self.folder_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nw")
        self.folder.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="nsew", columnspan=2)
        self.browse.grid(row=1, column=3, padx=10, pady=(0, 10), sticky="nw")

        self.kind_label = ctk.CTkLabel(self, text="Kind: ", font=("Segoe UI Bold", 14))
        self.kind = ctk.CTkOptionMenu(self, values=["Single", "Playlist"])
        self.format_label = ctk.CTkLabel(self, text="Format: ", font=("Segoe UI Bold", 14))
        self.format = ctk.CTkOptionMenu(self, values=["Video", "Audio"])
        self.kind_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nw")
        self.kind.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="nw")
        self.format_label.grid(row=2, column=2, padx=10, pady=(0, 10), sticky="nw")
        self.format.grid(row=2, column=3, padx=10, pady=(0, 10), sticky="nw")

        self.download = ctk.CTkButton(self, text="Download")
        self.download.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew", columnspan=4)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")

        self.main = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main.pack(fill=ctk.BOTH, expand=1)

        self.title("Youtube Downloader")
        self.geometry(f"{int(self.winfo_screenwidth())//2}x{int(self.winfo_screenheight())//2}")

        self.title = ctk.CTkLabel(self.main, text="Youtube Downloader", font=("Segoe UI Bold", 48))
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        self.grid_columnconfigure(0, weight=1)

        self.vid = Vid(self.main)
        self.vid.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        self.playlist = Playlist(self.main)
        self.playlist.grid(row=2, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        self.options = Options(self.main)
        self.options.grid(row=3, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        def download():
            if self.options.kind.get() == "Single":
                self.progress = DownloadOut(self.main, self.vid.url.get())
                self.progress.grid(row=4, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
                videodl = threading.Thread(target=download_video, args=(self.vid.url.get(), self.options.format.get(),
                                                                        self.options.folder.get()))
                videodl.start()
            if self.options.kind.get() == "Playlist":
                self.progress = DownloadOut(self.main, self.playlist.url.get())
                self.progress.grid(row=4, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
                playlistdl = threading.Thread(target=download_playlist(self.playlist.url.get(),
                                                                       self.options.format.get(),
                                                                       self.options.folder.get(),
                                                                       self.playlist.start.get(),
                                                                       self.playlist.end.get()))
                playlistdl.start()

        self.options.download.configure(command=download)


app = App()
app.mainloop()

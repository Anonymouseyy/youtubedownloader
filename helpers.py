import yt_dlp


def what_is(url):
    # Work around to printing errors to the console
    class ignoreErrors:
        @staticmethod
        def error(msg):
            print(msg)

        @staticmethod
        def warning(msg):
            pass

        @staticmethod
        def debug(msg):
            pass

    ydl_opts = {'skip_download': True, 'ignoreerrors': True, 'quiet': True, "logger": ignoreErrors, 'extract_flat': True, 'playlistend': 2}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, False)

    if 'playlist' in url:
        return 'playlist'
    else:
        return 'vid'

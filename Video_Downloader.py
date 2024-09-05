import yt_dlp

def download_video_yt_dlp(url, output_path):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Specify the output path and filename
        'noplaylist': True,                             # Download only the provided video, not the playlist
        'format': 'bestvideo+bestaudio/best',           # Download the best video and audio quality
        'merge_output_format': 'mp4',                   # Merge video and audio into an MP4 file
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


print("Enter the video link which you want to download: ")
link = input()

# Example usage
youtube_url =   link
output_path = 'C:/Users/Santosh Kumar/Downloads'
download_video_yt_dlp(youtube_url, output_path)




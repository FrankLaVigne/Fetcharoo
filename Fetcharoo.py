import sys
import os
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

def download_mp3(youtube_url, output_directory="./", filename=None):
    try:
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        if audio_stream is None:
            print("No audio stream found.")
            return

        print(f"Downloading: {yt.title}...")
        file_path = audio_stream.download(output_directory)

        base, ext = os.path.splitext(file_path)
        mp3_file = base + '.mp3'

        if filename:
            mp3_file = os.path.join(output_directory, filename + '.mp3')
            os.rename(file_path, mp3_file)
        else:
            os.rename(file_path, mp3_file)
        
        print(f"Download complete: {mp3_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_transcript(youtube_url):
    try:
        video_id = YouTube(youtube_url).video_id
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        for entry in transcript:
            print(f"{entry['start']:.2f} - {entry['start'] + entry['duration']:.2f}: {entry['text']}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <action> <youtube_url> [<filename>]")
        print("Actions: download_mp3, get_transcript")
        sys.exit(1)

    action = sys.argv[1].lower()
    youtube_url = sys.argv[2]
    filename = sys.argv[3] if len(sys.argv) > 3 else None

    if action == "download_mp3":
        download_mp3(youtube_url, filename=filename)
    elif action == "get_transcript":
        download_transcript(youtube_url)
    else:
        print("Invalid action. Please use 'download_mp3' or 'get_transcript'")
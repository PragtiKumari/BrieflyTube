from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0].split("?")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    else:
        return None

def fetch_transcript(url):
    video_id = get_video_id(url)
    if not video_id:
        return "Invalid YouTube URL."

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try English first
        try:
            transcript = transcript_list.find_transcript(['en'])
        except NoTranscriptFound:
            # Fall back to any generated transcript (like Hindi)
            transcript = transcript_list.find_generated_transcript(
                [t.language_code for t in transcript_list]
            )

        # Final fix: access .text, not ['text']
        full_text = " ".join([t.text for t in transcript.fetch()])
        return full_text

    except TranscriptsDisabled:
        return f"Error: Transcripts are disabled for this video {url}."
    except Exception as e:
        return f"Error: Could not retrieve a transcript for the video {url}! This is most likely caused by:\n\n{str(e)}"

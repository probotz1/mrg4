import ffmpeg
import subprocess

def merge_video_audio(video_path, audio_path, output_path):
    """
    Merge video and audio files using ffmpeg-python.
    Removes all existing audio tracks from the video and replaces them with the provided audio.
    """
    try:
        # Build the FFmpeg command
        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(audio_path)
        stream = ffmpeg.output(input_video, input_audio, output_path, vcodec='copy', acodec='aac', strict='experimental')
        
        # Execute the command
        ffmpeg.run(stream, overwrite_output=True)
        return True
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        raise
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

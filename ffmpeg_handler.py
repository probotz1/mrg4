import ffmpeg  # This imports the ffmpeg-python library

def merge_video_audio(video_path, audio_path, output_path):
    """
    Merge video and audio files using ffmpeg-python.
    Removes all existing audio tracks from the video and replaces them with the provided audio.
    """
    try:
        (
            ffmpeg
            .input(video_path)
            .input(audio_path)
            .output(output_path, vcodec='copy', acodec='aac', shortest=None)
            .run(overwrite_output=True)
        )
        return True
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr}")
        return False

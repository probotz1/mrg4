import ffmpeg

def merge_video_audio(video_path, audio_path, output_path):
    """
    Merge video and audio files using ffmpeg-python.
    Removes all existing audio tracks from the video and replaces them with the provided audio.
    """
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, c='copy')
            .output(output_path, c='copy', acodec='aac', shortest=None)
            .run(overwrite_output=True)
        )
        return True
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr}")
        return False

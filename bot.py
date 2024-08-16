import os
from pyrogram import Client, filters
from pyrogram.types import Message
import ffmpeg

# Replace with your own values
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

app = Client("video_audio_merge_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to store user states
user_states = {}

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Welcome! Send me a video file to start the merging process.")

@app.on_message(filters.video)
async def handle_video(client, message: Message):
    user_id = message.from_user.id
    video_file = await message.download()
    user_states[user_id] = {"video": video_file}
    await message.reply_text("Video received. Now send me an audio file.")

@app.on_message(filters.audio)
async def handle_audio(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_states or "video" not in user_states[user_id]:
        await message.reply_text("Please send a video file first.")
        return

    audio_file = await message.download()
    video_file = user_states[user_id]["video"]

    await message.reply_text("Processing... Please wait.")

    output_file = f"merged_{user_id}.mp4"
    
    try:
        # Merge video and audio using FFmpeg
        input_video = ffmpeg.input(video_file)
        input_audio = ffmpeg.input(audio_file)
        
        (
            ffmpeg
            .output(input_video, input_audio, output_file, vcodec='copy', acodec='aac')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )

        # Send the merged file
        await client.send_video(user_id, output_file)
        await message.reply_text("Here's your merged video!")

    except ffmpeg.Error as e:
        await message.reply_text(f"An error occurred: {e.stderr.decode()}")

    finally:
        # Clean up files
        os.remove(video_file)
        os.remove(audio_file)
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # Clear user state
        del user_states[user_id]

app.run()

from pyrogram import Client, filters
from pyrogram.types import Message
from ffmpeg_handler import merge_video_audio
import os
import uuid

# Configuration
API_ID = "28015531"
API_HASH = "2ab4ba37fd5d9ebf1353328fc915ad28"
BOT_TOKEN = "7321073695:AAE2ZvYJg6_dQNhEvznmRCSsKMoNHoQWnuI"

# Temporary file storage directory
TEMP_DIR = "temp_files"

app = Client("video_audio_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to hold user sessions and file paths
user_sessions = {}

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply("Send me a video file to start.")

@app.on_message(filters.video & filters.private)
async def video_handler(client: Client, message: Message):
    user_id = message.from_user.id
    video_file = await message.download(file_name=os.path.join(TEMP_DIR, f"{uuid.uuid4()}_video.mp4"))

    # Store the video path in user session
    user_sessions[user_id] = {"video_path": video_file}

    await message.reply("Now send me an audio file.")

@app.on_message(filters.audio | filters.voice & filters.private)
async def audio_handler(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id not in user_sessions or "video_path" not in user_sessions[user_id]:
        await message.reply("Please send a video file first.")
        return

    audio_file = await message.download(file_name=os.path.join(TEMP_DIR, f"{uuid.uuid4()}_audio.mp3"))

    # Get the video path from user session
    video_path = user_sessions[user_id]["video_path"]

    # Path for the merged output
    output_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_merged.mp4")

    # Merge video and audio
    try:
        merge_video_audio(video_path, audio_file, output_path)
        await message.reply_video(video=output_path, caption="Here is your merged video.")
    except Exception as e:
        await message.reply(f"Sorry, there was an error merging your video and audio: {e}")

    # Clean up
    os.remove(video_path)
    os.remove(audio_file)
    os.remove(output_path)
    del user_sessions[user_id]

# Ensure temp_files directory exists
os.makedirs(TEMP_DIR, exist_ok=True)

app.run()

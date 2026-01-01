from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
import os

# =================== تنظیمات ===================
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session = "music"

app = Client(session, api_id=api_id, api_hash=api_hash)
calls = PyTgCalls(app)

# =================== دستورات ===================
@app.on_message(filters.command(["ping"]))
async def ping(_, m):
    await m.reply("✅ آنلاینم")

@app.on_message(filters.command(["play", "پخش"]) & filters.group)
async def play(_, m):
    if not m.reply_to_message or not m.reply_to_message.audio:
        await m.reply("❌ روی فایل آهنگ ریپلای کن")
        return

    audio = await m.reply_to_message.download()
    await calls.join_group_call(
        m.chat.id,
        InputAudioStream(
            audio,
            HighQualityAudio(),
        ),
    )
    await m.reply("🎧 در حال پخش")

# =================== اجرای ربات ===================
from pyrogram import idle

async def main():
    await app.start()
    await calls.start()
    print("Userbot آماده و آنلاین است")
    await idle()

app.run(main())

from pyrogram import Client
from MusicPlayer.tgcalls import client as USER
from pyrogram import filters
from pyrogram.types import Chat, Message, User
from MusicPlayer.config import (
    BOT_USERNAME,
)

@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
  await USER.send_message(message.chat.id,"Hello, I am the assistant of music player, didn't have a time to talk with you 🙂 kindly join @BlueCodeSupport for any query\n\nMade by @AKH1LS.")
  return

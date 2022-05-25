import asyncio
import requests
from pyrogram import Client
from pytgcalls import idle
from MusicPlayer import app
from MusicPlayer import client
from MusicPlayer.database.functions import clean_restart_stage
from MusicPlayer.database.queue import get_active_chats, remove_active_chat
from MusicPlayer.tgcalls.calls import run
from MusicPlayer.config import API_ID, API_HASH, BOT_TOKEN, BG_IMG, OWNER_ID, BOT_NAME


response = requests.get(BG_IMG)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)


async def load_start():
    restart_data = await clean_restart_stage()
    if restart_data:
        print("[INFO]: SENDING RESTART STATUS")
        try:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted the Bot Successfully.**",
            )
        except Exception:
            pass
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        print("Error came while clearing db")
    for served_chat in served_chats:
        try:
            await remove_active_chat(served_chat)
        except Exception as e:
            print("Error came while clearing db")
            pass
    await app.send_message(OWNER_ID, "**Bot Started Successfully**\n\nMake sure you joined @AKH1LS for regular updates from me.")
    # If you change it then bot will be crash © copyrighted area
    await client.join_chat("BlueCodeSupport")
    await client.join_chat("AKH1LS")
    print("[INFO]: STARTED")
    

loop = asyncio.get_event_loop_policy().get_event_loop()
loop.run_until_complete(load_start())

Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "MusicPlayer.modules"},
).start()

run()
idle()
loop.close()

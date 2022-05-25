from asyncio import QueueEmpty

from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream

from pyrogram import Client, filters
from pyrogram.types import Message

from MusicPlayer import app
from MusicPlayer.config import que
from MusicPlayer.database.queue import (
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from MusicPlayer.tgcalls import calls
from MusicPlayer.utils.filters import command, other_filters
from MusicPlayer.utils.decorators import sudo_users_only
from MusicPlayer.tgcalls.queues import clear, get, is_empty, put, task_done


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await app.get_chat_member(chat_id, user_id)
    except Exception:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


from MusicPlayer.utils.administrator import adminsOnly


@app.on_message(command(["pause", "op"]) & other_filters)
async def pause(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🙄 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(
            "Nothing playing in voice chat."
        )
    elif not await is_music_playing(message.chat.id):
        return await message.reply_text(
            "Nothing playing in voice chat."
        )
    await music_off(chat_id)
    await calls.pytgcalls.pause_stream(chat_id)
    await message.reply_text(
        f"🥀 __**Voicechat Paused**__\n│\n🌹 Music paused by {checking}!"
    )


@app.on_message(command(["resume", "or"]) & other_filters)
async def resume(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🙄 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(
            "Nothing playing in voice chat."
        )
    elif await is_music_playing(chat_id):
        return await message.reply_text(
            "Nothing playing in voice chat."
        )
    else:
        await music_on(chat_id)
        await calls.pytgcalls.resume_stream(chat_id)
        await message.reply_text(
            f"🥀 __**Voicechat Resumed**__\n│\n🌹 Music resumed by {checking}!"
        )


@app.on_message(command(["end", "oe"]) & other_filters)
async def stop(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🙄 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await calls.pytgcalls.leave_group_call(chat_id)
        await message.reply_text(
            f"🥀 __**Voicechat End/Stopped**__\n│\n🌹 Music ended by {checking}!"
        )
    else:
        return await message.reply_text(
            "Nothing playing in voice chat."
        )


@app.on_message(command(["skip", "os"]) & other_filters)
async def skip(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🙄 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    chat_title = message.chat.title
    if not await is_active_chat(chat_id):
        await message.reply_text("Nothing playing in voice chat.")
    else:
        task_done(chat_id)
        if is_empty(chat_id):
            await remove_active_chat(chat_id)
            await message.reply_text(
                "**Next song not available**\n\n**»** `Leaving Voice Chat...`"
            )
            await calls.pytgcalls.leave_group_call(chat_id)
            return
        else:
            await calls.pytgcalls.change_stream(
                chat_id,
                InputStream(
                    InputAudioStream(
                        get(chat_id)["file"],
                    ),
                ),
            )
            await message.reply_text(
                f" __**Skipped.**__\n│\n🚶Music skipped by {checking}"
            )


@app.on_message(filters.command(["cleandb", "oc"]))
async def stop_cmd(_, message):
    if message.sender_chat:
        return await message.reply_text(
            "🙄 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    chat_id = message.chat.id
    checking = message.from_user.mention
    try:
        clear(chat_id)
    except QueueEmpty:
        pass
    await remove_active_chat(chat_id)
    try:
        await calls.pytgcalls.leave_group_call(chat_id)
    except:
        pass
    await message.reply_text(
        f"😉 __Erased queues in **{message.chat.title}**__\n│\n🚶Database cleaned by {checking}"
    )

# Copyright (C) 2020 TeamUltroid
# Ported by X_ImFine
# Recode by @mrismanaziz

import asyncio
import datetime

from telethon import events
from telethon.tl import functions, types

from userbot.events import register

from userbot import (  # noqa pylint: disable=unused-import isort:skip
    AFKREASON,
    ALIVE_NAME,
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    COUNT_MSG,
    ISAFK,
    LOGS,
    PM_AUTO_BAN,
    USERS,
    bot,
)

global USER_AFK
global afk_time
global last_afk_message
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
last_afk_message = {}
afk_start = {}


@bot.on(events.NewMessage(outgoing=True))
async def set_not_afk(event):
    if event.fwd_from:
        return
    global USER_AFK
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    came_back = datetime.datetime.now()
    afk_end = came_back.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message = event.message.message
    if "#" not in current_message and "yes" in USER_AFK:
        xx = await event.client.send_message(
            event.chat_id,
            f"**{ALIVE_NAME} Pengangguran So Sibuk Balik Lagi!**\n**Dari AFK :** `{total_afk_time}` **Yang Lalu**",
            file=pic,
        )
        try:
            await unsave_gif(event, xx)
        except BaseException:
            pass
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**#AFK Mode** = `False`\n{ALIVE_NAME} Pengangguran So Sibuk Balik Lagi!**\nDari AFK :** `{total_afk_time}` **Yang Lalu**",
            )
        except BaseException:
            pass
        await asyncio.sleep(5)
        await xx.delete()
        USER_AFK = {}
        afk_time = None


@bot.on(
    events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private))
)
async def on_afk(event):
    if event.fwd_from:
        return
    global USER_AFK
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    cum_back = datetime.datetime.now()
    afk_end = cum_back.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if USER_AFK and not (await event.get_sender()).bot:
        msg = None
        if reason == "":
            message_to_reply = (
                f"**✘ Maaf {ALIVE_NAME} Sedang AFK** `{total_afk_time}` **Yang Lalu ✘**"
            )
        else:
            message_to_reply = (
                f"**✘ {ALIVE_NAME} Sedang AFK** `{total_afk_time}` **Yang Lalu ✘**\n"
                + f"**✦҈͜͡➳ Karena :** `{reason}`"
            )
        msg = await event.reply(message_to_reply, file=pic)
        try:
            await unsave_gif(event, msg)
        except BaseException:
            pass
        await asyncio.sleep(2)
        if event.chat_id in last_afk_message:
            await last_afk_message[event.chat_id].delete()
        last_afk_message[event.chat_id] = msg


@register(outgoing=True, pattern=r"^\.afk ?(.*)", disable_errors=True)
async def _(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    global USER_AFK
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    global reason
    global pic
    USER_AFK = {}
    afk_time = None
    last_afk_message = {}
    afk_end = {}
    start_1 = datetime.datetime.now()
    afk_start = start_1.replace(microsecond=0)
    owo = event.text[5:]
    reason = owo
    pic = await event.client.download_media(reply)
    if not USER_AFK:
        last_seen_status = await bot(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.datetime.now()
        if owo == "":
            USER_AFK = f"yes: not-mentiond {pic}"
            x = await bot.send_message(event.chat_id, f"**Bye Gua AFK Dulu**", file=pic)
            try:
                await unsave_gif(event, x)
            except BaseException:
                pass
            await asyncio.sleep(0.001)
            await event.delete()
            try:
                xy = await bot.send_message(
                    BOTLOG_CHATID, f"**#AFK Mode** = `True`", file=pic
                )
                try:
                    await unsave_gif(event, xy)
                except BaseException:
                    pass
            except Exception as e:
                LOGS.warn(str(e))
        else:
            USER_AFK = f"yes: {reason} {pic}"
            x = await bot.send_message(
                event.chat_id,
                f"**Bye Gua AFK Dulu**\n\n**Karena :** `{reason}`",
                file=pic,
            )
            try:
                await unsave_gif(event, x)
            except BaseException:
                pass
            await asyncio.sleep(0.001)
            await event.delete()
            try:
                xy = await bot.send_message(
                    BOTLOG_CHATID,
                    f"**#AFK Mode** = `True`\n**Karena:** `{reason}`",
                    file=pic,
                )
                try:
                    await unsave_gif(event, xy)
                except BaseException:
                    pass
            except Exception as e:
                LOGS.warn(str(e))


CMD_HELP.update(
    {
        "afk": "**Plugin : **`afk`\
        \n\n  •  **Syntax :** `.afk` <alasan> bisa <sambil reply sticker/foto/gif/media>\
        \n  •  **Function : **Memberi tahu kalau Master sedang afk bisa dengan menampilkan media keren ketika seseorang menandai atau membalas salah satu pesan atau dm Anda.\
        \n\n  •  **Syntax :** `.off`\
        \n  •  **Function : **Memberi tahu kalau Master sedang OFFLINE, dan menguubah nama belakang menjadi 【 OFF 】 \
    "
    }
)

# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """


from userbot import ALIVE_NAME, CHANNEL
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, ICON_HELP, bot
from userbot.events import man_cmd, sudo_cmd
from userbot.utils import edit_delete, edit_or_reply

modules = CMD_HELP


@bot.on(man_cmd(pattern="help(?:\\s|$)(.*)"))
@bot.on(sudo_cmd(pattern="help(?:\\s|$)(.*)", allow_sudo=True))
async def help(event):
    """For help command"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await edit_or_reply(event, str(CMD_HELP[args]))
        else:
            await edit_delete(event, f"`{args}` **Bukan Nama Modul yang Valid.**", 15)
    else:
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += f"`\t\t{ICON_HELP}\t\t"
        await edit_or_reply(
            event,
            f"**✦ Daftar Perintah Untuk Man-Userbot:**\n"
            f"**✦ Jumlah** `{len(modules)}` **Modules**\n"
            f"**✦ Owner:** `{ALIVE_NAME}`\n\n"
            f"{ICON_HELP}  {string}"
            f"\n\nSupport {CHANNEL}",
        )
        await edit_or_reply(
            event,
            f"\n**Contoh Ketik** `{cmd}help afk` **Untuk Melihat Informasi Module**",
        )

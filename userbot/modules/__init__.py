# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Init file which loads all of the modules """
import asyncio
import datetime
import os
import time
from random import choice
from telethon import Button, events
from telethon.tl import functions, types

from userbot import *
from userbot import CHANNEL, CMD_HELP, CMD_HANDLER, GROUP, LOGS, SUDO_HANDLER, SUDO_USERS, bot
from userbot.modules import *
from userbot.utils import *
from userbot.utils.core import *
from userbot.utils.resources import *
from userbot.utils.tools import (
    check_media,
    edit_delete,
    edit_or_reply,
    human_to_bytes,
    humanbytes,
    md5,
    media_to_pic,
    media_type,
    post_to_telegraph,
    reply_id,
    run_cmd,
    runcmd,
    take_screen_shot,
    time_formatter,
)

cmd = CMD_HANDLER
scmd = SUDO_HANDLER

user = bot.get_me()
OWNER_NAME = user.first_name
OWNER_ID = user.id
mention = f"[{user.first_name}](tg://user?id={user.id})"
hmention = f"<a href = tg://user?id={user.id}>{Config.first_name}</a>"
my_channel = CHANNEL or "Lunatic0de"
my_group = GROUP or "SharingUserbot"
if "@" in my_channel:
    my_channel = my_channel.replace("@", "")
if "@" in my_group:
    my_group = my_group.replace("@", "")

logo = "./userbot/resources/logo.jpg"

sudos = SUDO_USERS
if sudos:
    is_sudo = "True"
else:
    is_sudo = "False"


async def get_user_id(ids):
    if str(ids).isdigit():
        userid = int(ids)
    else:
        userid = (await bot.get_entity(ids)).id
    return userid


def __list_all_modules():
    import glob
    from os.path import basename, dirname, isfile

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    return [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]


ALL_MODULES = sorted(__list_all_modules())
LOGS.info("Modules To Load : %s", str(ALL_MODULES))
__all__ = ALL_MODULES + ["ALL_MODULES"]

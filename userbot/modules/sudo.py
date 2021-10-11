import heroku3
from telethon.tl.functions.users import GetFullUserRequest

from userbot import HEROKU_API_KEY, HEROKU_APP_NAME, SUDO_USERS, bot
from userbot.events import man_cmd
from userbot.utils import edit_delete as eod
from userbot.utils import edit_or_reply as eor

Heroku = heroku3.from_key(HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
sudousers = SUDO_USERS


@bot.on(man_cmd(pattern="sudo"))
async def sudo(event):
    sudo = "True" if SUDO_USERS else "False"
    users = sudousers
    if sudo == "True":
        await eor(event, f"📍 **Sudo :**  `Enabled`\n\n📝 **Sudo users :**  `{users}`")
    else:
        await eod(event, f"📍 **Sudo :**  `Disabled`")


@bot.on(man_cmd(pattern="addsudo(?: |$)"))
async def add(event):
    ok = await eor(event, "**Adding Sudo User...**")
    bot = "SUDO_USERS"
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await eod(
            ok,
            "**Silahkan Set-Up**  `HEROKU_APP_NAME` **untuk menambahkan pengguna sudo!!**",
        )
        return
    heroku_Config = app.config()
    if event is None:
        return
    try:
        target = await get_user(event)
    except Exception:
        await eod(ok, f"Reply to a user to add them in sudo.")
    if sudousers:
        newsudo = f"{sudousers} {target}"
    else:
        newsudo = f"{target}"
    await ok.edit(
        f"**Added**  `{target}`  **in Sudo User.**\n\n __Restarting Heroku to Apply Changes. Wait for a minute.__"
    )
    heroku_Config[bot] = newsudo


@bot.on(man_cmd(pattern="rmsudo(?: |$)"))
async def _(event):
    ok = await eor(event, "**🚫 Removing Sudo User...**")
    bot = "SUDO_USERS"
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await eod(ok, "**Please Set-Up**  HEROKU_APP_NAME to remove sudo users!!")
        return
    heroku_Config = app.config()
    if event is None:
        return
    try:
        target = await get_user(event)
        gett = str(target)
    except Exception:
        await eod(ok, f"Reply to a user to remove them from sudo.")
    if gett in sudousers:
        newsudo = sudousers.replace(gett, "")
        await ok.edit(
            f"**Removed**  `{target}`  from Sudo User.\n\n Restarting Heroku to Apply Changes. Wait for a minute."
        )
        heroku_Config[bot] = newsudo
    else:
        await ok.edit("**Pengguna ini tidak ada dalam Daftar Pengguna Sudo Anda.**")


async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.forward.sender_id)
            )
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
    target = replied_user.user.id
    return target

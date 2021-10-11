import heroku3
from telethon.tl.functions.users import GetFullUserRequest

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, HEROKU_API_KEY, HEROKU_APP_NAME, SUDO_USERS, bot
from userbot.events import man_cmd
from userbot.utils import edit_delete, edit_or_reply

Heroku = heroku3.from_key(HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
sudousers = SUDO_USERS


@bot.on(man_cmd(pattern="sudo"))
async def sudo(event):
    sudo = "True" if SUDO_USERS else "False"
    users = sudousers
    if sudo == "True":
        await edit_or_reply(
            event, f"📍 **Sudo :** `Enabled`\n\n📝 **Sudo users :** `{users}`"
        )
    else:
        await edit_delete(event, f"📍 **Sudo :** `Disabled`")


@bot.on(man_cmd(pattern="addsudo(?: |$)"))
async def add(event):
    ok = await edit_or_reply(event, "`Adding Sudo User...`")
    bot = "SUDO_USERS"
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await edit_delete(
            ok,
            "**Silahkan Tambahkan** `HEROKU_APP_NAME` **untuk menambahkan pengguna sudo!!**",
        )
        return
    heroku_Config = app.config()
    if event is None:
        return
    try:
        target = await get_user(event)
    except Exception:
        await edit_delete(
            ok, f"**Balas ke Pesan pengguna untuk menambahkannya di sudo.**"
        )
    if sudousers:
        newsudo = f"{sudousers} {target}"
    else:
        newsudo = f"{target}"
    await ok.edit(
        f"**Berhasil Menambahkan** `{target}` **di Pengguna Sudo.**\n\n__Sedang Merestart Heroku untuk Menerapkan Perubahan. Tunggu Sebentar__"
    )
    heroku_Config[bot] = newsudo


@bot.on(man_cmd(pattern="delsudo(?: |$)"))
async def _(event):
    ok = await edit_or_reply(event, "`Removing Sudo User...`")
    bot = "SUDO_USERS"
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await edit_delete(
            ok,
            "**Silahkan Tambahkan** `HEROKU_APP_NAME` **untuk menghapus pengguna sudo!!**",
        )
        return
    heroku_Config = app.config()
    if event is None:
        return
    try:
        target = await get_user(event)
        gett = str(target)
    except Exception:
        await edit_delete(ok, f"Balas ke pengguna untuk menghapusnya dari sudo.")
    if gett in sudousers:
        newsudo = sudousers.replace(gett, "")
        await ok.edit(
            f"**Berhasil Menghapus** `{target}` **Dari Pengguna Sudo.**\n\n__Sedang Merestart Heroku untuk Menerapkan Perubahan. Tunggu Sebentar__"
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


CMD_HELP.update(
    {
        "sudo": f"**Plugin : **`sudo`\
        \n\n  •  **Syntax :** `{cmd}sudo`\
        \n  •  **Function : **Untuk Mengecek Sudo.\
        \n\n  •  **Syntax :** `{cmd}addsudo`\
        \n  •  **Function : **Untuk Menambahkan Pengguna sudo.\
        \n\n  •  **Syntax :** `{cmd}delsudo`\
        \n  •  **Function : **Untuk Menghapus Pengguna sudo.\
    "
    }
)

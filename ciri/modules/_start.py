import datetime
import time

from telethon import types

from ciri import ALIVE_PIC, StartTime
from ciri.utils import ciri_cmd, eor

from .db import get_dp, set_dp

ALIVE_PIC = []

ALIVE_CAPTION = """
<b>The Ciri Userbot...</b>

<b>Hey,  I am alive.</b>

<b>✵ Owner -</b> {}
<b>✵ Ciri -</b> v1.2
<b>✵ UpTime -</b> {}
<b>✵ Python -</b> <code>3.10</code>
<b>✵ Telethon -</b> </code>1.25.1</code>
<b>✵ Branch -</b>  <a href='github.com/amarnathcjd/cirilla-userbot'>master</a>
"""


@ciri_cmd(pattern="alive", allow_sudo=True)
async def _start(e):
    me = await e.client.get_me()
    await e.delete()
    file, _t = construct_dp()
    print(file)
    if _t == "sticker":
        await e.respond(file=file)
        file = None
    try:
        await e.respond(
            ALIVE_CAPTION.format(me.first_name, (time.time() - StartTime) / 3600),
            file=file,
            parse_mode="html",
            link_preview=False,
        )
    except Exception as abc:
        print(abc)


@ciri_cmd(pattern="ping")
async def _ping(e):
    s = datetime.datetime.now()
    r = await eor(e, "`Pinging...`")
    f = datetime.datetime.now() - s
    await r.edit(
        "Pong!\n<code>{}</code>".format(str(f.microseconds)[:3] + " ms"),
        parse_mode="html",
    )


def construct_dp():
    dp = get_dp()
    if not dp:
        return None, "nil"
    if dp["type"] == "link":
        return dp["id"], "link"
    elif dp["type"] in ["sticker", "gif"]:
        return (
            types.Document(
                id=dp["id"],
                access_hash=dp["access_hash"],
                file_reference=dp["file_reference"],
            ),
            dp["type"],
        )
    elif dp["type"] == "photo":
        return (
            types.Photo(
                id=dp["id"],
                access_hash=dp["access_hash"],
                file_reference=dp["file_reference"],
                dc_id=4,
                date=datetime.datetime.now(),
                sizes=0,
            ),
            "photo",
        )


@ciri_cmd(pattern="setalive")
async def _setalive(e):
    r = await e.get_reply_message()
    p = e.text.split("")
    if not r.media and len(p) > 1:
        set_dp(p[1], "", "", "link")
        await eor(e, "`Setted.`")
    elif r.media:
        if r.photo:
            set_dp(
                r.photo.id,
                r.photo.access_hash,
                r.photo.file_reference,
                "photo",
            )
        elif r.sticker:
            set_dp(
                r.sticker.id,
                r.sticker.access_hash,
                r.sticker.file_reference,
                "sticker",
            )
        elif r.gif:
            set_dp(
                r.gif.id,
                r.gif.access_hash,
                r.gif.file_reference,
                "gif",
            )
        await eor(e, "`Setted.`")
    else:
        await eor(e, "`I can't set this.`")

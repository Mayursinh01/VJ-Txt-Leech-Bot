# Don't Remove Credit Tg - @VJ_Bots

import time
time.sleep(10)
import os
import re
import sys
import time
import asyncio
import requests
from subprocess import getstatusoutput

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

# ✅ important fix
os.makedirs("downloads", exist_ok=True)

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(
        f"<b>Hello {m.from_user.mention} 👋\n\nSend /upload to start.</b>"
    )


@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped**🚦")
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('Send TXT file')

    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete()

    try:
        with open(x, "r") as f:
            content = f.read().split("\n")

        links = [i.split("://", 1) for i in content if i.strip()]
        os.remove(x)

    except:
        await m.reply_text("Invalid file")
        os.remove(x)
        return

    await editable.edit(f"Total Links: {len(links)}\nSend start index (1)")

    input0: Message = await bot.listen(editable.chat.id)
    count = int(input0.text)
    await input0.delete()

    await editable.edit("Send Batch Name")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete()

    await editable.edit("Enter Quality (360/480/720/1080)")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete()

    await editable.edit("Send Caption")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete()

    await editable.edit("Send Thumbnail URL or 'no'")
    input6: Message = await bot.listen(editable.chat.id)
    thumb = input6.text
    await input6.delete()
    await editable.delete()

    if thumb.startswith("http"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = "no"

    for i in range(count - 1, len(links)):
        try:
            name1 = links[i][0].strip()
            url = "https://" + links[i][1]

            name = f"{str(i+1).zfill(3)}_{name1[:50]}"

            cmd = f'yt-dlp -f "best" "{url}" -o "{name}.mp4"'

            msg = await m.reply_text(f"Downloading: {name}")

            res_file = await helper.download_video(url, cmd, name)

            await msg.delete()

            await bot.send_video(
                chat_id=m.chat.id,
                video=res_file,
                caption=f"{name}\nBatch: {raw_text0}",
                thumb=thumb if thumb != "no" else None
            )

            os.remove(res_file)
            time.sleep(1)

        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await m.reply_text(f"Error: {str(e)}")

    await m.reply_text("Done ✅")


# ✅ stability fix for Render
time.sleep(5)

bot.run()

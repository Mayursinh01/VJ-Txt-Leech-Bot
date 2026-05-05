# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import time
import datetime
import aiohttp
import aiofiles
import asyncio
import logging
import requests
import subprocess
import concurrent.futures

from utils import progress_bar
from pyrogram import Client, filters
from pyrogram.types import Message

os.makedirs("downloads", exist_ok=True)

def duration(filename):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return float(result.stdout)
    except:
        return 0

def exec(cmd):
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout.decode()
    print(output)
    return output

def pull_run(work, cmds):
    with concurrent.futures.ThreadPoolExecutor(max_workers=work) as executor:
        print("Waiting for tasks to complete")
        fut = executor.map(exec, cmds)

async def aio(url, name):
    k = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(k, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return k

async def download(url, name):
    ka = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ka, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return ka

def parse_vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = []
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ", 2)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    new_info.append((i[0], i[2]))
            except:
                pass
    return new_info

def vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = dict()
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ", 3)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    new_info.update({f'{i[2]}': f'{i[0]}'})
            except:
                pass
    return new_info

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(f'[{cmd!r} exited with {proc.returncode}]')
    if proc.returncode == 1:
        return False
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'

def old_download(url, file_name, chunk_size=1024 * 10):
    if os.path.exists(file_name):
        os.remove(file_name)
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
    return file_name

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"


# ✅ MAIN FIX - download_video
async def download_video(url, cmd, name):
    # ✅ Try yt-dlp with aria2c
    download_cmd = (
        f'{cmd} '
        f'-R 25 --fragment-retries 25 '
        f'--external-downloader aria2c '
        f'--downloader-args "aria2c:-x 16 -j 32" '
        f'--no-check-certificate '
        f'--user-agent "Mozilla/5.0" '
    )
    print(download_cmd)
    logging.info(download_cmd)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        lambda: subprocess.run(download_cmd, shell=True)
    )

    # ✅ Check all possible output paths
    possible = [
        f"downloads/{name}.mp4",
        f"downloads/{name}.mkv",
        f"downloads/{name}.webm",
        f"{name}.mp4",
        f"{name}.mkv",
        f"{name}.webm",
        name,
    ]

    for path in possible:
        if os.path.isfile(path) and os.path.getsize(path) > 0:
            return path

    # ✅ Fallback - direct aiohttp download for signed URLs
    try:
        print(f"yt-dlp failed, trying direct download for: {url}")
        path = f"downloads/{name}.mp4"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://www.classsx.co.in/",
                "Accept": "*/*",
            }) as resp:
                if resp.status == 200:
                    async with aiofiles.open(path, 'wb') as f:
                        async for chunk in resp.content.iter_chunked(1024 * 1024):
                            await f.write(chunk)
                    if os.path.isfile(path) and os.path.getsize(path) > 0:
                        return path
    except Exception as e:
        print(f"Direct download also failed: {e}")

    return None


async def send_doc(bot: Client, m: Message, cc, ka, cc1, prog, count, name):
    reply = await m.reply_text(f"Uploading » `{name}`")
    time.sleep(1)
    start_time = time.time()
    await m.reply_document(ka, caption=cc1)
    count += 1
    await reply.delete(True)
    time.sleep(1)
    os.remove(ka)
    time.sleep(3)


async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog):
    subprocess.run(
        f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{filename}.jpg"',
        shell=True)
    await prog.delete(True)
    reply = await m.reply_text(f"**Uploading ...** - `{name}`")
    try:
        if thumb == "no":
            thumbnail = f"{filename}.jpg"
        else:
            thumbnail = thumb
    except Exception as e:
        await m.reply_text(str(e))

    dur = int(duration(filename))
    start_time = time.time()

    try:
        await m.reply_video(
            filename, caption=cc,
            supports_streaming=True,
            height=720, width=1280,
            thumb=thumbnail, duration=dur,
            progress=progress_bar,
            progress_args=(reply, start_time))
    except Exception:
        await m.reply_document(
            filename, caption=cc,
            progress=progress_bar,
            progress_args=(reply, start_time))

    os.remove(filename)
    try:
        os.remove(f"{filename}.jpg")
    except:
        pass
    await reply.delete(True)

import os
import yt_dlp
import discord

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

async def join_voice(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("🎵 Joined the voice channel.")
        print("[VC] Joined voice channel.")
    else:
        await ctx.send("❌ You must be in a voice channel.")
        print("[VC] Join failed — user not in VC.")

async def play_music(ctx, url, bot):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice:
        await ctx.send("❌ I'm not in a voice channel.")
        return

    if os.path.exists("song.mp3"):
        os.remove("song.mp3")

    await ctx.send("⏳ Downloading audio...")
    print(f"[YT] Downloading: {url}")
    download_audio(url)
    await ctx.send("▶️ Playing now...")

    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    print("[VC] Now playing.")

async def leave_voice(ctx):
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if voice:
        await voice.disconnect()
        await ctx.send("👋 Left the voice channel.")
        print("[VC] Disconnected.")
    else:
        await ctx.send("❌ I'm not in a voice channel.")

async def send_voice_note(ctx):
    if os.path.exists("song.mp3"):
        await ctx.send("📤 Sending audio as voice note...", file=discord.File("song.mp3"))
        print("[SEND] Sent audio as voice note.")
    else:
        await ctx.send("❌ No song file found.")

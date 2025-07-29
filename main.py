import os
import asyncio
import threading
import discord
from discord.ext import commands
import discum
from keep_alive import keep_alive
import player
from dotenv import load_dotenv

load_dotenv()  # Load secrets from .env

BOT_TOKEN = os.environ.get("BOT_TOKEN")
USER_TOKEN = os.environ.get("USER_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)
client = discum.Client(token=USER_TOKEN, log=True)

@bot.event
async def on_ready():
    print(f"[BOT] Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    await player.join_voice(ctx)

@bot.command()
async def play(ctx, url):
    await player.play_music(ctx, url, bot)

@bot.command()
async def leave(ctx):
    await player.leave_voice(ctx)

@bot.command()
async def sendnote(ctx):
    await player.send_voice_note(ctx)

@client.gateway.command
def on_message(resp):
    if resp.event.message:
        m = resp.parsed.auto()
        if m['content'].startswith('ping'):
            print("[DISCUM] Ping received.")
            client.sendMessage(m['channel_id'], "Pong from selfbot ✅")

def run_all():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    threading.Thread(target=bot.run, args=(BOT_TOKEN,), daemon=True).start()
    threading.Thread(target=client.gateway.run, daemon=True).start()

run_all()
keep_alive()

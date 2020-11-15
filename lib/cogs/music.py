from discord.ext.commands import Cog
from discord.ext.commands import command
import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import time
import asyncio

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {"options": "-vn -loglevel quiet -hide_banner -nostats", "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 0 -nostdin"}

queue = []

def queue_next(self, ctx):
    try:
        print("Playing next song!")
        # asyncio.run(ctx.send("Now playing next song!"))
        if len(queue) >= 1:
            del queue[0]
            vc = get(self.bot.voice_clients, guild=ctx.guild)
            vc.play(FFmpegPCMAudio(queue[0], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
    except IndexError:
        print("No more songs in queue.")
        # asyncio.run(ctx.send("No more songs in queue!"))

class Music(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="play", aliases=["Play", "PLAY"])
    async def play(self, ctx, url):
        print("play command used")

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            global title
            title = info["title"]
        URL = info["formats"][0]["url"]
        queue.append(URL)

        channel = ctx.author.voice.channel
        voice_channel = get(self.bot.voice_clients, guild=ctx.guild)

        if voice_channel and voice_channel.is_connected():
            print("Bot connected to voice channel.")
            await voice_channel.move_to(channel)

            if voice_channel.is_playing():
                print("Song added to queue.")
                await ctx.send("Song added to queue!")

        else:
            vc = await channel.connect()

            vc.play(FFmpegPCMAudio(queue[0], **FFMPEG_OPTIONS), after=lambda e: queue_next(self, ctx))
            vc.is_playing()

    @command(name="stop", aliases=["Stop", "STOP"])
    async def stop(self, ctx):
        await ctx.send("WIP")
        print("stop command used")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("music")


def setup(bot):
    bot.add_cog(Music(bot))

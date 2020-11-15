from datetime import datetime
from glob import glob
from asyncio import sleep
from termcolor import colored
import youtube_dl
import discord

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from discord.ext.commands import Bot as BotBase
from discord import Embed, File
from discord.ext.commands import CommandNotFound

from ..db import db

PREFIX = "+"
OWNER_IDS = [752492641970814986]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")

    def run(self, version):
        self.VERSION = version

        print(colored("running setup...", "yellow"))
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print(colored("running bot...", "yellow"))
        super().run(self.TOKEN, reconnect=True)

    # async def print_message(self):
    #    channel = self.get_channel(599569584005185539)
    #    await channel.send("Timed Test.")

    async def on_connect(self):
        print(" bot connected")

    async def on_disconnect(self):
        print(" bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            print(args, kwargs)
            await args[0].send("Etwas ist schief gelaufen. :(")

        error_log = self.get_channel(768867099614773358)
        await error_log.send("Error: " + args + kwargs)

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(503104675256729600)
            self.stdout = self.get_channel(599569584005185539)
            # self.scheduler.add_job(self.print_message, CronTrigger(second="0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55"))
            self.scheduler.start()

            # Send message
            await self.stdout.send("Ich bin online!")

            # Send embed
            # embed = Embed(title="Online", description="Alpha Bot ist online!", colour=0xFF0000, timestamp=datetime.utcnow())
            # fields = [("Name", "Value", True),
            #          ("Test", "Test", True),
            #          ("Test2", "Test2", False)]
            # for name, value, inline in fields:
            #    embed.add_field(name=name, value=value, inline=inline)
            # embed.set_footer(text="Footer Test")
            # embed.set_author(name="Alpha Bot", icon_url=self.guild.icon_url)
            # embed.set_thumbnail(url=self.guild.icon_url)
            # embed.set_image(url=self.guild.icon_url)
            # await channel.send(embed=embed)

            # Send file
            # await channel.send(file=File("./data/images/burger_test.jpg"))

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            print(colored("bot ready", "green"))
            self.ready = True

        else:
            print(colored("bot reconnected", "green"))

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()

from discord.ext.commands import Cog
from discord.ext.commands import command


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="test", aliases=["TEST"])
    async def test_command(self, ctx):
        await ctx.send(f"Hallo, {ctx.author.mention}!")
        print("test command used")

    @command(name="lolol", aliases=["lol"])
    async def lol_command(self, ctx):
        await ctx.send("lol")
        print("lol command used")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))

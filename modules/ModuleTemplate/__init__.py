from discord.ext import commands

class Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="test", description="Test command")
    @commands.is_owner()
    async def setup_event(self, ctx:commands.Context, event_name:str):
        await ctx.send("Test command", ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(Cog(bot))
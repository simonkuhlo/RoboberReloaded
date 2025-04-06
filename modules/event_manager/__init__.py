from discord.ext import commands
from .ui.views import event_manager as event_manager_ui
from . import ref
from . import api



class EventManagerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="setup_event", description="Sets up a new event on the current Server")
    @commands.is_owner()
    async def setup_event(self, ctx:commands.Context, event_name:str):
        await api.create_event(guild=ctx.guild, name=event_name)
        await ctx.send("Event wurde erstellt :thumbsup:", ephemeral=True)
    
    @commands.hybrid_command(name="create_event_control_button", description="Control Events")
    @commands.is_owner()
    async def create_event_control_button(self, ctx:commands.Context):
        await ctx.send("", view=event_manager_ui.View())


async def setup(bot:commands.Bot):
    ref.bot = bot
    await bot.add_cog(EventManagerCog(bot))
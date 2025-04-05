from . import event_manager_discord_helper as backend
from . import event_manager_edit_view
from discord.ext import commands
from core_app import db_model as db



class EventManagerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="setup_event", description="Sets up a new event on the current Server")
    @commands.is_owner()
    async def setup_event(self, ctx:commands.Context, event_name:str):
        await backend.create_event(guild=ctx.guild, event=db.EventDiscordWrapper(name=event_name))
        await ctx.send("Event wurde erstellt :thumbsup:", ephemeral=True)
    
    @commands.hybrid_command(name="create_event_control_button", description="Control Events")
    @commands.is_owner()
    async def create_event_control_button(self, ctx:commands.Context):
        await ctx.send("", view=event_manager_edit_view.EditButton())


async def setup(bot):
    await bot.add_cog(EventManagerCog(bot))
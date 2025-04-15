import discord
from discord.ext import commands
from discord import ui

event_roles = {
    "Game Jam" : 963691849653059584,
}

def get_select_options():
    select_options = []
    for event in event_roles:
        option = discord.SelectOption(label=event)
        select_options.append(option)
    return select_options


class MultiSelectView(discord.ui.View):
    @discord.ui.select(
        placeholder="Events auswählen...",
        min_values=0,
        max_values=len(event_roles.keys()),
        options=get_select_options()
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):

        guild = interaction.guild

        roles_to_remove = [guild.get_role(role_id) for role_id in event_roles.values() if guild.get_role(role_id)]
        await interaction.user.remove_roles(*roles_to_remove)

        roles_to_add = [guild.get_role(event_roles[value]) for value in select.values if guild.get_role(event_roles[value])]
        await interaction.user.add_roles(*roles_to_add)

        await interaction.response.send_message(f"Ausgewählte Events: {', '.join(select.values)}", ephemeral=True)

class SelectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="test", description="Eventroles multi-select")
    @commands.is_owner()
    async def haha(self, ctx):
        view = MultiSelectView()
        await ctx.send("----------\n:point_up: Wähle die Events aus, an denen du interessiert bist:\n----------", view=view)

async def setup(bot):
    await bot.add_cog(SelectCog(bot))

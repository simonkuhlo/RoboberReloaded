import discord
from ..views.edit import edit_menu_select
from ...ref import event

class Button(discord.ui.Button):
    def __init__(self):
        super().__init__(custom_id="EditEventStart")
        self.label = "Edit Event"
        self.style = discord.ButtonStyle.blurple
        self.event = event

    async def callback(self, interaction:discord.Interaction):
        options = await edit_menu_select.get_editable_events(interaction.guild, interaction.user)
        if options:
            await interaction.response.send_message(f"Select the event you want to edit:", ephemeral=True, view = edit_menu_select.View(options))
        else:
            await interaction.response.send_message("No editable events found for this user.", ephemeral=True)
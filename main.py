import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
used_token = os.getenv("USED_TOKEN")
bot_token = os.getenv(used_token)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.load_extension("modules.event_manager")
        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

bot = MyBot()
bot.run(bot_token)

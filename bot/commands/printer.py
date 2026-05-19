import discord
from discord.ext import commands
from discord import app_commands

class Printer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="printer", description="Bot repeats whatever you input!")
    async def printer(self, interaction: discord.Interaction, msg: str):
        await interaction.response.send_message(f"'{msg}' \n-# -By {interaction.user.name}")

async def setup(bot):
    await bot.add_cog(Printer(bot))

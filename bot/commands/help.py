import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Shows commands.")
    @app_commands.allowed_contexts(dms=True, private_channels=True, guilds=True)
    async def help_cmd(self, interaction: discord.Interaction):
        embed_help_cmd = discord.Embed(title="Help", color=discord.Color.purple(), description="Commands:")
        embed_help_cmd.add_field(name="Profile", value="Check some basic info about someones profile!")
        embed_help_cmd.add_field(name="Printer", value="Prints message you input!", inline=False)
        embed_help_cmd.add_field(name="Ping", value="Shows bot latency.", inline=False)
        await interaction.response.send_message(embed=embed_help_cmd)

async def setup(bot):
    await bot.add_cog(Help(bot))
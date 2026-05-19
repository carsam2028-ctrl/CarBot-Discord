import discord
from datetime import timedelta
from discord.ext import commands
from discord import app_commands


class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="timeout", description="Timeouts selected user")
    @app_commands.checks.has_permissions(mute_members=True, moderate_members=True)
    @app_commands.describe(time="Time (in minutes) you want to timeout this person.",
                           member="Person you want to timeout.",
                           reason="Reason to timeout this user.")
    @app_commands.guild_only
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, time: int, reason: str):
        await interaction.response.defer(ephemeral=False)
        duration = timedelta(minutes=time)
        if member == interaction.user:
            await interaction.followup.send("You cannot timeout yourself!", ephemeral=True)
        if time < 1:
            await interaction.followup.send("Time cannot be less than 1 minute.", ephemeral=True)
        if member == self.user:
            await interaction.followup.send("You cannot timeout the bot this way.", ephemeral=True)
        await member.timeout(duration, reason=reason)
        await interaction.followup.send(f"{member} has been timed out for {time} minutes. Reason: {reason}", ephemeral=False)
class RemoveTimeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="removetimeout", description="Removes timeout from selected user")
    @app_commands.checks.has_permissions(mute_members=True, moderate_members=True)
    @app_commands.describe(reason="Reason to remove timeout from this user.")
    @app_commands.guild_only
    async def remove_timeout(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await interaction.response.defer(ephemeral=False)
        duration = None
        if member == interaction.user:
            await interaction.followup.send("You cannot remove your own timeout!", ephemeral=True)
        if not member.is_timed_out():
            await interaction.followup.send("User is not timed out!")
        await member.timeout(duration, reason=reason)
        await interaction.followup.send(f"{member}'s timeout has been removed. Reason: {reason}", ephemeral=False)

async def setup(bot):
    await bot.add_cog(Timeout(bot))
    await bot.add_cog(RemoveTimeout(bot))
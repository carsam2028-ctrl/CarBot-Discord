import discord
import time
from discord.ext import commands
from discord import app_commands


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Purge messages")
    @app_commands.describe(amount="How many messages you want to purge (1-100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.allowed_contexts(dms=False, private_channels=True, guilds=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)

        if 100 > amount < 1:
            await interaction.followup.send("Whoa, that is over/under the limit.", ephemeral=True)
        else:
            deleted_msg = await interaction.channel.purge(limit=amount, reason=f"{interaction.user} used purge command.", check=lambda msg: not msg.pinned)
            await interaction.followup.send(f"{len(deleted_msg)} message(s) deleted.", ephemeral=False)
            time.sleep(3.5)
            await interaction.delete_original_response()

async def setup(bot):
    await bot.add_cog(Purge(bot))

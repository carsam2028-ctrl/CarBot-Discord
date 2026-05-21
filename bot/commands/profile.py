import discord
from discord.ext import commands
from discord import app_commands

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profile", description="Check out a discord profile!")
    @app_commands.describe(user="User's profile to fetch")
    @app_commands.allowed_contexts(dms=False, private_channels=True, guilds=True)
    async def profile_checker(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer(ephemeral=False)
        fetch_user = await self.fetch_user(user.id)
        #Initialize Embed w/ title and color for main profile
        embed_profile = discord.Embed(title=f"Profile of {user.display_name}", color=discord.Color.dark_orange())
        #Add to embed_profile
        embed_profile.add_field(name="Display Name:", value=f"{user.display_name}")
        embed_profile.add_field(name="User Name:", value=f"{user.name}", inline=False)
        embed_profile.add_field(name="User ID:", value=f"`{user.id}`", inline=False)
        embed_profile.add_field(name="Joined Discord:", value=f"{user.created_at.strftime('%Y-%m-%d')}", inline=False)
        embed_profile.add_field(name="User Profile:", value="", inline=False)
        embed_profile.set_image(url=f"{user.display_avatar.url}")
        await interaction.followup.send(embed=embed_profile)

        #Initialize Another Embed w/ title and color for banner
        embed_profile_banner = discord.Embed(title=f"{user.display_name}'s banner")
        #Checks if user has a custom banner and if not, does not send an image
        if fetch_user.banner is not None:
            embed_profile_banner.add_field(name="User Banner:", value="\u200b", inline=False)
            embed_profile_banner.set_image(url=f"{fetch_user.banner.url}")
        else:
            embed_profile_banner.add_field(name="User does not have a banner", value="\u200b", inline=False)
        await interaction.followup.send(embed=embed_profile_banner)

async def setup(bot):
    await bot.add_cog(Profile(bot))

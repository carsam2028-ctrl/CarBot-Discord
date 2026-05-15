#Imports
import os
import discord
import dotenv
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
load_dotenv()


#Variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.message_content = True


#Bot Startup
class CarBot(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.tree.sync()
        print('Synced Commands Globally!')
        await self.tree.sync(guild=discord.Object(id=1504288510650093570))
        print('Synced Commands in Home Server!')


bot = CarBot(command_prefix='CB!', intents=intents)
#Error Handler
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    err_msg = ""
    print(f"Error: {str(error)}")
    if isinstance(error, app_commands.CommandInvokeError):
        error = error.original
        err_msg = "Command Invoke Error has occurred, please try again."
    elif isinstance(error, app_commands.MissingPermissions):
        err_msg = "You do not have the necessary permission(s) for this command."
    elif isinstance(error, app_commands.BotMissingPermissions):
        err_msg = "Bot does not have required permission(s)."
    elif isinstance(error, discord.HTTPException):
        err_msg = "An HTTP Exception has occurred, try again."
    else:
        err_msg = f"A fatal error has occurred: {str(error)}"


    if interaction.response.is_done():
        await interaction.followup.send(f"{err_msg}")
    else:
        await interaction.response.send_message(f"{err_msg}")
#Commands
@bot.tree.command(name="ping", description="Check the bot's latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Latency: {round(bot.latency * 1000)}ms")


@bot.tree.command(name="profile", description="Check out a discord profile!")
async def profile_checker(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(ephemeral=False)
    #Initialize Embed w/ title and color
    embed_profile = discord.Embed(title=f"Display: {user.display_name}", color=discord.Color.dark_orange())
    #Add to embed_profile
    embed_profile.add_field(name="User Name:", value=f"{user.name}")
    embed_profile.add_field(name="User ID:", value=f"`{user.id}`")
    embed_profile.set_image(url=f"{user.display_avatar}")
    await interaction.followup.send(embed=embed_profile)


@bot.tree.command(name="printer", description="Bot repeats whatever you input!")
async def printer(interaction: discord.Interaction, msg: str):
    await interaction.response.send_message(f"{interaction.user.mention} said: {msg}")
#Loop
bot.run(DISCORD_TOKEN)
